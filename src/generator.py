"""Send a question plus retrieved context to an LLM and get an answer back."""

import logging
import os
from collections.abc import Generator

import ollama  # Local LLM runner — generates answers without cloud APIs

from src.errors import MissingAPIKeyError, OllamaConnectionError

logger = logging.getLogger(__name__)


RAG_PROMPT_TEMPLATE = """You are a helpful assistant. Answer the question based ONLY on the following context. If the context doesn't contain enough information to answer, say "I don't have enough information to answer that."

Context:
{context}

Question: {question}

Answer:"""


def format_context(chunks: list[str]) -> str:
    """Join retrieved text chunks into a single context string.

    Chunks are separated by '---' dividers so the LLM can see where
    one source ends and another begins.

    Args:
        chunks: The text chunks retrieved from the vector store.

    Returns:
        A single string with all chunks joined by dividers.

    Example:
        ctx = format_context(["Chunk one.", "Chunk two."])
        # "Chunk one.\\n---\\nChunk two."
    """
    return "\n---\n".join(chunks)


def generate_answer(
    question: str,
    context_chunks: list[str],
    model: str = "llama3.1:8b",
    prompt_template: str | None = None,
) -> str:
    """Send a question with context to Ollama and return the generated answer.

    Formats the prompt template with the provided context and question,
    then calls the local LLM to generate a grounded answer.

    Args:
        question: The user's question.
        context_chunks: Relevant text chunks retrieved from the vector store.
        model: The Ollama model to use for generation.
        prompt_template: Custom prompt template with {context} and {question}
            placeholders. Uses RAG_PROMPT_TEMPLATE if not provided.

    Returns:
        The LLM's answer as a plain string.

    Raises:
        OllamaConnectionError: If Ollama is not running or unreachable.

    Example:
        answer = generate_answer("What is RAG?", ["RAG stands for..."])
    """
    template = prompt_template or RAG_PROMPT_TEMPLATE
    context = format_context(context_chunks)
    prompt = template.format(context=context, question=question)

    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]
    except Exception as e:
        if _is_connection_error(e):
            raise OllamaConnectionError() from e
        raise


def generate_answer_stream(
    question: str,
    context_chunks: list[str],
    model: str = "llama3.1:8b",
    prompt_template: str | None = None,
) -> Generator[str, None, None]:
    """Stream an answer token-by-token from Ollama.

    Same as generate_answer but yields text chunks as they arrive,
    so the UI can display partial answers while the LLM is still
    generating. Useful for Streamlit or CLI apps.

    Args:
        question: The user's question.
        context_chunks: Relevant text chunks retrieved from the vector store.
        model: The Ollama model to use for generation.
        prompt_template: Custom prompt template with {context} and {question}
            placeholders. Uses RAG_PROMPT_TEMPLATE if not provided.

    Yields:
        Text chunks as the LLM generates them.

    Raises:
        OllamaConnectionError: If Ollama is not running or unreachable.

    Example:
        for token in generate_answer_stream("What is RAG?", ["RAG stands for..."]):
            print(token, end="", flush=True)
    """
    template = prompt_template or RAG_PROMPT_TEMPLATE
    context = format_context(context_chunks)
    prompt = template.format(context=context, question=question)

    try:
        stream = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        for chunk in stream:
            yield chunk["message"]["content"]
    except Exception as e:
        if _is_connection_error(e):
            raise OllamaConnectionError() from e
        raise


def generate_answer_openai(
    question: str,
    context_chunks: list[str],
    model: str = "gpt-4o-mini",
    prompt_template: str | None = None,
) -> str:
    """Generate an answer using OpenAI's API instead of Ollama.

    Only use this if you have an OPENAI_API_KEY set and want cloud-based
    generation. Ollama is the default and works offline.

    Args:
        question: The user's question.
        context_chunks: Relevant text chunks retrieved from the vector store.
        model: The OpenAI model to use.
        prompt_template: Custom prompt template. Uses RAG_PROMPT_TEMPLATE if None.

    Returns:
        The generated answer as a plain string.

    Raises:
        MissingAPIKeyError: If OPENAI_API_KEY is not set.

    Example:
        answer = generate_answer_openai("What is RAG?", ["RAG stands for..."])
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise MissingAPIKeyError("OPENAI_API_KEY")

    from openai import OpenAI  # Cloud LLM API — only imported when explicitly chosen

    template = prompt_template or RAG_PROMPT_TEMPLATE
    client = OpenAI(api_key=api_key)
    context = format_context(context_chunks)
    prompt = template.format(context=context, question=question)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def _is_connection_error(exc: Exception) -> bool:
    """Check if an exception is caused by Ollama being unreachable."""
    error_text = str(exc).lower()
    return any(term in error_text for term in ("connect", "connection", "refused"))
