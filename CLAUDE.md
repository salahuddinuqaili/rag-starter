# CLAUDE.md

## Project

**rag-starter** — Local-first RAG pipeline for non-engineers (PMs, analysts, students).
One shared Python library (`src/`) consumed by three interfaces: quickstart scripts,
CLI tools, and a Streamlit app. MIT licensed.

Read the code for architecture details — `src/pipeline.py` is the orchestrator and
only entry point that scripts should import.

## Guardrails — v0.1

Do NOT introduce: LangChain, LlamaIndex, Docker, Node.js/TypeScript, multi-modal,
reranking, agentic RAG, any database server, any cloud-only dependency.

## Code Rules

### Python style

- **Max file length:** 150 lines of code (excluding comments/docstrings). Split if exceeded.
- **Functions over classes.** Only dataclass: `Document` in `src/loader.py`. No hierarchies.
- **Type hints everywhere.** Full annotations on every function signature.
- **Docstrings on every function.** Plain English, no jargon without parenthetical
  explanation (e.g. "embedding" needs "(a list of numbers that captures meaning)").
- **Imports:** stdlib, then third-party, then local (`src.`). One blank line between groups.
- **Error handling:** `src/` raises custom exceptions from `src/errors.py`. CLI scripts
  catch `RagStarterError` at the boundary with `sys.exit(1)`. Never `sys.exit()` in `src/`.
- **No print() in src/.** Use `logging`. Exception: `pipeline.py` verbose timing.
- **Verbose flag:** Every CLI script and `pipeline.py` supports `--verbose` / `verbose=True`.

### Dependencies

- Runtime deps: `quickstart/requirements.txt`. Dev deps: `requirements-dev.txt` (root).
- Pin major ranges only: `chromadb>=0.5,<1.0` not `chromadb==0.5.23`.
- Document why at the import site when adding a new dependency.

### Configuration

- Defaults hardcoded in function signatures. No config files in v0.1.
- Overridable via CLI flags and function parameters.
- Cloud LLM: `OPENAI_API_KEY` env var enables OpenAI code path. Ollama is default.
- ChromaDB path defaults to `./chroma_db/`.

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
- No generated files committed (chroma_db/, __pycache__, notebook outputs).
- Architecture decisions go in DECISIONS.md (Claude projects directory, not the repo).

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

## v0.2 Plan

Queued upgrade — start in a new session on branch `feat/v0.2-web-app`:

- Replace Streamlit with **FastAPI + React 19 + Vite + Tailwind v4** (SSE streaming)
- Add multi-collection support, chat history, document management UI
- Migrate to **uv** (pip is broken on this machine)
- `src/` RAG library stays unchanged — upgrade is interface layer only
- Keep core philosophy: no LangChain, no heavy frameworks, direct Ollama calls
