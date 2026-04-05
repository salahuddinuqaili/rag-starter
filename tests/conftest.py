"""Shared test fixtures — sample data, mock embeddings, and temp directories."""

import pytest

from src.loader import Document


@pytest.fixture
def sample_text() -> str:
    """A known 1000-character paragraph for testing chunking behavior."""
    return (
        "Retrieval-Augmented Generation (RAG) is a technique that combines "
        "information retrieval with text generation. Instead of relying solely "
        "on what a language model memorised during training, RAG first searches "
        "a knowledge base for relevant documents and then feeds those documents "
        "to the model as additional context. This approach has several advantages. "
        "First, it allows the model to answer questions about private or recent "
        "information that was not in its training data. Second, it reduces "
        "hallucination because the model can ground its answers in actual source "
        "material. Third, it makes the system more transparent because you can "
        "see exactly which documents informed the answer. The typical RAG pipeline "
        "has five stages: loading documents from various file formats, splitting "
        "them into manageable chunks, converting those chunks into numerical "
        "embeddings, storing the embeddings in a vector database, and finally "
        "retrieving the most relevant chunks to include in the prompt sent to the "
        "language model. Each stage can be tuned independently. For example, you "
        "can adjust the chunk size, change the embedding model, or modify the "
        "prompt template to improve results for your specific use case."
    )


@pytest.fixture
def sample_documents() -> list[Document]:
    """Three Document objects with varied content for testing the pipeline."""
    return [
        Document(
            content=(
                "Remote work requires intentional communication. Teams should "
                "default to asynchronous methods like written updates and shared "
                "documents rather than scheduling meetings for every discussion. "
                "When meetings are necessary, always circulate an agenda beforehand "
                "and share notes within 24 hours."
            ),
            metadata={"source": "remote-work.md", "page": 0},
        ),
        Document(
            content=(
                "Machine learning is the practice of teaching computers to find "
                "patterns in data. Supervised learning uses labelled examples — "
                "like emails tagged as spam or not spam — to train a model. "
                "Unsupervised learning discovers structure without labels, such as "
                "grouping customers by purchasing behaviour."
            ),
            metadata={"source": "intro-to-ml.md", "page": 0},
        ),
        Document(
            content=(
                "Berlin is a city of contrasts. Kreuzberg pulses with street art "
                "and independent cafés. Mitte houses world-class museums along the "
                "Spree. Prenzlauer Berg is where young families brunch on weekends. "
                "The U-Bahn and S-Bahn networks make it easy to hop between "
                "neighbourhoods without a car."
            ),
            metadata={"source": "berlin-guide.md", "page": 0},
        ),
    ]


@pytest.fixture
def mock_embeddings() -> list[list[float]]:
    """Deterministic 768-dimensional embedding vectors for testing.

    Three vectors pointing in different directions so cosine similarity
    can distinguish them in retrieval tests.
    """
    dim = 768
    # Vector 1: mostly positive first half
    vec1 = [1.0 / (i + 1) for i in range(dim)]
    # Vector 2: alternating positive/negative
    vec2 = [(-1.0) ** i / (i + 1) for i in range(dim)]
    # Vector 3: mostly positive second half
    vec3 = [1.0 / (dim - i) for i in range(dim)]
    return [vec1, vec2, vec3]


@pytest.fixture
def temp_chroma_path(tmp_path):
    """A temporary directory for an isolated ChromaDB instance."""
    return str(tmp_path / "test_chroma_db")
