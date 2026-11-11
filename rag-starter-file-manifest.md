# rag-starter — File Manifest for Claude Code

> **Target directory:** `C:\Users\mulli\projects\rag-starter`
> **Total files:** 47
> **Priority:** Files are tagged P0 (launch-blocking), P1 (launch day), P2 (week 1 post-launch)

---

## CLAUDE.md Instructions

Before creating any files, Claude Code should create a `CLAUDE.md` at the repo root with these project rules:

```
# CLAUDE.md — rag-starter

## Project Identity
- Name: rag-starter
- Tagline: "Your first RAG pipeline. Running in 15 minutes. On your own documents."
- Audience: Non-engineers (PMs, analysts, writers, students) new to RAG
- License: MIT

## Stack (locked for v0.1)
- Python 3.10+
- Ollama (llama3.1:8b for LLM, nomic-embed-text for embeddings)
- ChromaDB (vector store, pip install, no Docker)
- PyMuPDF / pymupdf4llm (PDF loading)
- Streamlit (UI)
- NO LangChain, NO LlamaIndex, NO Docker in the default path

## Code Rules
- Every Python file must be < 150 lines (excluding comments)
- Every function must have a docstring explaining what it does in plain English
- All scripts support a --verbose flag that prints each RAG pipeline stage
- No classes unless absolutely necessary — prefer functions
- Use type hints throughout
- requirements.txt pins major versions only (e.g., chromadb>=0.5,<1.0)
- All imports at the top of the file, stdlib first, then third-party, then local

## Writing Rules
- No jargon without a plain-English explanation in parentheses
- First sentence of every README answers "what does this do?"
- Use second person ("you") not third person ("the user")
- Code blocks must be copy-pasteable (include the full command, not fragments)
- Every markdown file starts with a single H1, never skip heading levels

## Testing
- Tests use pytest
- Test files mirror source structure: quickstart/check.py → tests/test_check.py
- Tests must run without Ollama installed (mock the LLM calls)

## Git
- Commit messages: imperative mood, <72 chars, e.g. "Add health check script"
- Branch naming: feature/short-description, fix/short-description
- No generated files committed (chroma_db/, __pycache__/, .ipynb_checkpoints/)
```

---

## File Manifest

### Root Files

| # | Path | Priority | Purpose | Content Notes |
|---|---|---|---|---|
| 1 | `CLAUDE.md` | P0 | Claude Code project rules | See above |
| 2 | `README.md` | P0 | The product — first thing visitors see | Follow the README strategy from the v2 plan. Three-path quickstart (Colab / Local / Cloud). GIF placeholder. Badges. |
| 3 | `LICENSE` | P0 | MIT license | Standard MIT license text with current year and "rag-starter contributors" |
| 4 | `CONTRIBUTING.md` | P1 | How to contribute | Issue-first workflow. Code style rules. "Good first issues" section. Link to beginner_question issue template. |
| 5 | `CHANGELOG.md` | P1 | Release history | Start with `## [0.1.0] - Unreleased` section with initial feature list |
| 6 | `.gitignore` | P0 | Files to exclude from git | Python defaults + `chroma_db/`, `.env`, `__pycache__/`, `*.pyc`, `.ipynb_checkpoints/`, `indexed_data/` |
| 7 | `.env.example` | P0 | Template for environment variables | `OPENAI_API_KEY=your-key-here` (commented out, optional) |

---

### quickstart/

| # | Path | Priority | Purpose | Content Notes |
|---|---|---|---|---|
| 8 | `quickstart/requirements.txt` | P0 | Python dependencies | `chromadb>=0.5,<1.0`, `pymupdf>=1.24`, `pymupdf4llm>=0.0.10`, `ollama>=0.3`, `streamlit>=1.35`, `python-dotenv>=1.0` |
| 9 | `quickstart/install.sh` | P0 | One-command setup (macOS/Linux) | Check Python version, create venv, pip install, pull Ollama models (llama3.1:8b + nomic-embed-text), run check.py |
| 10 | `quickstart/install.ps1` | P0 | One-command setup (Windows) | PowerShell equivalent of install.sh. Must handle Windows paths and venv activation syntax. |
| 11 | `quickstart/check.py` | P0 | Health check | Print checklist: ✓/✗ Python version, ✓/✗ pip packages installed, ✓/✗ Ollama running, ✓/✗ LLM model available, ✓/✗ embedding model available. Exit with clear error message if anything fails. |
| 12 | `quickstart/my_first_rag.py` | P0 | First RAG experience (<80 lines) | Load sample-docs/, chunk them, embed with nomic-embed-text, store in ChromaDB, ask 3 pre-written questions, print answers with source file references. Support `--verbose` flag. Include `expected_output` comment block at bottom showing what success looks like. |

---

### bring-your-own-docs/

| # | Path | Priority | Purpose | Content Notes |
|---|---|---|---|---|
| 13 | `bring-your-own-docs/README.md` | P0 | Instructions for using your own files | "Point this at any folder of documents and start asking questions." Three steps: index, query, launch UI. Supported formats: PDF, MD, TXT. |
| 14 | `bring-your-own-docs/index_folder.py` | P0 | Index a local folder | CLI script: `python index_folder.py /path/to/folder`. Walks directory recursively, loads PDF (pymupdf4llm), MD, and TXT files. Chunks, embeds, stores in ChromaDB under `./chroma_db/`. Prints progress: "Indexed 42 chunks from 7 files." Support `--verbose`, `--chunk-size`, `--chunk-overlap` flags. |
| 15 | `bring-your-own-docs/query.py` | P0 | CLI query interface | `python query.py "What were the key decisions?"`. Retrieves top-k chunks, passes to Ollama, prints answer + source references (filename, chunk excerpt). Support `--top-k`, `--verbose`, `--model` flags. |
| 16 | `bring-your-own-docs/app.py` | P0 | Streamlit UI | Single-file Streamlit app. Sidebar: folder path input + "Index" button + settings (chunk size, top-k). Main area: chat-style Q&A with source references shown in expandable sections. Must import shared functions from a common module — do NOT duplicate RAG logic. |

---

### src/ (shared module — NEW addition not in v2 plan)

The v2 plan didn't have a shared module, but bring-your-own-docs/app.py, bring-your-own-docs/query.py, bring-your-own-docs/index_folder.py, and quickstart/my_first_rag.py all need the same RAG functions. Without a shared module, we'd duplicate code across 4 files.

| # | Path | Priority | Purpose | Content Notes |
|---|---|---|---|---|
| 17 | `src/__init__.py` | P0 | Package init | Empty or single-line version: `__version__ = "0.1.0"` |
| 18 | `src/loader.py` | P0 | Document loading | Functions: `load_pdf(path) → str`, `load_markdown(path) → str`, `load_text(path) → str`, `load_folder(path) → list[Document]`. Document is a simple dataclass: `{content: str, metadata: {source: str, page: int}}`. No class hierarchy — just functions. |
| 19 | `src/chunker.py` | P0 | Text splitting | Function: `chunk_text(text, chunk_size=500, chunk_overlap=50) → list[str]`. Recursive character splitter implemented from scratch (~50 lines). Split on `\n\n`, then `\n`, then `. `, then ` `. Every split point explained in comments. |
| 20 | `src/embedder.py` | P0 | Embedding generation | Function: `embed_texts(texts: list[str], model="nomic-embed-text") → list[list[float]]`. Uses Ollama Python client. Includes fallback error message if Ollama isn't running. |
| 21 | `src/store.py` | P0 | Vector store operations | Functions: `create_store(path="./chroma_db") → ChromaDB client`, `add_documents(store, chunks, embeddings, metadatas)`, `query_store(store, query_embedding, top_k=5) → results`. Thin wrapper around ChromaDB. |
| 22 | `src/generator.py` | P0 | LLM response generation | Function: `generate_answer(query, context_chunks, model="llama3.1:8b") → str`. Builds a RAG prompt (query + retrieved context), sends to Ollama, returns response. The prompt template is visible and editable (not hidden in a framework). |
| 23 | `src/pipeline.py` | P0 | End-to-end orchestration | Functions: `index_documents(folder_path, db_path, verbose=False)`, `query_documents(question, db_path, verbose=False) → Answer`. Wires together loader → chunker → embedder → store → generator. The `verbose` flag prints each stage with timing. |

---

### how-it-works/

| # | Path | Priority | Purpose | Content Notes |
|---|---|---|---|---|
| 24 | `how-it-works/README.md` | P0 | Pipeline overview | "RAG in 5 steps" — one paragraph per step with a link to the detailed page. Include a text-based pipeline diagram (ASCII art or mermaid-compatible). |
| 25 | `how-it-works/01-loading.md` | P1 | Document loading explained | What happens when you feed a PDF to the pipeline. How PyMuPDF extracts text. What metadata is preserved. ~300 words. |
| 26 | `how-it-works/02-chunking.md` | P1 | Chunking explained | Why we split documents (LLMs have limited context, smaller chunks = more precise retrieval). How chunk size and overlap work. Visual example: a paragraph split into overlapping chunks. ~400 words. |
| 27 | `how-it-works/03-embedding.md` | P1 | Embeddings explained | "Think of embeddings as GPS coordinates for meaning." Two sentences that are similar get coordinates close together. No math — just intuition. Mention that nomic-embed-text outputs 768 numbers per chunk. ~350 words. |
| 28 | `how-it-works/04-retrieval.md` | P1 | Retrieval explained | How the query gets embedded, then ChromaDB finds the closest chunks by cosine similarity. What top-k means. Why retrieval quality matters more than LLM quality. ~350 words. |
| 29 | `how-it-works/05-generation.md` | P1 | Generation explained | How the LLM receives the query + retrieved chunks as context. The RAG prompt template (show it in full). Why this reduces hallucination. ~300 words. |

---

### guides/

| # | Path | Priority | Purpose | Content Notes |
|---|---|---|---|---|
| 30 | `guides/use-cloud-llm.md` | P1 | Swap Ollama for OpenAI/Anthropic | Show the 3-line code change. Explain cost implications (~$0.01 per query for gpt-4o-mini). Mention when cloud makes sense vs. local. |
| 31 | `guides/improve-results.md` | P1 | Practical tuning guide | 5 knobs to turn: chunk size, chunk overlap, top-k, prompt template, embedding model. Each with a "try this" experiment and expected impact. |
| 32 | `guides/use-langchain.md` | P2 | Rebuild with LangChain | Same pipeline, rebuilt using LangChain abstractions. Side-by-side comparison: "our code" vs "LangChain equivalent." Explain when the framework helps (complex chains, agent loops) and when it doesn't (simple Q&A). |
| 33 | `guides/use-llamaindex.md` | P2 | Rebuild with LlamaIndex | Same approach as use-langchain.md but for LlamaIndex. Highlight LlamaIndex's strength in document indexing. |
| 34 | `guides/add-docx-support.md` | P2 | Extend loader for Word docs | Add `python-docx` to requirements, add `load_docx()` to loader.py. ~15 minutes of work, good first contribution. |
| 35 | `guides/migrate-vector-db.md` | P2 | Outgrowing ChromaDB | When to migrate (>100k documents, need cloud hosting, need filtering). Step-by-step for Qdrant (Docker) and Pinecone (cloud). |

---

### notebooks/

| # | Path | Priority | Purpose | Content Notes |
|---|---|---|---|---|
| 36 | `notebooks/rag_starter_colab.ipynb` | P0 | Zero-install Colab notebook | Uses OpenAI or Groq (free tier) since Ollama can't run in Colab. Cells: install deps → load sample text → chunk → embed → store in ChromaDB → query → "try your own text" cell. Badge at top: "Open in Colab". Every cell has markdown explanation above it. |
| 37 | `notebooks/rag_starter_local.ipynb` | P1 | Jupyter version of local pipeline | Same flow as quickstart but in notebook format. Uses Ollama locally. For users who prefer notebooks over scripts. |

---

### sample-docs/

Original content written specifically for this repo (no licensing issues). Each file is 300-600 words — long enough to chunk meaningfully, short enough to index in seconds.

| # | Path | Priority | Purpose | Content Notes |
|---|---|---|---|---|
| 38 | `sample-docs/README.md` | P0 | Explains the sample docs | "These are original documents written for rag-starter. They cover diverse topics so you can test retrieval across different subjects. Licensed CC0 (public domain)." |
| 39 | `sample-docs/remote-work-best-practices.md` | P0 | Sample doc: remote work | ~500 words covering async communication, meeting discipline, documentation culture, home office setup. Written as an internal company guide. |
| 40 | `sample-docs/project-management-fundamentals.md` | P0 | Sample doc: project management | ~500 words covering scope, timeline, stakeholders, risk management, agile vs waterfall tradeoffs. Written as a training document. |
| 41 | `sample-docs/intro-to-machine-learning.md` | P0 | Sample doc: ML basics | ~500 words covering supervised vs unsupervised learning, training data, overfitting, real-world applications. Written as a beginner explainer. |
| 42 | `sample-docs/healthy-eating-guide.md` | P0 | Sample doc: nutrition | ~400 words covering macronutrients, meal planning, hydration, common myths. Written as a wellness guide. |
| 43 | `sample-docs/berlin-travel-guide.md` | P0 | Sample doc: Berlin travel | ~500 words covering neighbourhoods, transport, food, culture, tips. Written as a personal travel blog post. Personal touch — gives retrieval something distinctive to find. |
| 44 | `sample-docs/what-is-rag.md` | P0 | Sample doc: RAG itself | ~400 words explaining RAG in plain English. Meta: the tool can answer questions about itself. Good for demo moments. |

---

### reference/

| # | Path | Priority | Purpose | Content Notes |
|---|---|---|---|---|
| 45 | `reference/glossary.md` | P0 | RAG jargon → plain English | 25 terms max. Each entry: **Term** — one-sentence definition — one-sentence analogy. Terms: RAG, embedding, vector, vector store, chunk, chunking, overlap, top-k, cosine similarity, LLM, context window, token, hallucination, retrieval, generation, augmentation, prompt, prompt template, inference, model, fine-tuning, semantic search, keyword search, hybrid search, reranking. |
| 46 | `reference/troubleshooting.md` | P1 | Top 10 issues | "Ollama not found" → install instructions. "Model not found" → pull command. "ChromaDB permission error" → path fix. "Empty results" → check indexing. "Slow responses" → smaller model or cloud LLM. Etc. |
| 47 | `reference/faq.md` | P1 | Common questions | "Do I need a GPU?" "Is my data sent to the cloud?" "Can I use this at work?" "How much does it cost?" "What file types are supported?" "How is this different from ChatGPT?" ~10 questions. |

---

### tests/

| # | Path | Priority | Purpose | Content Notes |
|---|---|---|---|---|
| 48 | `tests/__init__.py` | P1 | Package init | Empty |
| 49 | `tests/test_check.py` | P1 | Test health check | Mock subprocess calls to Ollama. Verify check.py returns correct status for each dependency. |
| 50 | `tests/test_chunker.py` | P1 | Test text splitting | Test with known inputs: verify chunk sizes, overlap, edge cases (empty string, single paragraph, very long text). |
| 51 | `tests/test_loader.py` | P1 | Test document loading | Test markdown loading with sample-docs. Mock PDF loading (don't require actual PDF in tests). |
| 52 | `tests/test_retrieval.py` | P1 | Test retrieval pipeline | Create a small ChromaDB with known content, query it, verify relevant chunks are returned. Mock the Ollama embedding call. |
| 53 | `tests/conftest.py` | P1 | Shared test fixtures | Fixtures: `sample_text`, `sample_chunks`, `mock_embeddings`, `temp_chroma_db` (tmpdir-based). |

---

### .github/

| # | Path | Priority | Purpose | Content Notes |
|---|---|---|---|---|
| 54 | `.github/workflows/ci.yml` | P1 | CI pipeline | Python 3.10 + 3.12. Install deps. Run pytest (without Ollama — tests must mock). Lint with ruff. |
| 55 | `.github/ISSUE_TEMPLATE/bug_report.md` | P1 | Bug report template | Fields: OS, Python version, Ollama version, steps to reproduce, expected vs actual, error output. |
| 56 | `.github/ISSUE_TEMPLATE/workflow_request.md` | P1 | Feature request | "I want to use RAG for [use case]. My documents are [format]. My goal is [outcome]." |
| 57 | `.github/ISSUE_TEMPLATE/beginner_question.md` | P1 | Low-barrier questions | "No question is too basic. We're here to help." Fields: what are you trying to do, what happened, what did you expect. |
| 58 | `.github/PULL_REQUEST_TEMPLATE.md` | P1 | PR template | Checklist: tests pass, docs updated, follows CLAUDE.md code rules, tested on fresh venv. |

---

## Execution Order for Claude Code

Claude Code should create files in this order to maintain valid imports and testability:

### Phase 1: Skeleton (create all directories + root files)
1. `CLAUDE.md`
2. `.gitignore`
3. `.env.example`
4. `LICENSE`
5. All `__init__.py` files
6. `quickstart/requirements.txt`

### Phase 2: Core module (src/)
7. `src/loader.py`
8. `src/chunker.py`
9. `src/embedder.py`
10. `src/store.py`
11. `src/generator.py`
12. `src/pipeline.py`

### Phase 3: Quickstart
13. `quickstart/check.py`
14. `quickstart/my_first_rag.py`
15. `quickstart/install.sh`
16. `quickstart/install.ps1`

### Phase 4: Bring your own docs
17. `bring-your-own-docs/index_folder.py`
18. `bring-your-own-docs/query.py`
19. `bring-your-own-docs/app.py`
20. `bring-your-own-docs/README.md`

### Phase 5: Content
21. All `sample-docs/*.md` files
22. All `how-it-works/*.md` files
23. `reference/glossary.md`
24. `reference/faq.md`
25. `reference/troubleshooting.md`

### Phase 6: Tests
26. `tests/conftest.py`
27. `tests/test_chunker.py`
28. `tests/test_loader.py`
29. `tests/test_check.py`
30. `tests/test_retrieval.py`

### Phase 7: GitHub + docs
31. All `.github/` files
32. `CONTRIBUTING.md`
33. `CHANGELOG.md`
34. `README.md` (last — references everything else)

### Phase 8: Notebooks
35. `notebooks/rag_starter_colab.ipynb`
36. `notebooks/rag_starter_local.ipynb`

### Phase 9: Guides (P2 — post-launch)
37. `guides/use-cloud-llm.md`
38. `guides/improve-results.md`
39. `guides/use-langchain.md`
40. `guides/use-llamaindex.md`
41. `guides/add-docx-support.md`
42. `guides/migrate-vector-db.md`

---

## Quick Reference: Directory Tree

```
C:\Users\mulli\projects\rag-starter\
│
├── CLAUDE.md
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── .gitignore
├── .env.example
│
├── src/
│   ├── __init__.py
│   ├── loader.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── store.py
│   ├── generator.py
│   └── pipeline.py
│
├── quickstart/
│   ├── requirements.txt
│   ├── install.sh
│   ├── install.ps1
│   ├── check.py
│   └── my_first_rag.py
│
├── bring-your-own-docs/
│   ├── README.md
│   ├── index_folder.py
│   ├── query.py
│   └── app.py
│
├── how-it-works/
│   ├── README.md
│   ├── 01-loading.md
│   ├── 02-chunking.md
│   ├── 03-embedding.md
│   ├── 04-retrieval.md
│   └── 05-generation.md
│
├── guides/
│   ├── use-cloud-llm.md
│   ├── use-langchain.md
│   ├── use-llamaindex.md
│   ├── improve-results.md
│   ├── add-docx-support.md
│   └── migrate-vector-db.md
│
├── notebooks/
│   ├── rag_starter_colab.ipynb
│   └── rag_starter_local.ipynb
│
├── sample-docs/
│   ├── README.md
│   ├── remote-work-best-practices.md
│   ├── project-management-fundamentals.md
│   ├── intro-to-machine-learning.md
│   ├── healthy-eating-guide.md
│   ├── berlin-travel-guide.md
│   └── what-is-rag.md
│
├── reference/
│   ├── glossary.md
│   ├── troubleshooting.md
│   └── faq.md
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_check.py
│   ├── test_chunker.py
│   ├── test_loader.py
│   └── test_retrieval.py
│
└── .github/
    ├── workflows/
    │   └── ci.yml
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   ├── workflow_request.md
    │   └── beginner_question.md
    └── PULL_REQUEST_TEMPLATE.md
```

**Total: 58 files across 11 directories.**
