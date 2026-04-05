"""Send a question plus retrieved context to an LLM and get an answer back."""

import logging
import os
import sys

import ollama  # Local LLM runner — generates answers without cloud APIs

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
) -> str:
    """Send a question with context to Ollama and return the generated answer.

    Formats the RAG prompt template with the provided context and question,
    then calls the local LLM to generate a grounded answer.

    Args:
        question: The user's question.
        context_chunks: Relevant text chunks retrieved from the vector store.
        model: The Ollama model to use for generation.

    Returns:
        The LLM's answer as a plain string.

    Raises:
        SystemExit: If Ollama is not running or unreachable.

    Example:
        answer = generate_answer("What is RAG?", ["RAG stands for..."])
    """
    context = format_context(context_chunks)
    prompt = RAG_PROMPT_TEMPLATE.format(context=context, question=question)

    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]
    except Exception as e:
        if "connect" in str(e).lower() or "connection" in str(e).lower():
            logger.error(
                "Could not connect to Ollama. Is it running? "
                "Start it with: ollama serve"
            )
            sys.exit(1)
        raise


def generate_answer_openai(
    question: str,
    context_chunks: list[str],
    model: str = "gpt-4o-mini",
) -> str:
    """Generate an answer using OpenAI's API instead of Ollama.

    Only use this if you have an OPENAI_API_KEY set and want cloud-based
    generation. Ollama is the default and works offline.

    Args:
        question: The user's question.
        context_chunks: Relevant text chunks retrieved from the vector store.
        model: The OpenAI model to use.

    Returns:
        The generated answer as a plain string.

    Raises:
        SystemExit: If OPENAI_API_KEY is not set.

    Example:
        answer = generate_answer_openai("What is RAG?", ["RAG stands for..."])
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not set. Export it or use Ollama instead.")
        sys.exit(1)

    from openai import OpenAI  # Cloud LLM API — only imported when explicitly chosen

    client = OpenAI(api_key=api_key)
    context = format_context(context_chunks)
    prompt = RAG_PROMPT_TEMPLATE.format(context=context, question=question)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
