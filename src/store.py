"""ChromaDB wrapper: create collections, add documents, and query by similarity."""

import logging
import os

import chromadb  # Embedded vector database — stores embeddings locally, no server needed

logger = logging.getLogger(__name__)


def create_store(
    path: str = "./chroma_db",
    collection_name: str = "documents",
) -> tuple[chromadb.ClientAPI, chromadb.Collection]:
    """Create or open a ChromaDB persistent store and return client + collection.

    ChromaDB stores embedding vectors on disk so you don't have to re-embed
    documents every time you restart.

    Args:
        path: Directory where ChromaDB stores its data.
        collection_name: Name of the collection inside the database.

    Returns:
        A tuple of (client, collection) ready for adding or querying.

    Example:
        client, collection = create_store("./my_db", "notes")
    """
    client = chromadb.PersistentClient(path=path)
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )
    return client, collection


def add_documents(
    collection: chromadb.Collection,
    chunks: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict],
) -> None:
    """Add chunked documents with their embeddings to a ChromaDB collection.

    Each chunk gets a string ID like "chunk_0", "chunk_1", etc.
    If the collection already has documents, new IDs continue from the
    existing count to avoid collisions.

    Args:
        collection: The ChromaDB collection to add to.
        chunks: The text content of each chunk.
        embeddings: The embedding vector for each chunk.
        metadatas: Metadata dict for each chunk (source filename, page, etc.).

    Example:
        add_documents(collection, ["Hello world"], [[0.1, 0.2, ...]], [{"source": "test.md"}])
    """
    existing_count = collection.count()
    ids = [f"chunk_{existing_count + i}" for i in range(len(chunks))]

    # ChromaDB requires metadata values to be str, int, float, or bool
    safe_metadatas = [
        {k: str(v) if not isinstance(v, (str, int, float, bool)) else v for k, v in m.items()}
        for m in metadatas
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=safe_metadatas,
    )
    logger.info("[store] Added %d chunks to collection", len(chunks))


def query_store(
    collection: chromadb.Collection,
    query_embedding: list[float],
    top_k: int = 5,
    where: dict | None = None,
    max_distance: float | None = None,
) -> list[dict]:
    """Find the most similar chunks to a query embedding.

    Uses cosine similarity to rank stored chunks and returns the top-k
    most relevant ones with their content, metadata, and distance score.

    Args:
        collection: The ChromaDB collection to search.
        query_embedding: The embedding vector of the user's question.
        top_k: How many results to return (fewer if the collection is small).
        where: Optional ChromaDB metadata filter, e.g. {"source": "report.pdf"}.
            Only chunks matching this filter will be searched.
        max_distance: Optional relevance threshold (0.0 = identical, 2.0 = opposite).
            Results with distance above this value are filtered out. For cosine
            distance, 0.3 is a reasonable threshold — anything above 0.5 is
            usually irrelevant.

    Returns:
        A list of dicts, each with 'content', 'metadata', and 'distance' keys.
        Lower distance means higher similarity.

    Example:
        results = query_store(collection, query_vec, top_k=3)
        # results[0]["content"] == "The most relevant chunk text..."

        # Filter by source file:
        results = query_store(collection, query_vec, where={"source": "report.pdf"})

        # Only return relevant results:
        results = query_store(collection, query_vec, max_distance=0.4)
    """
    actual_k = min(top_k, collection.count())
    if actual_k == 0:
        return []

    query_kwargs: dict = {
        "query_embeddings": [query_embedding],
        "n_results": actual_k,
    }
    if where is not None:
        query_kwargs["where"] = where

    results = collection.query(**query_kwargs)

    output: list[dict] = []
    for i in range(len(results["documents"][0])):
        distance = results["distances"][0][i]

        # Skip results that are too distant (irrelevant)
        if max_distance is not None and distance > max_distance:
            continue

        output.append({
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": distance,
        })
    return output


def store_exists(path: str = "./chroma_db") -> bool:
    """Check whether a ChromaDB index already exists at the given path.

    Useful for warning users to index documents before querying.

    Args:
        path: Directory where ChromaDB would store its data.

    Returns:
        True if the directory exists and contains ChromaDB files.

    Example:
        if not store_exists("./chroma_db"):
            print("Run index_folder.py first!")
    """
    return os.path.isdir(path) and len(os.listdir(path)) > 0
