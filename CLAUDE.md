# CLAUDE.md

## Project

**rag-starter** — Your first RAG pipeline. Running in 15 minutes. On your own documents.

An open-source repository that enables non-engineers (PMs, analysts, writers, students) to go from zero to a working Retrieval-Augmented Generation pipeline on their own documents in under 15 minutes. Local-first. Zero-framework at the core. MIT licensed.

Repository: `github.com/salahuddin-s/rag-starter`

## Architecture

The project has one shared Python module (`src/`) consumed by three interfaces: a quickstart script, CLI tools, and a Streamlit app. No code duplication across entry points.

```
src/               ← Shared RAG library (the brain)
  loader.py        ← Load PDF, MD, TXT files into Document objects
  chunker.py       ← Split text into overlapping chunks (hand-written, no framework)
  embedder.py      ← Generate embeddings via Ollama (nomic-embed-text)
  store.py         ← ChromaDB wrapper: create, add, query
  generator.py     ← Send query + context to Ollama LLM, return answer
  pipeline.py      ← Orchestrate: index_documents() and query_documents()

quickstart/        ← First-run experience
  my_first_rag.py  ← Imports from src/, runs on sample-docs/, prints answers
  check.py         ← Health check (Python, Ollama, models, packages)
  install.sh/ps1   ← One-command setup scripts
  requirements.txt ← Pinned dependencies

bring-your-own-docs/ ← The core product
  index_folder.py  ← CLI: index any folder → ChromaDB
  query.py         ← CLI: ask questions → answers with sources
  app.py           ← Streamlit UI wrapping the same pipeline

how-it-works/      ← Educational content (5 markdown explainers)
guides/            ← Upgrade paths (cloud LLM, LangChain, LlamaIndex, tuning)
notebooks/         ← Colab (zero-install) + local Jupyter
sample-docs/       ← 6 original markdown files (CC0, diverse topics)
reference/         ← Glossary, FAQ, troubleshooting
tests/             ← pytest, all LLM calls mocked
```

### Data flow

```
User's folder
  → src/loader.py     (extract text from PDF/MD/TXT)
  → src/chunker.py    (split into ~500-char chunks with 50-char overlap)
  → src/embedder.py   (Ollama nomic-embed-text → 768-dim vectors)
  → src/store.py      (persist in ChromaDB at ./chroma_db/)

User's question
  → src/embedder.py   (embed the question)
  → src/store.py      (cosine similarity → top-k chunks)
  → src/generator.py  (question + chunks → Ollama llama3.1:8b → answer)
```

## Stack — Locked for v0.1

| Layer | Choice | Version constraint |
|---|---|---|
| Runtime | Python 3.10+ | Supports 3.10, 3.11, 3.12 |
| LLM | Ollama + llama3.1:8b | ollama>=0.3 |
| Embeddings | nomic-embed-text via Ollama | (bundled with Ollama) |
| Vector store | ChromaDB | chromadb>=0.5,<1.0 |
| PDF loading | PyMuPDF + pymupdf4llm | pymupdf>=1.24, pymupdf4llm>=0.0.10 |
| UI | Streamlit | streamlit>=1.35 |
| Env vars | python-dotenv | python-dotenv>=1.0 |
| Testing | pytest + pytest-mock | Dev dependencies |
| Linting | ruff | Dev dependency |

### Explicitly excluded from v0.1

Do NOT introduce these unless explicitly told to: LangChain, LlamaIndex, Docker, Node.js/TypeScript, multi-modal (images), reranking, agentic RAG, any database server, any cloud-only dependency.

## Code Rules

### Python style

- **Max file length:** 150 lines of code (excluding comments and docstrings). If a file grows beyond this, split it.
- **Functions over classes.** Use plain functions. The only dataclass allowed is `Document` in `src/loader.py`. No class hierarchies, no inheritance, no abstract base classes.
- **Type hints everywhere.** Every function signature must have full type annotations including return type.
- **Docstrings on every function.** Plain English. First line says what the function does. Include an example if the function is non-obvious. No jargon in docstrings — if you say "embedding," add "(a list of numbers that captures the meaning of the text)."
- **Imports.** Group in order: stdlib → third-party → local (`src.`). One blank line between groups. No wildcard imports.
- **Error handling.** Catch specific exceptions. When Ollama isn't running, print a human-readable error message with the fix, not a stack trace. Use `sys.exit(1)` in CLI scripts; raise exceptions in library code (`src/`).
- **No print() in src/ files.** Library code uses `logging`. CLI scripts (`quickstart/`, `bring-your-own-docs/`) use print() for user-facing output.
- **Verbose flag.** Every CLI script and `pipeline.py` must support `--verbose` / `verbose=True`. When active, print what each RAG stage is doing and how long it took: `[loader] Loaded 7 files (3 PDF, 4 MD) in 0.8s`.

### Dependencies

- `requirements.txt` lives at `quickstart/requirements.txt` (not root — avoids confusion with project-level vs development deps).
- Pin major version ranges only: `chromadb>=0.5,<1.0` not `chromadb==0.5.23`.
- Dev dependencies (pytest, ruff, pytest-mock) go in a separate `requirements-dev.txt` at root.
- Never add a dependency without documenting why in a code comment at the import site.

### Configuration

- Default values hardcoded in function signatures (e.g., `chunk_size=500`). No config files in v0.1.
- Overridable via CLI flags (`--chunk-size 1000`) and function parameters.
- Cloud LLM support: if `OPENAI_API_KEY` env var is set, `src/generator.py` and `src/embedder.py` should have a code path for OpenAI. But Ollama is the default and works with no env vars.
- ChromaDB path defaults to `./chroma_db/` relative to the working directory.

## Writing Rules (Markdown)

These apply to every `.md` file in the repo:

- **First sentence answers "what does this do?"** No preamble, no "Welcome to…", no "In this guide we will…"
- **Second person.** Write "you" not "the user" or "one." Address the reader directly.
- **No jargon without a parenthetical.** First use of any technical term includes a plain-English explanation: "embeddings (lists of numbers that capture the meaning of text)."
- **Code blocks are copy-pasteable.** Include the full command, not fragments. Use `bash` or `python` syntax highlighting. If a command has a prerequisite, state it before the code block.
- **Heading structure.** Every file starts with one H1 (`#`). Never skip levels (no H1 → H3). Use H2 for sections, H3 for subsections. Max depth: H3.
- **No emoji in headings.** Emoji in body text is fine sparingly (checkmarks ✓, crosses ✗). No emoji in H1/H2/H3.
- **Line length.** Wrap prose at ~100 characters for readable diffs. Code blocks are exempt.

## Testing Rules

- **Framework:** pytest.
- **Location:** `tests/` directory. File naming mirrors source: `src/chunker.py` → `tests/test_chunker.py`.
- **No Ollama required.** All tests must pass without Ollama installed. Mock all LLM and embedding calls using `pytest-mock` or `unittest.mock`.
- **Shared fixtures** go in `tests/conftest.py`: sample text, sample chunks, mock embedding vectors, temporary ChromaDB directory (via `tmp_path`).
- **Test naming:** `test_<function_name>_<scenario>` e.g., `test_chunk_text_empty_input`, `test_chunk_text_respects_overlap`.
- **Assertions:** Use plain `assert` statements. No `self.assertEqual` (we don't use unittest classes).
- **Coverage target:** Every public function in `src/` has at least one test.

## Git Rules

- **Commit messages:** Imperative mood, <72 chars. e.g., `Add health check script`, `Fix PDF loading for scanned documents`.
- **Branch naming:** `feature/short-description`, `fix/short-description`.
- **.gitignore must exclude:** `chroma_db/`, `__pycache__/`, `*.pyc`, `.env`, `.ipynb_checkpoints/`, `indexed_data/`, `*.egg-info/`, `dist/`, `build/`, `.venv/`, `venv/`.
- **No generated files committed.** No `chroma_db/` data, no compiled Python, no notebook outputs.

## File Specifications

Detailed specs for every file, grouped by build phase. Create files in this order — later phases import from earlier ones.

### Phase 1: Skeleton

**`.gitignore`** — Python defaults plus: `chroma_db/`, `.env`, `__pycache__/`, `*.pyc`, `.ipynb_checkpoints/`, `indexed_data/`, `*.egg-info/`, `dist/`, `build/`, `.venv/`, `venv/`, `.ruff_cache/`.

**`.env.example`** — Two commented lines: `# OPENAI_API_KEY=your-key-here` and `# OLLAMA_HOST=http://localhost:11434`. Comment above explaining these are optional.

**`LICENSE`** — Standard MIT license. Year: 2025. Copyright holder: "rag-starter contributors".

**`src/__init__.py`** — Single line: `__version__ = "0.1.0"`.

**`tests/__init__.py`** — Empty file.

**`quickstart/requirements.txt`** — Runtime dependencies only:
```
chromadb>=0.5,<1.0
pymupdf>=1.24
pymupdf4llm>=0.0.10
ollama>=0.3
streamlit>=1.35
python-dotenv>=1.0
openai>=1.30
```

**`requirements-dev.txt`** — Dev dependencies:
```
pytest>=8.0
pytest-mock>=3.12
ruff>=0.4
```

### Phase 2: Core module (src/)

**`src/loader.py`**
- Dataclass: `Document(content: str, metadata: dict)` where metadata has keys `source` (filename) and `page` (int, 0 for non-PDF).
- Functions: `load_pdf(path: str) → list[Document]` (uses pymupdf4llm, one Document per page), `load_markdown(path: str) → Document`, `load_text(path: str) → Document`, `load_folder(folder_path: str, verbose: bool = False) → list[Document]`.
- `load_folder` walks recursively, dispatches by extension (`.pdf`, `.md`, `.txt`), skips unknown types with a warning, returns flat list.
- Log format when verbose: `[loader] Loaded 3 pages from report.pdf`.

**`src/chunker.py`**
- Function: `chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) → list[str]`.
- Implementation: recursive character text splitter. Try splitting on `"\n\n"` first, then `"\n"`, then `". "`, then `" "`, then character-level. Each separator tried in order until chunks fit within `chunk_size`.
- Every step commented explaining WHY: "We try paragraph breaks first because they're the most natural split points."
- Return empty list for empty input, single-element list if text is shorter than chunk_size.
- Helper: `chunk_documents(docs: list[Document], chunk_size: int = 500, chunk_overlap: int = 50) → tuple[list[str], list[dict]]` — chunks all documents, returns parallel lists of (chunk_texts, chunk_metadatas) where metadata includes original source and chunk index.

**`src/embedder.py`**
- Function: `embed_texts(texts: list[str], model: str = "nomic-embed-text") → list[list[float]]`.
- Uses the `ollama` Python client: `ollama.embed(model=model, input=texts)`.
- If Ollama is not running, catch `ConnectionError` and print: `"Could not connect to Ollama. Is it running? Start it with: ollama serve"` then `sys.exit(1)`.
- Function: `embed_query(query: str, model: str = "nomic-embed-text") → list[float]` — convenience wrapper for a single string.
- Optional cloud path: if `OPENAI_API_KEY` is set in env, provide `embed_texts_openai()` as an alternative. Do NOT make this the default.

**`src/store.py`**
- Function: `create_store(path: str = "./chroma_db", collection_name: str = "documents") → tuple[chromadb.Client, Collection]`.
- Function: `add_documents(collection, chunks: list[str], embeddings: list[list[float]], metadatas: list[dict]) → None`. Uses ChromaDB's `collection.add()`. Generates string IDs: `"chunk_0"`, `"chunk_1"`, etc.
- Function: `query_store(collection, query_embedding: list[float], top_k: int = 5) → list[dict]`. Returns list of `{"content": str, "metadata": dict, "distance": float}`.
- Function: `store_exists(path: str = "./chroma_db") → bool` — check if an index already exists at that path.

**`src/generator.py`**
- The RAG prompt template as a module-level constant string (visible, editable, not hidden):
```python
RAG_PROMPT_TEMPLATE = """You are a helpful assistant. Answer the question based ONLY on the following context. If the context doesn't contain enough information to answer, say "I don't have enough information to answer that."

Context:
{context}

Question: {question}

Answer:"""
```
- Function: `generate_answer(question: str, context_chunks: list[str], model: str = "llama3.1:8b") → str`. Formats the prompt, calls `ollama.chat()`, returns the response text.
- Function: `format_context(chunks: list[str]) → str` — joins chunks with `"\n---\n"` separators.
- Optional: `generate_answer_openai()` for cloud path. Not the default.

**`src/pipeline.py`**
- Function: `index_documents(folder_path: str, db_path: str = "./chroma_db", chunk_size: int = 500, chunk_overlap: int = 50, verbose: bool = False) → dict`. Returns stats: `{"files_loaded": int, "chunks_created": int, "time_seconds": float}`. Calls loader → chunker → embedder → store in sequence. When verbose, prints each stage with timing.
- Function: `query_documents(question: str, db_path: str = "./chroma_db", top_k: int = 5, model: str = "llama3.1:8b", verbose: bool = False) → dict`. Returns `{"answer": str, "sources": list[dict]}` where each source has `content`, `metadata`, `distance`. When verbose, prints retrieval results before generation.
- Both functions are the ONLY entry points other files should use. Scripts should NOT call `src/embedder.py` directly.

### Phase 3: Quickstart

**`quickstart/check.py`**
- Runs as: `python quickstart/check.py`
- Checks (in order): Python >= 3.10, required pip packages installed, Ollama binary available (`shutil.which("ollama")`), Ollama service responding (`ollama.list()`), `llama3.1:8b` model available, `nomic-embed-text` model available.
- Output format: `✓ Python 3.11.9` or `✗ Ollama not found — install from https://ollama.ai`.
- Exit code 0 if all pass, 1 if any fail.

**`quickstart/my_first_rag.py`**
- Runs as: `python quickstart/my_first_rag.py [--verbose]`
- Steps: (1) Index sample-docs/ into a temporary ChromaDB, (2) Ask 3 hardcoded questions that test cross-document retrieval: "What are the best practices for async communication in remote teams?", "How does supervised learning differ from unsupervised learning?", "What neighbourhoods should I visit in Berlin?", (3) Print each question, answer, and source file.
- Output must be clean and readable — not raw JSON. Format like:
```
Question: What are the best practices for async communication?
Answer: [generated answer]
Source: remote-work-best-practices.md

---
```
- At the bottom of the file, include a comment block showing expected output so users can verify.

**`quickstart/install.sh`**
- Shebang: `#!/usr/bin/env bash`, `set -e`.
- Check Python >= 3.10 exists. Create venv at `.venv/` if not exists. Activate venv. `pip install -r quickstart/requirements.txt`. Check if Ollama is installed (if not, print install instructions and exit). `ollama pull llama3.1:8b`. `ollama pull nomic-embed-text`. Run `python quickstart/check.py`.
- Make it idempotent — safe to run multiple times.

**`quickstart/install.ps1`**
- PowerShell equivalent. Same logic, Windows syntax. Use `python -m venv .venv`, `.venv\Scripts\Activate.ps1`. Handle the common PowerShell execution policy issue with a clear message.

### Phase 4: Bring your own docs

**`bring-your-own-docs/README.md`**
- H1: "Bring Your Own Documents"
- First sentence: "Point this at any folder of PDFs, markdown files, or text files and start asking questions."
- Three sections: Index (one command), Query (one command), Launch UI (one command).
- Supported formats table. Mention that DOCX support is coming (see `guides/add-docx-support.md`).

**`bring-your-own-docs/index_folder.py`**
- Runs as: `python bring-your-own-docs/index_folder.py /path/to/folder [--chunk-size 500] [--chunk-overlap 50] [--db-path ./chroma_db] [--verbose]`
- Uses `argparse`. Imports `src.pipeline.index_documents()`. Prints summary on completion.
- If folder doesn't exist or is empty, print a helpful error.

**`bring-your-own-docs/query.py`**
- Runs as: `python bring-your-own-docs/query.py "Your question here" [--top-k 5] [--model llama3.1:8b] [--db-path ./chroma_db] [--verbose]`
- Uses `argparse`. Imports `src.pipeline.query_documents()`. Prints answer + sources.
- If no index exists at db-path, print: "No index found. Run index_folder.py first."
- Interactive mode: if no question argument, enter a loop that prompts for questions until Ctrl+C.

**`bring-your-own-docs/app.py`**
- Single-file Streamlit app. Run as: `streamlit run bring-your-own-docs/app.py`
- Sidebar: text input for folder path, "Index Documents" button, chunk size slider (100-2000, default 500), top-k slider (1-20, default 5), model selector (text input, default `llama3.1:8b`).
- Main area: chat input. When user submits a question, call `src.pipeline.query_documents()`, display answer, show sources in `st.expander()` sections (one per source chunk with filename and excerpt).
- Session state: maintain chat history within the session.
- Show a warning banner if no documents are indexed yet.

### Phase 5: Content

**`sample-docs/README.md`**
- Explains these are original CC0 documents written for rag-starter. Lists each file with a one-line description. Notes they're designed to cover diverse topics for testing cross-document retrieval.

**`sample-docs/remote-work-best-practices.md`** — ~500 words. Written as an internal company guide. Topics: async-first communication, meeting discipline (agenda required, notes shared within 24h), documentation culture (decisions in writing, not Slack), home office ergonomics, timezone awareness. Include specific actionable advice, not platitudes.

**`sample-docs/project-management-fundamentals.md`** — ~500 words. Written as a training document. Topics: defining scope (and why scope creep kills projects), the iron triangle (scope/time/cost), stakeholder management, risk registers, when agile works vs. when waterfall works. Include a mini-example of a risk register entry.

**`sample-docs/intro-to-machine-learning.md`** — ~500 words. Written as a beginner explainer. Topics: what ML is (pattern recognition from data), supervised vs. unsupervised learning with concrete examples (spam detection vs. customer segmentation), training data and why quality matters, overfitting explained with an analogy (memorising exam answers vs. understanding the subject), real-world applications (recommendations, fraud detection, medical imaging).

**`sample-docs/healthy-eating-guide.md`** — ~400 words. Written as a wellness guide. Topics: macronutrients (protein, carbs, fats — what each does), the plate method for portion control, hydration (how much, when), common myths debunked (fat doesn't make you fat, carbs aren't evil). Practical, no-nonsense tone.

**`sample-docs/berlin-travel-guide.md`** — ~500 words. Written as a personal travel blog post. Topics: neighbourhood breakdown (Kreuzberg for culture, Mitte for museums, Prenzlauer Berg for brunch, Neukölln for nightlife), getting around (U-Bahn/S-Bahn, cycling), food recommendations (currywurst, döner, third-wave coffee), cultural tips (cash is still king in some places, Sunday closures). Personal voice — this should read like a friend's recommendation, not a guidebook.

**`sample-docs/what-is-rag.md`** — ~400 words. Meta document: explains RAG in plain English. Topics: the problem (LLMs don't know your private documents), the solution (retrieve relevant context, then generate), the pipeline (load → chunk → embed → store → retrieve → generate), when to use RAG vs. fine-tuning, limitations (quality depends on retrieval, not just the LLM). This lets the demo answer questions about itself.

**`how-it-works/README.md`** — Pipeline overview. "RAG in 5 steps" with one paragraph per step and links to the detailed pages. Include an ASCII pipeline diagram.

**`how-it-works/01-loading.md`** through **`05-generation.md`** — See file manifest for content specs. ~300-400 words each. Plain English. No prerequisites. Each page is self-contained.

**`reference/glossary.md`** — 25 terms. Format: `**Term** — Definition. *Analogy: ...*`. Keep definitions to one sentence. Keep analogies concrete and relatable. Example: `**Embedding** — A list of numbers (typically 768) that represents the meaning of a piece of text. *Analogy: GPS coordinates for ideas — similar meanings get nearby coordinates.*`

**`reference/faq.md`** — 10 questions. Q&A format. Questions: "Do I need a GPU?", "Is my data sent to the cloud?", "Can I use this at work with confidential documents?", "How much does it cost?", "What file types are supported?", "How is this different from ChatGPT?", "Can I use a different LLM?", "How many documents can this handle?", "What if my results are bad?", "Can I contribute?"

**`reference/troubleshooting.md`** — 10 issues. Format: **Problem** → **Cause** → **Fix**. Issues: Ollama not found, model not found, connection refused, ChromaDB permission error, empty results, slow responses, out of memory, Python version error, import errors, Windows path issues.

### Phase 6: Tests

**`tests/conftest.py`** — Fixtures: `sample_text` (a known 1000-char paragraph), `sample_documents` (3 Document objects with varied content), `mock_embeddings` (deterministic 768-dim vectors for testing), `temp_chroma_path` (uses `tmp_path` fixture for isolated ChromaDB).

**`tests/test_chunker.py`** — Tests: empty input → empty list, text shorter than chunk_size → single chunk, text at exact chunk_size boundary, overlap is respected (last N chars of chunk K appear as first N chars of chunk K+1), separators are tried in order.

**`tests/test_loader.py`** — Tests: load a markdown file from sample-docs/ (real file), load a text file (create in tmp_path), `load_folder` with mixed file types, `load_folder` on empty directory, `load_folder` skips unknown extensions with warning.

**`tests/test_check.py`** — Mock `shutil.which` and `ollama.list()` to test all check.py pass/fail scenarios.

**`tests/test_retrieval.py`** — Integration test: create a ChromaDB with known chunks and mock embeddings, query it, verify the correct chunks are returned. Mock the Ollama embed call to return deterministic vectors.

### Phase 7: GitHub + docs

**`.github/workflows/ci.yml`** — Matrix: Python 3.10, 3.12. Steps: checkout, setup-python, `pip install -r quickstart/requirements.txt -r requirements-dev.txt`, `ruff check .`, `pytest tests/ -v`. No Ollama in CI — tests must mock.

**`.github/ISSUE_TEMPLATE/bug_report.md`** — YAML frontmatter with name, description, labels. Fields: OS + version, Python version, Ollama version, steps to reproduce, expected vs. actual behaviour, full error output.

**`.github/ISSUE_TEMPLATE/workflow_request.md`** — "I want to use RAG for [use case]." Fields: use case description, document format(s), desired outcome.

**`.github/ISSUE_TEMPLATE/beginner_question.md`** — "No question is too basic." Fields: what you're trying to do, what happened, what you expected. Label: `question`.

**`.github/PULL_REQUEST_TEMPLATE.md`** — Checklist: tests pass (`pytest tests/`), lint passes (`ruff check .`), docs updated if behaviour changed, tested on a fresh venv, follows the code rules in CLAUDE.md.

**`CONTRIBUTING.md`** — How to contribute. Sections: filing issues (use templates), submitting PRs (fork → branch → PR), code style (point to Code Rules above), good first issues (link to label), development setup (clone, install dev deps, run tests).

**`CHANGELOG.md`** — Start with `## [0.1.0] - Unreleased` and list initial features under Added.

**`README.md`** — The most important file. Create LAST since it references everything else. Structure:
1. H1 + tagline + badges (stars, license, Python version, Open in Colab)
2. One-sentence pitch + one-line value props (local, free, 15 minutes)
3. GIF placeholder (`<!-- TODO: Add demo GIF -->`)
4. Three-path quickstart (Colab button / local commands / cloud LLM)
5. "Use it on YOUR documents" section (index + query commands)
6. "How does it work?" → link to `how-it-works/`
7. "Ready for more?" → link to `guides/`
8. "FAQ" → link to `reference/faq.md`
9. "Contributing" → link to `CONTRIBUTING.md`
10. License line

### Phase 8: Notebooks

**`notebooks/rag_starter_colab.ipynb`** — Uses Groq (free tier, no credit card) or OpenAI for LLM + embeddings since Ollama doesn't run in Colab. Cells: install deps → define sample text inline (copy from sample-docs) → chunk → embed → store in ChromaDB → query with 3 example questions → "Try your own" cell with text input. Every cell has a markdown cell above it explaining what happens. First cell has the Colab badge.

**`notebooks/rag_starter_local.ipynb`** — Same flow but uses Ollama. Prerequisite cell checks Ollama is running. Links to `quickstart/install.sh` for setup.

### Phase 9: Guides (post-launch, P2)

**`guides/use-cloud-llm.md`** — 3-line code change to swap Ollama for OpenAI. Cost estimate. When cloud is better (no GPU, need GPT-4 quality).

**`guides/improve-results.md`** — 5 tuning knobs: chunk size, chunk overlap, top-k, prompt template, embedding model. Each with a "try this" experiment.

**`guides/use-langchain.md`** — Same pipeline rebuilt with LangChain. Side-by-side code comparison. When LangChain helps (complex chains) and when it doesn't (simple Q&A).

**`guides/use-llamaindex.md`** — Same approach for LlamaIndex. Highlight its document indexing strengths.

**`guides/add-docx-support.md`** — Add `python-docx`, add `load_docx()` to loader.py. Good first contribution.

**`guides/migrate-vector-db.md`** — When to leave ChromaDB (>100k docs, need cloud, need metadata filtering). Step-by-step for Qdrant and Pinecone.

## Common Commands

```bash
# Setup
pip install -r quickstart/requirements.txt
pip install -r requirements-dev.txt
ollama pull llama3.1:8b && ollama pull nomic-embed-text

# Run
python quickstart/check.py
python quickstart/my_first_rag.py --verbose
python bring-your-own-docs/index_folder.py ~/my-docs --verbose
python bring-your-own-docs/query.py "your question" --verbose
streamlit run bring-your-own-docs/app.py

# Test & lint
pytest tests/ -v
ruff check .
ruff format .
```
