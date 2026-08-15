# rag-starter

**Your first RAG pipeline. On your own documents. Completely local.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![CI](https://github.com/salahuddinuqaili/rag-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/salahuddinuqaili/rag-starter/actions/workflows/ci.yml)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/salahuddinuqaili/rag-starter/blob/main/notebooks/rag_starter_colab.ipynb)

RAG (Retrieval-Augmented Generation) lets you ask questions about your
own documents using AI — without uploading anything to the cloud. This
repo gives you a working pipeline with no frameworks to learn.

- **Local-first** — your documents never leave your machine
- **Zero cost** — runs on Ollama, no API keys required
- **No frameworks** — plain Python you can read, modify, and learn from
- **Web app included** — FastAPI + React UI with drag-and-drop upload

## Who is this for?

- You have documents (PDFs, notes, research, internal wikis) and want
  an AI that knows *your* content
- You're a PM, analyst, student, or developer learning RAG for the
  first time
- You want to understand how RAG works, not just use a black box

## Quickstart

### Fastest start (browser only, no install)

[![Open in Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/salahuddinuqaili/rag-starter/blob/main/notebooks/rag_starter_colab.ipynb)

Click the badge above. The notebook runs in your browser using Groq's
free API (no credit card needed). No local setup required.

### Local setup

#### Prerequisites

- **Python 3.10+** — [download here](https://python.org)
- **Ollama** — [download here](https://ollama.ai) (free, runs AI models
  locally)
- **Node.js 18+** — [download here](https://nodejs.org) (for the web UI)

#### Option A: Web app (recommended)

```bash
git clone https://github.com/salahuddinuqaili/rag-starter.git
cd rag-starter

# Install
pip install uv               # if you don't have uv yet
uv sync
cd frontend && npm install && cd ..

# Pull AI models (~5 GB first time)
ollama pull llama3.1:8b
ollama pull nomic-embed-text

# Start (two terminals)
uv run uvicorn backend.main:app --reload --port 8000
cd frontend && npm run dev
```

Open [http://localhost:5173](http://localhost:5173). The app walks you
through setup, indexing, and your first question.

#### Option B: CLI quickstart

```bash
git clone https://github.com/salahuddinuqaili/rag-starter.git
cd rag-starter

# macOS / Linux
bash quickstart/install.sh

# Windows (PowerShell)
.\quickstart\install.ps1

# Run the demo
python quickstart/my_first_rag.py
```

#### Already have an OpenAI key?

```bash
export OPENAI_API_KEY=your-key-here    # or $env:OPENAI_API_KEY on Windows
python quickstart/my_first_rag.py
```

See [guides/use-cloud-llm.md](guides/use-cloud-llm.md) for details.

## Use it on YOUR documents

### Web app

Open the web UI and:

1. **Upload files** — drag and drop PDFs, Markdown, or text files
2. **Ask questions** — answers stream in with source citations
3. **Manage collections** — organize documents into separate collections
4. **Browse history** — past conversations persist in the sidebar

### CLI

```bash
# Index your files
python bring-your-own-docs/index_folder.py ./my-documents --verbose

# Ask questions
python bring-your-own-docs/query.py "What does the Q3 report say about revenue?"

# Interactive mode
python bring-your-own-docs/query.py
```

Supports PDF, Markdown, and plain text.

## How does it work?

```
Your documents → Load → Split into chunks → Embed → Store in vector DB
Your question  → Embed → Find similar chunks → Send to LLM → Answer
```

Read the full walkthrough in [how-it-works/](how-it-works/README.md) —
plain English, no jargon. Check the [Glossary](reference/glossary.md)
for any unfamiliar terms.

## Architecture

```
src/               ← Shared RAG library (untouched between CLI and web app)
backend/           ← FastAPI API server (SSE streaming, file upload)
frontend/          ← React 19 + Vite + Tailwind v4
quickstart/        ← First-run scripts and health check
bring-your-own-docs/ ← CLI tools (index, query, legacy Streamlit app)
```

The web app stores data in three places: ChromaDB for vectors
(`./chroma_db/`), SQLite for conversations and collections
(`./rag_starter.db`), and a file system folder for uploads (`./uploads/`).

## Ready for more?

Once you've got the basics working:

- [Improve your results](guides/improve-results.md) — tune chunk size,
  prompts, and retrieval
- [Use a cloud LLM](guides/use-cloud-llm.md) — swap Ollama for OpenAI
  or Groq
- [Use LangChain](guides/use-langchain.md) — rebuild the pipeline with
  a popular framework
- [Use LlamaIndex](guides/use-llamaindex.md) — try the document-indexing
  specialist
- [Add DOCX support](guides/add-docx-support.md) — a great first
  contribution
- [Migrate your vector DB](guides/migrate-vector-db.md) — when to leave
  ChromaDB

## Reference

- [FAQ](reference/faq.md) — Do I need a GPU? Is my data sent to the
  cloud? How many documents can this handle?
- [Troubleshooting](reference/troubleshooting.md) — common errors with
  copy-pasteable fixes
- [Glossary](reference/glossary.md) — plain-English definitions for
  every technical term

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for
guidelines. Look for issues labelled "good first issue" to get started.

## License

MIT — see [LICENSE](LICENSE).
