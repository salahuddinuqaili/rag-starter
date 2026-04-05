# CLAUDE.md

## Project

**rag-starter** — Your first RAG pipeline. On your own documents. Completely local.

An open-source repository that enables non-engineers (PMs, analysts, writers, students)
to go from zero to a working Retrieval-Augmented Generation pipeline on their own
documents. Local-first. Zero-framework at the core. MIT licensed.

Repository: `github.com/salahuddinuqaili/rag-starter`

## Architecture

One shared Python module (`src/`) consumed by three interfaces: a quickstart script,
CLI tools, and a Streamlit app. No code duplication across entry points.

```
src/               ← Shared RAG library (the brain)
  errors.py        ← Custom exceptions (OllamaConnectionError, etc.)
  loader.py        ← Load PDF, MD, TXT files into Document objects
  chunker.py       ← Split text into overlapping chunks (hand-written, no framework)
  embedder.py      ← Generate embeddings via Ollama (nomic-embed-text)
  store.py         ← ChromaDB wrapper: create, add, query with metadata filtering
  generator.py     ← Send query + context to Ollama LLM, return answer (+ streaming)
  pipeline.py      ← Orchestrate: index_documents() and query_documents()

quickstart/        ← First-run experience
  my_first_rag.py  ← Imports from src/, runs on sample-docs/, prints answers
  check.py         ← Health check (Python, Ollama, models, packages)
  install.sh/ps1   ← One-command setup scripts
  requirements.txt ← Runtime dependencies

bring-your-own-docs/ ← The core product
  index_folder.py  ← CLI: index any folder → ChromaDB
  query.py         ← CLI: ask questions → answers with sources (+ interactive mode)
  app.py           ← Streamlit UI with onboarding, chat, and source display

how-it-works/      ← Educational content (5 markdown explainers, cross-linked)
guides/            ← Upgrade paths (cloud LLM, tuning, LangChain, LlamaIndex)
notebooks/         ← Colab (Groq, zero-install) + local Jupyter (Ollama)
sample-docs/       ← 6 original markdown files (CC0, diverse topics)
reference/         ← Glossary (25 terms), FAQ (10 Qs), troubleshooting (10 issues)
tests/             ← pytest (42 tests), all LLM calls mocked
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
  → src/store.py      (cosine similarity → top-k chunks, optional metadata filter)
  → src/generator.py  (question + chunks → Ollama llama3.1:8b → answer)
```

### Key API surfaces

**`src/pipeline.py`** is the only entry point scripts should use:
- `index_documents(folder_path, db_path, chunk_size, chunk_overlap, verbose) → dict`
- `query_documents(question, db_path, top_k, model, verbose, prompt_template, where, max_distance) → dict`

**`src/errors.py`** — library code raises these; CLI scripts catch at the boundary:
- `OllamaConnectionError` — Ollama not running
- `OllamaModelNotFoundError` — model not pulled
- `MissingAPIKeyError` — cloud API key not set
- `IndexNotFoundError` — querying before indexing

**`src/generator.py`** — prompt template is customisable:
- `generate_answer(question, context_chunks, model, prompt_template) → str`
- `generate_answer_stream(question, context_chunks, model, prompt_template) → Generator[str]`
- `RAG_PROMPT_TEMPLATE` — module-level constant, the default template

**`src/store.py`** — supports metadata filtering and relevance thresholds:
- `query_store(collection, query_embedding, top_k, where, max_distance) → list[dict]`

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

Do NOT introduce these unless explicitly told to: LangChain, LlamaIndex, Docker,
Node.js/TypeScript, multi-modal (images), reranking, agentic RAG, any database
server, any cloud-only dependency.

## Code Rules

### Python style

- **Max file length:** 150 lines of code (excluding comments and docstrings). If a
  file grows beyond this, split it.
- **Functions over classes.** Use plain functions. The only dataclass allowed is
  `Document` in `src/loader.py`. No class hierarchies, no inheritance, no ABCs.
- **Type hints everywhere.** Every function signature must have full type annotations
  including return type.
- **Docstrings on every function.** Plain English. First line says what the function
  does. Include an example if the function is non-obvious. No jargon in docstrings —
  if you say "embedding," add "(a list of numbers that captures the meaning of the text)."
- **Imports.** Group in order: stdlib → third-party → local (`src.`). One blank line
  between groups. No wildcard imports.
- **Error handling.** Library code (`src/`) raises custom exceptions from `src/errors.py`.
  CLI scripts catch `RagStarterError` at the boundary and call `sys.exit(1)` with a
  human-readable message. Never `sys.exit()` inside `src/`.
- **No print() in src/ files.** Library code uses `logging`. The one exception is
  `pipeline.py` which prints verbose stage timing. CLI scripts use print() for
  user-facing output.
- **Verbose flag.** Every CLI script and `pipeline.py` must support `--verbose` /
  `verbose=True`. When active, print what each RAG stage is doing and how long it took.

### Dependencies

- `requirements.txt` lives at `quickstart/requirements.txt` (not root — avoids
  confusion with project-level vs development deps).
- Pin major version ranges only: `chromadb>=0.5,<1.0` not `chromadb==0.5.23`.
- Dev dependencies (pytest, ruff, pytest-mock) go in a separate `requirements-dev.txt`
  at root.
- Never add a dependency without documenting why in a code comment at the import site.

### Configuration

- Default values hardcoded in function signatures (e.g., `chunk_size=500`). No config
  files in v0.1.
- Overridable via CLI flags (`--chunk-size 1000`) and function parameters.
- Cloud LLM support: if `OPENAI_API_KEY` env var is set, `src/generator.py` and
  `src/embedder.py` have a code path for OpenAI. Ollama is the default.
- ChromaDB path defaults to `./chroma_db/` relative to the working directory.

## Writing Rules (Markdown)

These apply to every `.md` file in the repo:

- **First sentence answers "what does this do?"** No preamble.
- **Second person.** Write "you" not "the user."
- **No jargon without a parenthetical.** First use of any technical term includes a
  plain-English explanation.
- **Code blocks are copy-pasteable.** Include the full command. If a command has a
  prerequisite, state it before the code block.
- **Heading structure.** One H1 per file. Never skip levels. Max depth: H3.
- **No emoji in headings.** Emoji in body text is fine sparingly.
- **Line length.** Wrap prose at ~100 characters. Code blocks are exempt.
- **Cross-linking.** Every reference page should have a "See Also" or "Next Steps"
  footer linking to related content. No dead-end pages.

## Testing Rules

- **Framework:** pytest.
- **Location:** `tests/` directory. File naming mirrors source: `src/chunker.py` →
  `tests/test_chunker.py`.
- **No Ollama required.** All tests must pass without Ollama installed. Mock all LLM
  and embedding calls using `pytest-mock` or `unittest.mock`.
- **Shared fixtures** go in `tests/conftest.py`: sample text, sample chunks, mock
  embedding vectors, temporary ChromaDB directory (via `tmp_path`).
- **Test naming:** `test_<function_name>_<scenario>`.
- **Assertions:** Use plain `assert` statements. No unittest classes.
- **Coverage target:** Every public function in `src/` has at least one test.
- **Current count:** 42 tests across 4 test files.

## Git Rules

- **Commit messages:** Conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`).
  Imperative mood, <72 chars.
- **Branch naming:** `feat/short-description`, `fix/short-description`.
- **.gitignore must exclude:** `chroma_db/`, `__pycache__/`, `*.pyc`, `.env`,
  `.ipynb_checkpoints/`, `indexed_data/`, `*.egg-info/`, `dist/`, `build/`, `.venv/`,
  `venv/`, `.ruff_cache/`.
- **No generated files committed.** No `chroma_db/` data, no compiled Python, no
  notebook outputs.
- **Decisions log:** Architecture decisions go in the project-level DECISIONS.md
  (in the Claude projects directory, not the repo).

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
