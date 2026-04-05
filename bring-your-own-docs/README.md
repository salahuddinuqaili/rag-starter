# Bring Your Own Documents

Point this at any folder of PDFs, markdown files, or text files and start
asking questions.

## Which tool should I use?

| Tool | Best for | Command |
|------|----------|---------|
| **Web UI** | Visual interface, browsing results | `streamlit run bring-your-own-docs/app.py` |
| **Interactive CLI** | Quick back-and-forth questions | `python bring-your-own-docs/query.py` |
| **One-shot CLI** | Scripting, single questions | `python bring-your-own-docs/query.py "question"` |

If you're not sure, **start with the web UI** — it handles indexing
and querying in one place.

## Index your documents

```bash
# macOS / Linux
python bring-your-own-docs/index_folder.py ./my-documents --verbose

# Windows (PowerShell) — quote paths with spaces
python bring-your-own-docs/index_folder.py "C:\Users\You\Documents\My PDFs" --verbose
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
| Word (DOCX) | `.docx` | Coming soon — see [guides/add-docx-support.md](../guides/add-docx-support.md) |

## Options

Both `index_folder.py` and `query.py` support these flags:

- `--verbose` — Show what each pipeline stage is doing and how long it took
- `--db-path ./my_db` — Use a custom database location (default: `./chroma_db`)
- `--chunk-size 500` — Characters per chunk (indexing only)
- `--chunk-overlap 50` — Overlap between chunks (indexing only)
- `--top-k 5` — Number of chunks to retrieve (querying only)
- `--model llama3.1:8b` — LLM model for answer generation (querying only)

For guidance on tuning these options, see
[guides/improve-results.md](../guides/improve-results.md).

## Troubleshooting

- **"No index found"** — Run `index_folder.py` first before querying.
- **"Could not connect to Ollama"** — Start Ollama with `ollama serve`.
- **Windows path errors** — Use forward slashes (`C:/Users/...`) or quote
  paths with backslashes (`"C:\Users\..."`).
- **More issues** — See [reference/troubleshooting.md](../reference/troubleshooting.md).
