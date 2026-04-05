"""Split text into overlapping chunks using a recursive character splitter."""

import logging

from src.loader import Document

logger = logging.getLogger(__name__)

# Separators tried in order — we prefer natural break points so chunks
# stay semantically coherent. Paragraph breaks are best, then line breaks,
# then sentences, then words, then individual characters as a last resort.
SEPARATORS = ["\n\n", "\n", ". ", " ", ""]


def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[str]:
    """Split text into overlapping chunks, preserving natural boundaries.

    Tries paragraph breaks first, then line breaks, then sentences, then
    words, and finally individual characters. This keeps chunks readable
    and semantically meaningful.

    Args:
        text: The text to split.
        chunk_size: Maximum number of characters per chunk.
        chunk_overlap: Number of characters to repeat between consecutive
            chunks so context isn't lost at boundaries.

    Returns:
        A list of text chunks. Empty list for empty input, single-element
        list if the text is shorter than chunk_size.

    Example:
        chunks = chunk_text("Hello world. This is a test.", chunk_size=15, chunk_overlap=5)
    """
    if not text or not text.strip():
        return []

    text = text.strip()

    if len(text) <= chunk_size:
        return [text]

    return _recursive_split(text, chunk_size, chunk_overlap, SEPARATORS)


def _recursive_split(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
    separators: list[str],
) -> list[str]:
    """Recursively split text trying each separator in order.

    We try the highest-quality separator first (paragraph break). If the
    resulting pieces are still too large, we recurse with the next separator.
    """
    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    separator = separators[0]
    remaining_separators = separators[1:]

    # Character-level fallback — just slice at chunk_size
    if separator == "":
        return _split_by_characters(text, chunk_size, chunk_overlap)

    pieces = text.split(separator)

    chunks: list[str] = []
    current = ""

    for piece in pieces:
        candidate = (current + separator + piece) if current else piece

        if len(candidate) <= chunk_size:
            current = candidate
        else:
            # Flush what we have so far
            if current:
                chunks.append(current.strip())
            # If this single piece is too big, split it with the next separator
            if len(piece) > chunk_size and remaining_separators:
                sub_chunks = _recursive_split(piece, chunk_size, chunk_overlap, remaining_separators)
                chunks.extend(sub_chunks)
                current = ""
            else:
                current = piece

    if current.strip():
        chunks.append(current.strip())

    # Apply overlap — prepend the tail of the previous chunk to the next
    if chunk_overlap > 0 and len(chunks) > 1:
        chunks = _apply_overlap(chunks, chunk_overlap)

    return chunks


def _split_by_characters(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Last-resort split: slice text at fixed character intervals with overlap."""
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks


def _apply_overlap(chunks: list[str], overlap: int) -> list[str]:
    """Prepend the last `overlap` characters of each chunk to the next chunk."""
    result = [chunks[0]]
    for i in range(1, len(chunks)):
        prev_tail = chunks[i - 1][-overlap:]
        # Only add overlap if the chunk doesn't already start with it
        if not chunks[i].startswith(prev_tail):
            result.append(prev_tail + chunks[i])
        else:
            result.append(chunks[i])
    return result


def chunk_documents(
    docs: list[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> tuple[list[str], list[dict]]:
    """Chunk all documents and return parallel lists of texts and metadata.

    Each chunk inherits the metadata of its source document, with an added
    'chunk_index' field so you can trace it back.

    Args:
        docs: List of Document objects to chunk.
        chunk_size: Maximum characters per chunk.
        chunk_overlap: Characters of overlap between consecutive chunks.

    Returns:
        A tuple of (chunk_texts, chunk_metadatas) where both lists have
        the same length. Each metadata dict has the original source info
        plus a 'chunk_index' key.

    Example:
        texts, metas = chunk_documents(my_docs, chunk_size=300)
        # metas[0] == {"source": "report.pdf", "page": 1, "chunk_index": 0}
    """
    all_texts: list[str] = []
    all_metadatas: list[dict] = []

    for doc in docs:
        chunks = chunk_text(doc.content, chunk_size, chunk_overlap)
        for i, chunk in enumerate(chunks):
            all_texts.append(chunk)
            all_metadatas.append({**doc.metadata, "chunk_index": i})

    return all_texts, all_metadatas
