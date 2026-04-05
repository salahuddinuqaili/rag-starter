# Loading Documents

[← Back to overview](README.md)

The loading step reads your files — PDFs, markdown, and plain text — and
converts each one into a common format that the rest of the pipeline can work
with.

## Why loading matters

Your documents do not all look the same under the hood. A PDF contains layout
instructions, fonts, and sometimes images. A markdown file mixes text with
formatting symbols like `##` and `**`. A plain text file is just raw
characters. Before you can search across all of them, you need to extract the
actual text and throw away everything else.

Without a loading step, every downstream component would need to know how to
handle every file format. By standardising early, the rest of the pipeline only
deals with one thing: text plus a bit of metadata.

## The Document object

Every loaded file becomes one or more `Document` objects. A Document is
deliberately simple — it has exactly two fields:

- **content** — the extracted text as a plain string.
- **metadata** — a dictionary with `source` (the filename) and `page` (the
  page number, or 0 for non-PDF files).

```python
Document(
    content="Remote teams thrive when communication is async-first...",
    metadata={"source": "remote-work-best-practices.md", "page": 0}
)
```

PDFs produce one Document per page, so a 12-page report becomes 12 Documents.
Markdown and text files each produce a single Document.

## How PDF loading works

PDFs are the trickiest format because they store layout information, not
logical paragraphs. rag-starter uses PyMuPDF (a fast C-based PDF library)
together with pymupdf4llm, which extracts text in a way that is optimised for
feeding into language models. It preserves reading order, strips headers and
footers where possible, and converts tables into readable text.

Scanned PDFs (images of text) are not supported in v0.1 — the PDF must contain
selectable text. If you open the PDF and can highlight words with your cursor,
it will work.

## What happens to formatting

Markdown syntax (`#`, `*`, `-`) is kept as-is because it does not hurt
retrieval and sometimes carries useful structure. PDF formatting (bold, italic,
columns) is discarded — only the text content survives. This is intentional:
embeddings (the next-but-one step) work on meaning, not appearance.

## Loading a folder

In practice, you point the pipeline at a folder rather than individual files.
The loader walks the folder recursively, picks up every `.pdf`, `.md`, and
`.txt` file, and skips anything else with a warning. The result is a flat list
of Documents ready for chunking.

```bash
python bring-your-own-docs/index_folder.py ~/my-docs --verbose
```

With `--verbose` enabled, the loader reports what it found:

```
[loader] Loaded 3 pages from annual-report.pdf
[loader] Loaded 1 file: meeting-notes.md
[loader] Skipped unsupported file: diagram.png
[loader] Loaded 7 documents from 4 files in 0.8s
```

## Next step

Once your documents are loaded into a uniform format, they need to be broken
into smaller pieces. That is [chunking](02-chunking.md).
