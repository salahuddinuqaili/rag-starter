# rag-starter

**Your first RAG pipeline. On your own documents. Completely local.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-42%20passing-brightgreen.svg)](tests/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/salahuddinuqaili/rag-starter/blob/main/notebooks/rag_starter_colab.ipynb)

RAG (Retrieval-Augmented Generation) lets you ask questions about your
own documents using AI — without uploading anything to the cloud. This
repo gives you a working pipeline with no frameworks to learn.

- **Local-first** — your documents never leave your machine
- **Zero cost** — runs on Ollama, no API keys required
- **No frameworks** — plain Python you can read, modify, and learn from

## Who is this for?

- You have documents (PDFs, notes, research, internal wikis) and want
  an AI that knows *your* content
- You're a PM, analyst, student, or developer learning RAG for the
  first time
- You want to understand how RAG works, not just use a black box

## See it in action

<!-- TODO: Replace with actual demo GIF once recorded -->
```
$ python quickstart/my_first_rag.py

============================================================
  rag-starter: Your First RAG Pipeline
============================================================

Step 1: Indexing sample documents...
Indexed 6 files → 42 chunks in 3.2s

Step 2: Asking questions across your documents...

------------------------------------------------------------
Question: What are the best practices for async communication in remote teams?

Answer: Teams should default to async methods like written updates and shared
documents rather than scheduling meetings. When meetings are necessary, always
circulate an agenda beforehand and share notes within 24 hours.

Sources: remote-work-best-practices.md
```

## Quickstart

### Fastest start (browser only, no install)

[![Open in Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/salahuddinuqaili/rag-starter/blob/main/notebooks/rag_starter_colab.ipynb)

Click the badge above. The notebook runs in your browser using Groq's
free API (no credit card needed). No local setup required.

### Local setup

#### Prerequisites

- **Python 3.10+** — [download here](https://python.org) if you don't
  have it
- **Ollama** — [download here](https://ollama.ai) (free, runs AI models
  locally on your machine). Install this first — the setup script needs
  it.

#### Install and run

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

The install script creates a virtual environment, installs dependencies,
and pulls the required AI models (~5 GB on first run). First-time setup
takes about 10-15 minutes depending on your internet speed.

> **Windows note:** If you close your terminal, reactivate the virtual
> environment before running commands: `.venv\Scripts\Activate.ps1`

#### Already have an OpenAI key?

```bash
# macOS / Linux
export OPENAI_API_KEY=your-key-here

# Windows (PowerShell)
$env:OPENAI_API_KEY="your-key-here"

python quickstart/my_first_rag.py
```

See [guides/use-cloud-llm.md](guides/use-cloud-llm.md) for details.

## Use it on YOUR documents

### Step 1: Index your files

```bash
# macOS / Linux
python bring-your-own-docs/index_folder.py ./my-documents --verbose

# Windows — quote paths with spaces
python bring-your-own-docs/index_folder.py "C:\Users\You\Documents\My PDFs" --verbose
```

Supports PDF, Markdown, and plain text. Your files are processed locally
and stored in a ChromaDB database at `./chroma_db/`.

### Step 2: Ask questions

```bash
python bring-your-own-docs/query.py "What does the Q3 report say about revenue?"
```

Or start an interactive session:

```bash
python bring-your-own-docs/query.py
```

Or launch the web UI:

```bash
streamlit run bring-your-own-docs/app.py
```

## How does it work?

```
Your documents → Load → Split into chunks → Embed → Store in vector DB
Your question  → Embed → Find similar chunks → Send to LLM → Answer
```

Read the full walkthrough in [how-it-works/](how-it-works/README.md) —
plain English, no jargon. Check the [Glossary](reference/glossary.md)
for any unfamiliar terms.

## Ready for more?

Once you've got the basics working:

- [Improve your results](guides/improve-results.md) — tune chunk size,
  prompts, and retrieval with copy-pasteable experiments
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
