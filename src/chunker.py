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
        chunk_size: Maximum number of characters per chunk. Must be > 0.
        chunk_overlap: Number of characters to repeat between consecutive
            chunks so context isn't lost at boundaries. Must be < chunk_size.

    Returns:
        A list of text chunks. Empty list for empty input, single-element
        list if the text is shorter than chunk_size.

    Raises:
        ValueError: If chunk_overlap >= chunk_size or either is <= 0.

    Example:
        chunks = chunk_text("Hello world. This is a test.", chunk_size=15, chunk_overlap=5)
    """
    if chunk_size <= 0:
        raise ValueError(f"chunk_size must be > 0, got {chunk_size}")
    if chunk_overlap < 0:
        raise ValueError(f"chunk_overlap must be >= 0, got {chunk_overlap}")
    if chunk_overlap >= chunk_size:
        raise ValueError(
            f"chunk_overlap ({chunk_overlap}) must be < chunk_size ({chunk_size})"
        )

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
    _is_top_level: bool = True,
) -> list[str]:
    """Recursively split text trying each separator in order.

    We try the highest-quality separator first (paragraph break). If the
    resulting pieces are still too large, we recurse with the next separator.
    Overlap is only applied at the top level to avoid compounding.
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
                sub_chunks = _recursive_split(
                    piece, chunk_size, chunk_overlap, remaining_separators,
                    _is_top_level=False,
                )
                chunks.extend(sub_chunks)
                current = ""
            else:
                current = piece

    if current.strip():
        chunks.append(current.strip())

    # Only apply overlap at the top level so it doesn't compound
    # through multiple recursion depths
    if _is_top_level and chunk_overlap > 0 and len(chunks) > 1:
        chunks = _apply_overlap(chunks, chunk_overlap)

    return chunks


def _split_by_characters(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Last-resort split: slice text at fixed character intervals with overlap."""
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        # Step forward by (chunk_size - overlap) so consecutive chunks share
        # their tail/head, preserving context at the boundary.
        start += chunk_size - chunk_overlap
    return chunks


def _apply_overlap(chunks: list[str], overlap: int) -> list[str]:
    """Prepend the last `overlap` characters of each chunk to the next chunk.

    Always prepend — the previous implementation skipped overlap when the
    next chunk coincidentally started with the same characters, which was
    a bug. Unconditional prepend is correct because the overlap serves as
    a context bridge regardless of content similarity.
    """
    result = [chunks[0]]
    for i in range(1, len(chunks)):
        prev_tail = chunks[i - 1][-overlap:]
        result.append(prev_tail + chunks[i])
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
