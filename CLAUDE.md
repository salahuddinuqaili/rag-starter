# CLAUDE.md

## Project

**rag-starter** — Local-first RAG pipeline for non-engineers (PMs, analysts, students).
A shared Python library (`src/`) with a FastAPI + React web app, CLI tools, and
quickstart scripts. MIT licensed.

`src/pipeline.py` is the RAG orchestrator. `backend/main.py` is the FastAPI app.
`frontend/` is React 19 + Vite + Tailwind v4.

## Guardrails

Do NOT introduce: LangChain, LlamaIndex, Docker, multi-modal (images), reranking,
agentic RAG, any database server, any cloud-only dependency.

## Code Rules

### Python style

- **Max file length:** 150 lines of code (excluding comments/docstrings). Split if exceeded.
- **Functions over classes.** Only dataclass: `Document` in `src/loader.py`. No hierarchies.
- **Type hints everywhere.** Full annotations on every function signature.
- **Docstrings on every function.** Plain English, no jargon without parenthetical
  explanation (e.g. "embedding" needs "(a list of numbers that captures meaning)").
- **Imports:** stdlib, then third-party, then local (`src.` / `backend.`). One blank
  line between groups.
- **Error handling:** `src/` raises custom exceptions from `src/errors.py`. Backend
  catches `RagStarterError` via FastAPI exception handler. Never `sys.exit()` in `src/`.
- **No print() in src/.** Use `logging`. Exception: `pipeline.py` verbose timing.

### Dependencies

- Python deps managed by **uv** via `pyproject.toml` at root. Dev deps in
  `[dependency-groups]`. `quickstart/requirements.txt` kept as secondary install path.
- Pin major ranges only: `chromadb>=0.5,<1.0` not `chromadb==0.5.23`.
- Frontend deps: `frontend/package.json` (npm).
- Document why at the import site when adding a new dependency.

### Configuration

- Defaults hardcoded in function signatures. No config files.
- Overridable via API parameters, CLI flags, and frontend Settings panel.
- Cloud LLM: `OPENAI_API_KEY` env var enables OpenAI code path. Ollama is default.
- Embedding model configurable via `embed_model` param (default nomic-embed-text).
- Data: ChromaDB at `./chroma_db/`, SQLite at `./rag_starter.db`, uploads at `./uploads/`.

## Writing Rules (Markdown)

- First sentence answers "what does this do?" No preamble.
- Second person ("you" not "the user").
- No jargon without parenthetical. First use of a term includes plain-English explanation.
- Code blocks must be copy-pasteable with full commands.
- One H1 per file. Never skip levels. Max depth: H3. No emoji in headings.
- Wrap prose at ~100 chars. Cross-link related pages — no dead ends.

## Testing Rules

- pytest in `tests/`. File naming mirrors source: `src/chunker.py` → `tests/test_chunker.py`.
- All tests must pass without Ollama. Mock all LLM/embedding calls.
- Shared fixtures in `tests/conftest.py`. Test naming: `test_<function>_<scenario>`.
- Plain `assert` statements. No unittest classes.
- Every public function in `src/` has at least one test.

## Git Rules

- Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`. Imperative mood, <72 chars.
- Branch naming: `feat/short-description`, `fix/short-description`.
- No generated files committed (chroma_db/, __pycache__, node_modules/, rag_starter.db).
- Architecture decisions go in DECISIONS.md (Claude projects directory, not the repo).

## Common Commands

```bash
# Setup
uv sync --dev
ollama pull llama3.1:8b && ollama pull nomic-embed-text
cd frontend && npm install

# Run (two terminals)
uv run uvicorn backend.main:app --reload --port 8000
cd frontend && npm run dev    # opens http://localhost:5173

# Legacy CLI
python quickstart/my_first_rag.py --verbose
python bring-your-own-docs/index_folder.py ~/my-docs --verbose
python bring-your-own-docs/query.py "your question" --verbose

# Test & lint
uv run python -m pytest tests/ -v
uv run ruff check .
uv run ruff format .
```
