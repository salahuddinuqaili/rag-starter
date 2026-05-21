"""Routes for collection management, indexing, querying, and document ops."""

import json
import os
import shutil

import chromadb  # Embedded vector DB — used to delete collections and list documents
from fastapi import APIRouter, UploadFile  # APIRouter groups related endpoints
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel  # Request validation — bundled with FastAPI

from backend.db import create_collection, delete_collection, list_collections
from src.chunker import chunk_documents
from src.embedder import embed_query, embed_texts
from src.errors import IndexNotFoundError
from src.generator import generate_answer_stream
from src.loader import EXTENSION_HANDLERS
from src.pipeline import index_documents
from src.store import add_documents, create_store, query_store, store_exists

router = APIRouter(prefix="/api/collections", tags=["collections"])

UPLOAD_DIR = "./uploads"
DB_PATH = "./chroma_db"


class CollectionCreate(BaseModel):
    """Body for POST /api/collections."""

    name: str


class IndexRequest(BaseModel):
    """Body for POST /api/collections/{name}/index."""

    folder_path: str = "./sample-docs"
    chunk_size: int = 500
    chunk_overlap: int = 50
    embed_model: str = "nomic-embed-text"


class QueryRequest(BaseModel):
    """Body for POST /api/collections/{name}/query."""

    question: str
    top_k: int = 5
    model: str = "llama3.1:8b"
    embed_model: str = "nomic-embed-text"


# --- CRUD ---

@router.post("")
def create(body: CollectionCreate) -> dict:
    """Create a new named collection."""
    return create_collection(body.name)


@router.get("")
def list_all() -> list[dict]:
    """List all collections with chunk counts from ChromaDB."""
    collections = list_collections()
    for c in collections:
        try:
            _client, coll = create_store(path=DB_PATH, collection_name=c["name"])
            c["chunk_count"] = coll.count()
        except Exception:
            c["chunk_count"] = 0
    return collections


@router.delete("/{name}", status_code=204)
def delete(name: str) -> None:
    """Delete a collection from SQLite and ChromaDB."""
    delete_collection(name)
    try:
        client = chromadb.PersistentClient(path=DB_PATH)
        client.delete_collection(name)
    except Exception:
        pass
    upload_path = os.path.join(UPLOAD_DIR, name)
    if os.path.isdir(upload_path):
        shutil.rmtree(upload_path)


# --- Index & Query ---

@router.post("/{name}/index", response_model=None)
def index_collection(name: str, req: IndexRequest) -> dict | JSONResponse:
    """Index a folder into a named collection."""
    if not os.path.isdir(req.folder_path):
        return JSONResponse(
            status_code=400,
            content={"error": "InvalidPath", "message": f"Not found: {req.folder_path}"},
        )
    return index_documents(
        folder_path=req.folder_path, db_path=DB_PATH,
        chunk_size=req.chunk_size, chunk_overlap=req.chunk_overlap,
        embed_model=req.embed_model,
    )


@router.post("/{name}/query")
def query(name: str, req: QueryRequest) -> StreamingResponse:
    """Query a collection and stream the answer via SSE."""
    if not store_exists(DB_PATH):
        raise IndexNotFoundError(DB_PATH)
    query_embedding = embed_query(req.question, model=req.embed_model)
    _client, collection = create_store(path=DB_PATH, collection_name=name)
    results = query_store(collection, query_embedding, top_k=req.top_k)
    if not results:
        def empty():
            msg = "No relevant documents found. Try rephrasing or indexing more documents."
            yield f"event: token\ndata: {json.dumps({'text': msg})}\n\n"
            yield "event: sources\ndata: []\n\nevent: done\ndata: {}\n\n"
        return StreamingResponse(empty(), media_type="text/event-stream")
    context_chunks = [r["content"] for r in results]
    sources = [
        {"content": r["content"], "metadata": r["metadata"], "distance": r["distance"]}
        for r in results
    ]

    def stream():
        for token in generate_answer_stream(req.question, context_chunks, model=req.model):
            yield f"event: token\ndata: {json.dumps({'text': token})}\n\n"
        yield f"event: sources\ndata: {json.dumps(sources)}\n\n"
        yield "event: done\ndata: {}\n\n"
    return StreamingResponse(stream(), media_type="text/event-stream")


# --- Upload & Document Management ---

@router.post("/{name}/upload")
async def upload_file(name: str, file: UploadFile) -> dict:
    """Upload and index a single file into a collection."""
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in EXTENSION_HANDLERS:
        return JSONResponse(status_code=400, content={
            "error": "UnsupportedType", "message": "Supported: .pdf, .md, .txt",
        })
    dest_dir = os.path.join(UPLOAD_DIR, name)
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, file.filename)
    with open(dest_path, "wb") as f:
        f.write(await file.read())
    handler = EXTENSION_HANDLERS[ext]
    result = handler(dest_path)
    docs = result if isinstance(result, list) else [result]
    texts, metas = chunk_documents(docs)
    embeddings = embed_texts(texts)
    _client, collection = create_store(path=DB_PATH, collection_name=name)
    add_documents(collection, texts, embeddings, metas)
    return {"source": file.filename, "chunks_created": len(texts)}


@router.get("/{name}/documents")
def list_documents(name: str) -> list[dict]:
    """List distinct source documents in a collection with chunk counts."""
    _client, collection = create_store(path=DB_PATH, collection_name=name)
    if collection.count() == 0:
        return []
    result = collection.get(include=["metadatas"])
    sources: dict[str, int] = {}
    for meta in result["metadatas"]:
        src = meta.get("source", "unknown")
        sources[src] = sources.get(src, 0) + 1
    return [{"source": s, "chunk_count": c} for s, c in sources.items()]


@router.delete("/{name}/documents/{source}", status_code=204)
def delete_document(name: str, source: str) -> None:
    """Remove all chunks for a given source file from a collection."""
    _client, collection = create_store(path=DB_PATH, collection_name=name)
    result = collection.get(where={"source": source}, include=[])
    if result["ids"]:
        collection.delete(ids=result["ids"])
