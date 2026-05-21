"""FastAPI backend for rag-starter — wraps the src/ RAG library as a REST API."""

import json
import logging
import os

from fastapi import FastAPI, Request  # ASGI web framework — serves the RAG API
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel  # Request validation — bundled with FastAPI

from backend.db import init_db
from backend.routes.collections import router as collections_router
from backend.routes.conversations import router as conversations_router
from src.embedder import embed_query
from src.errors import IndexNotFoundError, RagStarterError
from src.generator import generate_answer_stream
from src.pipeline import index_documents
from src.store import create_store, query_store, store_exists

logger = logging.getLogger(__name__)

app = FastAPI(title="rag-starter")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(collections_router)
app.include_router(conversations_router)


@app.on_event("startup")
def startup() -> None:
    """Initialize the SQLite database on first run."""
    init_db()


class IndexRequest(BaseModel):
    """Body for POST /api/index (legacy, operates on default collection)."""

    folder_path: str = "./sample-docs"
    chunk_size: int = 500
    chunk_overlap: int = 50
    db_path: str = "./chroma_db"
    embed_model: str = "nomic-embed-text"


class QueryRequest(BaseModel):
    """Body for POST /api/query (legacy, operates on default collection)."""

    question: str
    top_k: int = 5
    model: str = "llama3.1:8b"
    db_path: str = "./chroma_db"
    embed_model: str = "nomic-embed-text"


@app.exception_handler(RagStarterError)
async def rag_error_handler(request: Request, exc: RagStarterError) -> JSONResponse:
    """Return structured JSON for any rag-starter library error."""
    return JSONResponse(
        status_code=422,
        content={"error": type(exc).__name__, "message": str(exc)},
    )


@app.get("/api/health")
def health() -> dict:
    """Check if Ollama is running and required models are available."""
    import ollama  # Local LLM runner — checked at request time, not import time

    result: dict = {"ollama": False, "models": {}}
    try:
        models_response = ollama.list()
        available = [m.model for m in models_response.models] if models_response.models else []
        result["ollama"] = True
        result["models"] = {m: True for m in available}
    except Exception:
        pass
    return result


@app.post("/api/index", response_model=None)
def index(req: IndexRequest) -> dict | JSONResponse:
    """Index documents from a folder into the default collection."""
    if not os.path.isdir(req.folder_path):
        return JSONResponse(
            status_code=400,
            content={"error": "InvalidPath", "message": f"Folder not found: {req.folder_path}"},
        )
    return index_documents(
        folder_path=req.folder_path, db_path=req.db_path,
        chunk_size=req.chunk_size, chunk_overlap=req.chunk_overlap,
        embed_model=req.embed_model,
    )


@app.get("/api/index/status")
def index_status(db_path: str = "./chroma_db") -> dict:
    """Check whether an index exists and how many chunks it contains."""
    exists = store_exists(db_path)
    chunk_count = 0
    if exists:
        _client, collection = create_store(path=db_path)
        chunk_count = collection.count()
    return {"indexed": exists, "chunk_count": chunk_count}


@app.post("/api/query")
def query(req: QueryRequest) -> StreamingResponse:
    """Query the default collection and stream the answer via SSE."""
    if not store_exists(req.db_path):
        raise IndexNotFoundError(req.db_path)
    query_embedding = embed_query(req.question, model=req.embed_model)
    _client, collection = create_store(path=req.db_path)
    results = query_store(collection, query_embedding, top_k=req.top_k)
    if not results:
        def no_results():
            msg = "No relevant documents found. Try rephrasing or indexing more documents."
            yield f"event: token\ndata: {json.dumps({'text': msg})}\n\n"
            yield "event: sources\ndata: []\n\nevent: done\ndata: {}\n\n"
        return StreamingResponse(no_results(), media_type="text/event-stream")
    context_chunks = [r["content"] for r in results]
    sources = [
        {"content": r["content"], "metadata": r["metadata"], "distance": r["distance"]}
        for r in results
    ]

    def event_stream():
        for token in generate_answer_stream(req.question, context_chunks, model=req.model):
            yield f"event: token\ndata: {json.dumps({'text': token})}\n\n"
        yield f"event: sources\ndata: {json.dumps(sources)}\n\n"
        yield "event: done\ndata: {}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")
