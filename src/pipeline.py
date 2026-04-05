"""Orchestrate the full RAG pipeline: index documents and query them."""

import logging
import time

from src.chunker import chunk_documents
from src.embedder import embed_query, embed_texts
from src.generator import generate_answer
from src.loader import load_folder
from src.store import add_documents, create_store, query_store, store_exists

logger = logging.getLogger(__name__)


def index_documents(
    folder_path: str,
    db_path: str = "./chroma_db",
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    verbose: bool = False,
) -> dict:
    """Load, chunk, embed, and store documents from a folder.

    This is the main entry point for indexing. It runs the full pipeline:
    load files → split into chunks → generate embeddings → save to ChromaDB.

    Args:
        folder_path: Path to the folder containing your documents.
        db_path: Where to store the ChromaDB database on disk.
        chunk_size: Maximum characters per chunk (default 500).
        chunk_overlap: Characters of overlap between chunks (default 50).
        verbose: When True, print what each stage is doing and how long it took.

    Returns:
        A dict with stats: files_loaded, chunks_created, time_seconds.

    Example:
        stats = index_documents("./my-docs", verbose=True)
        # {"files_loaded": 7, "chunks_created": 42, "time_seconds": 3.2}
    """
    total_start = time.time()

    # Stage 1: Load files
    stage_start = time.time()
    docs = load_folder(folder_path, verbose=verbose)
    if verbose:
        print(f"[loader] Loaded {len(docs)} documents in {time.time() - stage_start:.1f}s")

    if not docs:
        print(f"No supported files found in {folder_path}")
        return {"files_loaded": 0, "chunks_created": 0, "time_seconds": 0.0}

    # Stage 2: Chunk documents
    stage_start = time.time()
    chunk_texts, chunk_metadatas = chunk_documents(docs, chunk_size, chunk_overlap)
    if verbose:
        print(f"[chunker] Created {len(chunk_texts)} chunks in {time.time() - stage_start:.1f}s")

    # Stage 3: Generate embeddings
    stage_start = time.time()
    embeddings = embed_texts(chunk_texts)
    if verbose:
        print(f"[embedder] Embedded {len(chunk_texts)} chunks in {time.time() - stage_start:.1f}s")

    # Stage 4: Store in ChromaDB
    stage_start = time.time()
    _client, collection = create_store(path=db_path)
    add_documents(collection, chunk_texts, embeddings, chunk_metadatas)
    if verbose:
        print(f"[store] Stored {len(chunk_texts)} chunks in {time.time() - stage_start:.1f}s")

    total_time = time.time() - total_start
    if verbose:
        print(f"[pipeline] Indexing complete in {total_time:.1f}s")

    return {
        "files_loaded": len(docs),
        "chunks_created": len(chunk_texts),
        "time_seconds": round(total_time, 2),
    }


def query_documents(
    question: str,
    db_path: str = "./chroma_db",
    top_k: int = 5,
    model: str = "llama3.1:8b",
    verbose: bool = False,
) -> dict:
    """Retrieve relevant chunks and generate an answer to a question.

    This is the main entry point for querying. It embeds the question,
    finds similar chunks in ChromaDB, then sends them to the LLM.

    Args:
        question: The question you want answered.
        db_path: Path to the ChromaDB database created by index_documents.
        top_k: How many chunks to retrieve (default 5).
        model: The Ollama model to use for generating the answer.
        verbose: When True, print retrieval results before generation.

    Returns:
        A dict with 'answer' (str) and 'sources' (list of dicts with
        content, metadata, and distance).

    Example:
        result = query_documents("What is machine learning?")
        # result["answer"] == "Machine learning is..."
        # result["sources"][0]["metadata"]["source"] == "intro-to-ml.md"
    """
    if not store_exists(db_path):
        return {
            "answer": "No index found. Run index_documents() or index_folder.py first.",
            "sources": [],
        }

    total_start = time.time()

    # Stage 1: Embed the question
    stage_start = time.time()
    query_embedding = embed_query(question)
    if verbose:
        print(f"[embedder] Embedded query in {time.time() - stage_start:.1f}s")

    # Stage 2: Retrieve similar chunks
    stage_start = time.time()
    _client, collection = create_store(path=db_path)
    results = query_store(collection, query_embedding, top_k=top_k)
    if verbose:
        print(f"[store] Retrieved {len(results)} chunks in {time.time() - stage_start:.1f}s")
        for i, r in enumerate(results):
            print(f"  [{i+1}] {r['metadata'].get('source', '?')} (distance: {r['distance']:.4f})")

    # Stage 3: Generate answer
    stage_start = time.time()
    context_chunks = [r["content"] for r in results]
    answer = generate_answer(question, context_chunks, model=model)
    if verbose:
        print(f"[generator] Generated answer in {time.time() - stage_start:.1f}s")
        print(f"[pipeline] Total query time: {time.time() - total_start:.1f}s")

    return {"answer": answer, "sources": results}
