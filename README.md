# rag-starter

**Your first RAG pipeline. Running in 15 minutes. On your own documents.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
<!-- TODO: Add stars badge after first push -->
<!-- TODO: Add Open in Colab badge -->

Build a working Retrieval-Augmented Generation pipeline on your own
documents — local, free, and no frameworks to learn.

- **Local-first** — your documents never leave your machine
- **Zero cost** — runs on Ollama, no API keys required
- **15 minutes** — from clone to asking questions about your files

<!-- TODO: Add demo GIF -->

## Quickstart

Choose your path:

### Option A: Google Colab (zero install)

<!-- TODO: Add Colab badge link -->
Open `notebooks/rag_starter_colab.ipynb` in Colab — uses Groq's free API
so you don't need Ollama or a GPU.

### Option B: Local (recommended)

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

### Option C: Cloud LLM

Already have an OpenAI key? Set it and go:

```bash
export OPENAI_API_KEY=your-key-here
python quickstart/my_first_rag.py
```

See [guides/use-cloud-llm.md](guides/use-cloud-llm.md) for details.

## Use it on YOUR documents

### Step 1: Index your files

```bash
python bring-your-own-docs/index_folder.py /path/to/your/folder --verbose
```

Supports PDF, Markdown, and plain text. Your files are processed locally
and stored in a ChromaDB database at `./chroma_db/`.

### Step 2: Ask questions

```bash
python bring-your-own-docs/query.py "What does the Q3 report say about revenue?"
```

Or launch the web UI:

```bash
streamlit run bring-your-own-docs/app.py
```

## How does it work?

RAG works in five steps: load your documents, split them into chunks,
convert chunks into numerical embeddings, store those embeddings in a
vector database, then retrieve the most relevant chunks when you ask a
question.

Read the full walkthrough in [how-it-works/](how-it-works/README.md) —
each step gets a plain-English explainer with no jargon.

## Ready for more?

Once you've got the basics working, these guides show you how to level up:

- [Use a cloud LLM](guides/use-cloud-llm.md) — swap Ollama for OpenAI
  or Groq
- [Improve your results](guides/improve-results.md) — tune chunk size,
  overlap, top-k, and prompts
- [Use LangChain](guides/use-langchain.md) — rebuild the pipeline with
  a popular framework
- [Use LlamaIndex](guides/use-llamaindex.md) — try the document-indexing
  specialist
- [Add DOCX support](guides/add-docx-support.md) — a great first
  contribution
- [Migrate your vector DB](guides/migrate-vector-db.md) — when to leave
  ChromaDB

## FAQ

See [reference/faq.md](reference/faq.md) for answers to common questions:
Do I need a GPU? Is my data sent to the cloud? How many documents can
this handle?

Having trouble? Check [reference/troubleshooting.md](reference/troubleshooting.md).

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for
guidelines. Look for issues labelled "good first issue" to get started.

## License

MIT — see [LICENSE](LICENSE).
