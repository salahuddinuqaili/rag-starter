# SPEC: v0.2 Phase 1 — FastAPI + React Shell

## Goal

Replace the Streamlit app with a FastAPI backend and React frontend that guides
a first-time user from zero to their first RAG answer. The `src/` library is
untouched — this phase wraps it in a proper web app.

## UX Flow (0 → 1)

1. User opens `http://localhost:5173` → lands on **Setup** screen
2. Setup screen auto-checks: is Ollama running? Are models pulled?
   - Green checkmarks for passing checks, red with fix instructions for failures
   - "Refresh" button to re-check after user fixes something
3. Once all checks pass → **Index** step appears
   - User enters a folder path (pre-filled with `./sample-docs`)
   - Clicks "Index" → progress indicator → success summary (files, chunks, time)
4. After indexing → **Chat** interface activates
   - Three example questions shown as clickable chips (same as current Streamlit)
   - Chat input at bottom, messages stream in via SSE
   - Each answer shows expandable source chunks with relevance badges
5. Sidebar: settings (chunk size, top-k, model, db path) — same as current app

## Backend (FastAPI)

New directory: `backend/`

### Endpoints

```
GET  /api/health          → { ollama: bool, models: { llama3.1:8b: bool, nomic-embed-text: bool } }
POST /api/index           → { folder_path, chunk_size?, chunk_overlap?, db_path? }
                            Returns: { files_loaded, chunks_created, time_seconds }
GET  /api/index/status    → { indexed: bool, chunk_count: int }
POST /api/query           → { question, top_k?, model?, db_path? }
                            Returns: SSE stream — data chunks then final sources JSON
```

### SSE streaming format for /api/query

```
event: token
data: {"text": "The"}

event: token
data: {"text": " answer"}

event: sources
data: [{"content": "...", "metadata": {...}, "distance": 0.23}]

event: done
data: {}
```

### Implementation notes

- `backend/main.py` — FastAPI app, imports from `src/` directly
- `backend/routes/` — split if main.py exceeds 150 lines
- Health check calls `ollama.list()` — same pattern as current `app.py:_check_ollama()`
- Index endpoint calls `src.pipeline.index_documents()` directly
- Query endpoint uses `src.generator.generate_answer_stream()` wrapped in SSE
- Error handling: catch `RagStarterError` subtypes, return structured JSON errors
- CORS middleware: allow `localhost:5173` in dev

### Dependencies (added to pyproject.toml)

- `fastapi>=0.111` — ASGI web framework
- `uvicorn[standard]>=0.30` — ASGI server
- `sse-starlette>=2.0` — SSE support for FastAPI

## Frontend (React + Vite + Tailwind)

New directory: `frontend/`

### Stack

- React 19 + Vite (scaffolded with `npm create vite@latest`)
- Tailwind CSS v4
- No additional UI library — plain Tailwind components
- No state management library — React state + context is sufficient

### Pages / Views (single-page app, no router needed)

1. **SetupView** — prerequisite checklist with auto-refresh
2. **IndexView** — folder path input + index button + progress
3. **ChatView** — message list + input + source expanders
4. Transition between views based on state: checks pass → show index,
   index exists → show chat

### Key components

- `HealthCheck` — polls `/api/health`, renders checklist
- `IndexForm` — folder path input, index button, stats display
- `ChatMessage` — renders one message (user or assistant)
- `SourceList` — expandable source chunks with relevance badges
- `StreamingMessage` — accumulates SSE tokens into a growing message
- `Settings` — sidebar panel for chunk_size, top_k, model, db_path

### SSE consumption

```js
const eventSource = new EventSource('/api/query?...');
// or use fetch() with ReadableStream for POST requests
```

Since `/api/query` is POST, use `fetch()` with `getReader()` on the response body,
not `EventSource` (which only supports GET). Parse SSE format manually or use a
small helper function.

## Package Management

- Migrate from pip to **uv** for Python
- `pyproject.toml` at project root replaces `quickstart/requirements.txt`
- Keep `quickstart/requirements.txt` as a secondary install path for users who
  don't have uv (generated from pyproject.toml, not hand-maintained)
- Frontend uses npm (standard for React/Vite)

### pyproject.toml structure

```toml
[project]
name = "rag-starter"
version = "0.2.0"
requires-python = ">=3.10"
dependencies = [
    "chromadb>=0.5,<1.0",
    "pymupdf>=1.24",
    "pymupdf4llm>=0.0.10",
    "ollama>=0.3",
    "python-dotenv>=1.0",
    "openai>=1.30",
    "fastapi>=0.111",
    "uvicorn[standard]>=0.30",
    "sse-starlette>=2.0",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-mock>=3.12", "ruff>=0.4"]
```

## Dev Workflow

```bash
# Backend
uv run uvicorn backend.main:app --reload --port 8000

# Frontend
cd frontend && npm run dev    # Vite dev server on :5173

# Test
uv run pytest tests/ -v
```

## File Inventory (new files this phase creates)

```
pyproject.toml
backend/
  __init__.py
  main.py              ← FastAPI app, CORS, routes
frontend/
  package.json
  vite.config.js
  tailwind.config.js   ← (if needed by Tailwind v4)
  index.html
  src/
    main.jsx
    App.jsx            ← View routing based on state
    components/
      HealthCheck.jsx
      IndexForm.jsx
      ChatView.jsx
      ChatMessage.jsx
      SourceList.jsx
      StreamingMessage.jsx
      Settings.jsx
    hooks/
      useSSE.js        ← POST-based SSE consumption hook
    api.js             ← fetch wrappers for all endpoints
    index.css          ← Tailwind imports
```

## What This Phase Does NOT Include

- Multi-collection support (Phase 2)
- Chat history persistence (Phase 2)
- Document management UI — upload/delete from browser (Phase 2)
- File upload via browser — Phase 1 uses folder paths like v0.1
- Authentication
- Docker / deployment

## Done Criteria

- [ ] `uv run uvicorn backend.main:app` starts the API server
- [ ] `cd frontend && npm run dev` starts the React dev server
- [ ] Health check endpoint reports Ollama + model status
- [ ] User can index `./sample-docs` from the UI
- [ ] User can ask a question and see a streaming answer with sources
- [ ] Settings (chunk size, top-k, model) are adjustable from sidebar
- [ ] All 42 existing tests still pass
- [ ] `ruff check .` passes
