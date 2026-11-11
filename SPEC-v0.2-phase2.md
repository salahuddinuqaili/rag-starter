# SPEC: v0.2 Phase 2 — Collections, Chat History, Document Management

## Goal

Build on the Phase 1 web app to add the three features that make rag-starter
a real tool: manage multiple document collections, persist conversations, and
upload/delete documents from the browser.

## Depends On

Phase 1 must be complete and merged. This spec assumes the FastAPI + React app
from Phase 1 is working.

## Feature 1: Multi-Collection Support

### What changes

Users can create named collections (e.g., "work-docs", "study-notes") instead
of everything going into one default collection. Each collection has its own
ChromaDB namespace and its own indexed documents.

### Backend

```
POST   /api/collections                → { name } → { id, name, chunk_count, created_at }
GET    /api/collections                → [{ id, name, chunk_count, created_at }]
DELETE /api/collections/{name}         → 204
POST   /api/collections/{name}/index   → { folder_path, chunk_size?, chunk_overlap? }
POST   /api/collections/{name}/query   → { question, top_k?, model? } → SSE stream
```

### Implementation

- `src/store.py` already accepts `collection_name` param — this is the hook
- Each collection is a ChromaDB collection within the same `./chroma_db/` directory
- Collection metadata (name, created_at) stored in a SQLite database (`./rag_starter.db`)
- Default collection named "documents" for backwards compatibility

### Frontend

- Collection picker dropdown in sidebar (above settings)
- "New Collection" button → name input → create
- Delete collection with confirmation dialog
- Active collection determines which index/query endpoints to call

## Feature 2: Chat History (SQLite)

### Schema

```sql
CREATE TABLE conversations (
    id          TEXT PRIMARY KEY,   -- UUID
    collection  TEXT NOT NULL,      -- which collection this chat is about
    title       TEXT,               -- auto-generated from first question
    created_at  TEXT NOT NULL,      -- ISO 8601
    updated_at  TEXT NOT NULL
);

CREATE TABLE messages (
    id              TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role            TEXT NOT NULL,       -- 'user' or 'assistant'
    content         TEXT NOT NULL,
    sources         TEXT,               -- JSON string of source chunks (nullable)
    created_at      TEXT NOT NULL,
    position        INTEGER NOT NULL    -- ordering within conversation
);
```

### Backend

```
GET    /api/conversations                    → [{ id, title, collection, updated_at }]
POST   /api/conversations                    → { collection } → { id, title, ... }
GET    /api/conversations/{id}               → { id, messages: [...], ... }
DELETE /api/conversations/{id}               → 204
```

- New conversation auto-created when user sends first message to a collection
  without an active conversation
- Title auto-generated: first 60 chars of first question
- Messages saved after each exchange (user message + assistant response)
- SQLite file: `./rag_starter.db` (same as collection metadata)

### Frontend

- Conversation list in left sidebar (below collection picker)
- Click a conversation to reload its messages
- "New Chat" button to start fresh
- Delete conversation with swipe or icon button

### Implementation

- New file: `backend/db.py` — SQLite helper functions (create tables, CRUD)
- Tables auto-created on first run (no migration tool needed)
- Use Python's `sqlite3` stdlib — no ORM, no new dependency

## Feature 3: Document Management UI

### What changes

Users can upload files directly from the browser instead of typing folder paths.
They can also see what's been indexed and remove documents.

### Backend

```
POST   /api/collections/{name}/upload    → multipart file upload → index immediately
GET    /api/collections/{name}/documents → [{ source, chunk_count, indexed_at }]
DELETE /api/collections/{name}/documents/{source} → remove chunks for that source → 204
```

### Implementation

- Uploaded files saved to `./uploads/{collection_name}/` before indexing
- After upload, run `src/loader` + `src/chunker` + `src/embedder` + `src/store`
  on that single file (don't re-index everything)
- Document list derived from ChromaDB metadata: `SELECT DISTINCT source FROM chunks`
  (via collection.get() with metadata inspection)
- Delete: remove all chunks with matching `source` metadata from ChromaDB collection
- Accepted formats: `.pdf`, `.md`, `.txt` (same as v0.1)

### Frontend

- Drag-and-drop upload zone (or file picker button) in the Index view
- Document list table: filename, chunk count, indexed date, delete button
- Upload progress indicator
- Keep the folder-path indexing as an "advanced" option

## File Inventory (new/modified files)

```
backend/
  db.py               ← SQLite helper: create tables, CRUD for conversations + collections
  main.py             ← Add new routes (or split into routes/ if >150 lines)
frontend/src/
  components/
    CollectionPicker.jsx
    ConversationList.jsx
    DocumentList.jsx
    FileUpload.jsx
  api.js              ← Add new endpoint wrappers
```

## What This Phase Does NOT Include

- Conversation context passed to LLM (follow-up questions are independent queries)
- Full-text search across conversations
- Export/import conversations
- User accounts or sharing

## Done Criteria

- [ ] User can create, switch between, and delete collections
- [ ] User can upload a PDF/MD/TXT from the browser and it gets indexed
- [ ] User can see a list of indexed documents and delete individual ones
- [ ] Chat messages persist across page reloads
- [ ] User can view and resume past conversations
- [ ] "New Chat" starts a fresh conversation
- [ ] All existing + new tests pass
- [ ] Folder-path indexing still works (backwards compatible)
