"""Generate embeddings (lists of numbers that capture text meaning) via Ollama."""

import logging
import os
import sys

import ollama  # Local LLM runner — provides embedding models without cloud APIs

logger = logging.getLogger(__name__)


def embed_texts(
    texts: list[str],
    model: str = "nomic-embed-text",
) -> list[list[float]]:
    """Convert a list of text strings into embedding vectors using Ollama.

    Each text becomes a list of 768 numbers that represent its meaning.
    Similar texts get similar numbers, which is how retrieval works.

    Args:
        texts: The strings to embed.
        model: The Ollama embedding model to use.

    Returns:
        A list of embedding vectors, one per input text.

    Raises:
        SystemExit: If Ollama is not running or unreachable.

    Example:
        vectors = embed_texts(["Hello world", "Goodbye world"])
        # len(vectors) == 2, len(vectors[0]) == 768
    """
    try:
        response = ollama.embed(model=model, input=texts)
        return response["embeddings"]
    except Exception as e:
        if "connect" in str(e).lower() or "connection" in str(e).lower():
            logger.error(
                "Could not connect to Ollama. Is it running? "
                "Start it with: ollama serve"
            )
            sys.exit(1)
        raise


def embed_query(
    query: str,
    model: str = "nomic-embed-text",
) -> list[float]:
    """Embed a single query string into a vector.

    Convenience wrapper around embed_texts for the common case of
    embedding one question at a time.

    Args:
        query: The text to embed.
        model: The Ollama embedding model to use.

    Returns:
        A single embedding vector (list of floats).

    Example:
        vec = embed_query("What is machine learning?")
        # len(vec) == 768
    """
    results = embed_texts([query], model=model)
    return results[0]


def embed_texts_openai(
    texts: list[str],
    model: str = "text-embedding-3-small",
) -> list[list[float]]:
    """Embed texts using OpenAI's API instead of Ollama.

    Only use this if you have an OPENAI_API_KEY set in your environment
    and want cloud-based embeddings. Ollama is the default and works
    offline with no API key.

    Args:
        texts: The strings to embed.
        model: The OpenAI embedding model to use.

    Returns:
        A list of embedding vectors, one per input text.

    Raises:
        SystemExit: If OPENAI_API_KEY is not set.

    Example:
        vectors = embed_texts_openai(["Hello world"])
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not set. Export it or use Ollama instead.")
        sys.exit(1)

    from openai import OpenAI  # Cloud LLM API — only imported when explicitly chosen

    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model=model, input=texts)
    return [item.embedding for item in response.data]
