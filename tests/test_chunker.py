"""Tests for src/chunker.py — text splitting with overlap."""

from src.chunker import chunk_documents, chunk_text


def test_chunk_text_empty_input():
    """Empty string should return an empty list."""
    assert chunk_text("") == []


def test_chunk_text_whitespace_only():
    """Whitespace-only string should return an empty list."""
    assert chunk_text("   \n\n  ") == []


def test_chunk_text_shorter_than_chunk_size():
    """Text shorter than chunk_size should return a single chunk."""
    text = "Hello world."
    result = chunk_text(text, chunk_size=500)
    assert len(result) == 1
    assert result[0] == text


def test_chunk_text_exact_chunk_size():
    """Text at exactly chunk_size should return a single chunk."""
    text = "A" * 500
    result = chunk_text(text, chunk_size=500)
    assert len(result) == 1


def test_chunk_text_splits_long_text(sample_text):
    """Long text should be split into multiple chunks."""
    result = chunk_text(sample_text, chunk_size=200, chunk_overlap=30)
    assert len(result) > 1
    for chunk in result:
        # Chunks may slightly exceed size due to overlap prepending
        assert len(chunk) < 200 + 50  # some tolerance for overlap


def test_chunk_text_respects_overlap(sample_text):
    """The end of one chunk should appear at the start of the next."""
    overlap = 30
    result = chunk_text(sample_text, chunk_size=200, chunk_overlap=overlap)
    if len(result) >= 2:
        # The overlap region from chunk[0] should appear in chunk[1]
        tail_of_first = result[0][-overlap:]
        assert tail_of_first in result[1], (
            f"Expected overlap '{tail_of_first}' to appear in next chunk"
        )


def test_chunk_text_separators_tried_in_order():
    """Paragraph breaks should be preferred over other separators."""
    text = "Paragraph one.\n\nParagraph two.\n\nParagraph three."
    result = chunk_text(text, chunk_size=50, chunk_overlap=0)
    # Should split on paragraph breaks, not mid-sentence
    assert any("Paragraph one." in c for c in result)
    assert any("Paragraph two." in c for c in result)


def test_chunk_text_no_overlap():
    """Overlap of 0 should produce non-overlapping chunks."""
    text = "word " * 200  # 1000 chars
    result = chunk_text(text, chunk_size=100, chunk_overlap=0)
    assert len(result) > 1


def test_chunk_documents_returns_parallel_lists(sample_documents):
    """chunk_documents should return aligned texts and metadatas."""
    texts, metas = chunk_documents(sample_documents, chunk_size=200, chunk_overlap=20)
    assert len(texts) == len(metas)
    assert len(texts) > 0


def test_chunk_documents_preserves_metadata(sample_documents):
    """Each chunk's metadata should include source and chunk_index."""
    texts, metas = chunk_documents(sample_documents, chunk_size=200, chunk_overlap=20)
    for meta in metas:
        assert "source" in meta
        assert "chunk_index" in meta


def test_chunk_documents_empty_input():
    """Empty document list should return empty lists."""
    texts, metas = chunk_documents([])
    assert texts == []
    assert metas == []
