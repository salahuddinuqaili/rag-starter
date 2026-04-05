"""Tests for src/loader.py — file loading and folder scanning."""

import os

from src.loader import Document, load_folder, load_markdown, load_text


def test_load_markdown_from_sample_docs():
    """Load a real markdown file from sample-docs/ and verify structure."""
    # Use any file that will exist after Phase 5
    path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "sample-docs", "what-is-rag.md"
    )
    if not os.path.exists(path):
        # Create a minimal test file if sample-docs doesn't exist yet
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("# What is RAG?\n\nRAG stands for Retrieval-Augmented Generation.")

    doc = load_markdown(path)
    assert isinstance(doc, Document)
    assert doc.content
    assert doc.metadata["source"] == "what-is-rag.md"
    assert doc.metadata["page"] == 0


def test_load_text_file(tmp_path):
    """Load a plain text file and verify content and metadata."""
    test_file = tmp_path / "notes.txt"
    test_file.write_text("These are some test notes.", encoding="utf-8")

    doc = load_text(str(test_file))
    assert doc.content == "These are some test notes."
    assert doc.metadata["source"] == "notes.txt"
    assert doc.metadata["page"] == 0


def test_load_folder_mixed_types(tmp_path):
    """load_folder should handle a mix of .md and .txt files."""
    (tmp_path / "readme.md").write_text("# Hello", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("Some notes", encoding="utf-8")

    docs = load_folder(str(tmp_path))
    assert len(docs) == 2
    sources = {d.metadata["source"] for d in docs}
    assert "readme.md" in sources
    assert "notes.txt" in sources


def test_load_folder_empty_directory(tmp_path):
    """load_folder on an empty directory should return an empty list."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    docs = load_folder(str(empty_dir))
    assert docs == []


def test_load_folder_skips_unknown_extensions(tmp_path):
    """load_folder should skip unsupported file types without crashing."""
    (tmp_path / "data.csv").write_text("a,b,c", encoding="utf-8")
    (tmp_path / "readme.md").write_text("# Test", encoding="utf-8")

    docs = load_folder(str(tmp_path))
    assert len(docs) == 1
    assert docs[0].metadata["source"] == "readme.md"


def test_load_folder_recursive(tmp_path):
    """load_folder should walk subdirectories."""
    sub = tmp_path / "subdir"
    sub.mkdir()
    (sub / "deep.md").write_text("# Deep file", encoding="utf-8")
    (tmp_path / "top.txt").write_text("Top level", encoding="utf-8")

    docs = load_folder(str(tmp_path))
    assert len(docs) == 2
    sources = {d.metadata["source"] for d in docs}
    assert "deep.md" in sources
    assert "top.txt" in sources


def test_load_folder_verbose(tmp_path, caplog):
    """Verbose mode should log file loading info."""
    (tmp_path / "test.md").write_text("# Test", encoding="utf-8")

    import logging
    with caplog.at_level(logging.INFO):
        load_folder(str(tmp_path), verbose=True)

    assert any("loader" in record.message.lower() for record in caplog.records)


def test_document_dataclass():
    """Document should be a proper dataclass with defaults."""
    doc = Document(content="test")
    assert doc.content == "test"
    assert doc.metadata == {}
