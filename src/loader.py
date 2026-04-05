"""Load PDF, Markdown, and plain-text files into Document objects."""

import logging
import os
from dataclasses import dataclass, field

import pymupdf4llm  # PDF-to-markdown conversion built on PyMuPDF

logger = logging.getLogger(__name__)


@dataclass
class Document:
    """A single unit of loaded text with its origin metadata.

    Attributes:
        content: The full text extracted from the file.
        metadata: A dict with 'source' (filename) and 'page' (int, 0 for non-PDF).
    """

    content: str
    metadata: dict = field(default_factory=dict)


def load_pdf(path: str) -> list[Document]:
    """Load a PDF file and return one Document per page.

    Uses pymupdf4llm to extract markdown-formatted text from each page,
    which preserves headings and lists better than raw text extraction.

    Args:
        path: Path to the PDF file.

    Returns:
        A list of Document objects, one per page.

    Example:
        docs = load_pdf("report.pdf")
        # docs[0].metadata == {"source": "report.pdf", "page": 1}
    """
    filename = os.path.basename(path)
    pages = pymupdf4llm.to_markdown(path, page_chunks=True)
    documents = []
    for i, page in enumerate(pages):
        text = page["text"] if isinstance(page, dict) else str(page)
        if text.strip():
            documents.append(Document(
                content=text.strip(),
                metadata={"source": filename, "page": i + 1},
            ))
    return documents


def load_markdown(path: str) -> Document:
    """Load a markdown file and return a single Document.

    Args:
        path: Path to the .md file.

    Returns:
        A Document with the full file content and page set to 0.

    Example:
        doc = load_markdown("notes.md")
        # doc.metadata == {"source": "notes.md", "page": 0}
    """
    filename = os.path.basename(path)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return Document(content=content.strip(), metadata={"source": filename, "page": 0})


def load_text(path: str) -> Document:
    """Load a plain-text file and return a single Document.

    Args:
        path: Path to the .txt file.

    Returns:
        A Document with the full file content and page set to 0.

    Example:
        doc = load_text("readme.txt")
    """
    filename = os.path.basename(path)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return Document(content=content.strip(), metadata={"source": filename, "page": 0})


EXTENSION_HANDLERS = {
    ".pdf": load_pdf,
    ".md": load_markdown,
    ".txt": load_text,
}


def load_folder(folder_path: str, verbose: bool = False) -> list[Document]:
    """Recursively load all supported files from a folder.

    Walks the directory tree and loads .pdf, .md, and .txt files.
    Unknown file types are skipped with a warning.

    Args:
        folder_path: Path to the root folder to scan.
        verbose: When True, log each file loaded with its type.

    Returns:
        A flat list of Document objects from all loaded files.

    Example:
        docs = load_folder("./my-docs", verbose=True)
        # [loader] Loaded 3 pages from report.pdf
        # [loader] Loaded 1 file: notes.md
    """
    import time

    start = time.time()
    documents: list[Document] = []
    counts: dict[str, int] = {}

    for root, _dirs, files in os.walk(folder_path):
        for filename in sorted(files):
            filepath = os.path.join(root, filename)
            ext = os.path.splitext(filename)[1].lower()

            if ext not in EXTENSION_HANDLERS:
                logger.warning("[loader] Skipping unsupported file: %s", filename)
                continue

            handler = EXTENSION_HANDLERS[ext]
            result = handler(filepath)

            if isinstance(result, list):
                documents.extend(result)
                counts[ext] = counts.get(ext, 0) + len(result)
                if verbose:
                    logger.info("[loader] Loaded %d pages from %s", len(result), filename)
            else:
                documents.append(result)
                counts[ext] = counts.get(ext, 0) + 1
                if verbose:
                    logger.info("[loader] Loaded 1 file: %s", filename)

    elapsed = time.time() - start
    if verbose:
        parts = [f"{v} {k}" for k, v in counts.items()]
        logger.info("[loader] Loaded %d documents (%s) in %.1fs", len(documents), ", ".join(parts), elapsed)

    return documents
