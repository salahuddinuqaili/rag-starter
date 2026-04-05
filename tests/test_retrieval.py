"""Integration test: index known chunks, query, and verify correct retrieval."""

from unittest.mock import patch

from src.store import add_documents, create_store, query_store, store_exists


def test_store_roundtrip(temp_chroma_path, mock_embeddings):
    """Add chunks with known embeddings and retrieve the most similar one."""
    chunks = [
        "Remote work requires async communication.",
        "Machine learning finds patterns in data.",
        "Berlin has great public transit.",
    ]
    metadatas = [
        {"source": "remote-work.md", "page": 0, "chunk_index": 0},
        {"source": "intro-to-ml.md", "page": 0, "chunk_index": 0},
        {"source": "berlin-guide.md", "page": 0, "chunk_index": 0},
    ]

    _client, collection = create_store(path=temp_chroma_path)
    add_documents(collection, chunks, mock_embeddings, metadatas)

    # Query with the first embedding — should retrieve the first chunk as closest
    results = query_store(collection, mock_embeddings[0], top_k=1)
    assert len(results) == 1
    assert results[0]["content"] == chunks[0]
    assert results[0]["metadata"]["source"] == "remote-work.md"
    assert "distance" in results[0]


def test_query_store_top_k(temp_chroma_path, mock_embeddings):
    """top_k should limit the number of results returned."""
    chunks = ["Chunk A", "Chunk B", "Chunk C"]
    metadatas = [{"source": "a.md"}, {"source": "b.md"}, {"source": "c.md"}]

    _client, collection = create_store(path=temp_chroma_path)
    add_documents(collection, chunks, mock_embeddings, metadatas)

    results = query_store(collection, mock_embeddings[0], top_k=2)
    assert len(results) == 2


def test_query_store_empty_collection(temp_chroma_path):
    """Querying an empty collection should return an empty list."""
    _client, collection = create_store(path=temp_chroma_path)
    dummy_embedding = [0.0] * 768

    results = query_store(collection, dummy_embedding, top_k=5)
    assert results == []


def test_store_exists_true(temp_chroma_path, mock_embeddings):
    """store_exists should return True after adding documents."""
    _client, collection = create_store(path=temp_chroma_path)
    add_documents(
        collection,
        ["test chunk"],
        [mock_embeddings[0]],
        [{"source": "test.md"}],
    )
    assert store_exists(temp_chroma_path) is True


def test_store_exists_false(tmp_path):
    """store_exists should return False for a non-existent path."""
    assert store_exists(str(tmp_path / "does_not_exist")) is False


def test_add_documents_increments_ids(temp_chroma_path, mock_embeddings):
    """Adding documents twice should not cause ID collisions."""
    _client, collection = create_store(path=temp_chroma_path)

    add_documents(
        collection,
        ["First chunk"],
        [mock_embeddings[0]],
        [{"source": "a.md"}],
    )
    assert collection.count() == 1

    add_documents(
        collection,
        ["Second chunk"],
        [mock_embeddings[1]],
        [{"source": "b.md"}],
    )
    assert collection.count() == 2


def test_pipeline_query_mocked(temp_chroma_path, mock_embeddings):
    """Full query pipeline with mocked Ollama calls."""
    # Set up the store with known data
    _client, collection = create_store(path=temp_chroma_path)
    add_documents(
        collection,
        ["RAG combines retrieval with generation."],
        [mock_embeddings[0]],
        [{"source": "rag.md", "chunk_index": 0}],
    )

    # Mock both embed and generate calls
    with patch("src.embedder.ollama") as mock_ollama:
        mock_ollama.embed.return_value = {"embeddings": [mock_embeddings[0]]}

        from src.embedder import embed_query
        query_vec = embed_query("What is RAG?")

        results = query_store(collection, query_vec, top_k=1)
        assert len(results) == 1
        assert "RAG" in results[0]["content"]
