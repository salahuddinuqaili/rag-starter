# Bring Your Own Documents

Point this at any folder of PDFs, markdown files, or text files and start
asking questions.

## Index your documents

```bash
python bring-your-own-docs/index_folder.py /path/to/your/folder --verbose
```

This scans your folder, splits documents into chunks, generates embeddings,
and stores everything in a local ChromaDB database at `./chroma_db/`.

## Ask questions

```bash
python bring-your-own-docs/query.py "What does the Q3 report say about revenue?"
```

Or start an interactive session (type questions, get answers, Ctrl+C to quit):

```bash
python bring-your-own-docs/query.py
```

## Launch the web UI

```bash
streamlit run bring-your-own-docs/app.py
```

This opens a browser-based chat interface where you can index documents and
ask questions with a visual interface.

## Supported formats

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Text-based and scanned (via PyMuPDF) |
| Markdown | `.md` | Full content preserved |
| Plain text | `.txt` | Full content preserved |
| Word (DOCX) | `.docx` | Coming soon — see `guides/add-docx-support.md` |

## Options

Both `index_folder.py` and `query.py` support these flags:

- `--verbose` — Show detailed timing for each pipeline stage
- `--db-path ./my_db` — Use a custom database location (default: `./chroma_db`)
- `--chunk-size 500` — Characters per chunk (indexing only)
- `--chunk-overlap 50` — Overlap between chunks (indexing only)
- `--top-k 5` — Number of chunks to retrieve (querying only)
- `--model llama3.1:8b` — LLM model for answer generation (querying only)
