"""SQLite helpers for collection metadata and conversation persistence."""

import json
import sqlite3
import uuid
from datetime import datetime, timezone

DB_PATH = "./rag_starter.db"


def _now() -> str:
    """Return current UTC time as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def get_db() -> sqlite3.Connection:
    """Open a SQLite connection with row factory and foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Create tables if they don't exist and ensure default collection."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS collections (
            name       TEXT PRIMARY KEY,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS conversations (
            id         TEXT PRIMARY KEY,
            collection TEXT NOT NULL,
            title      TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS messages (
            id              TEXT PRIMARY KEY,
            conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
            role            TEXT NOT NULL,
            content         TEXT NOT NULL,
            sources         TEXT,
            created_at      TEXT NOT NULL,
            position        INTEGER NOT NULL
        );
    """)
    conn.execute(
        "INSERT OR IGNORE INTO collections (name, created_at) VALUES (?, ?)",
        ("documents", _now()),
    )
    conn.commit()
    conn.close()


# --- Collections ---

def create_collection(name: str) -> dict:
    """Insert a new collection and return it."""
    conn = get_db()
    conn.execute("INSERT INTO collections (name, created_at) VALUES (?, ?)", (name, _now()))
    conn.commit()
    row = conn.execute("SELECT * FROM collections WHERE name = ?", (name,)).fetchone()
    conn.close()
    return dict(row)


def list_collections() -> list[dict]:
    """Return all collections ordered by creation date."""
    conn = get_db()
    rows = conn.execute("SELECT * FROM collections ORDER BY created_at").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_collection(name: str) -> None:
    """Delete a collection and its conversations."""
    conn = get_db()
    conn.execute("DELETE FROM conversations WHERE collection = ?", (name,))
    conn.execute("DELETE FROM collections WHERE name = ?", (name,))
    conn.commit()
    conn.close()


# --- Conversations ---

def create_conversation(collection: str) -> dict:
    """Create a new conversation linked to a collection."""
    conn = get_db()
    conv_id = str(uuid.uuid4())
    now = _now()
    conn.execute(
        "INSERT INTO conversations (id, collection, title, created_at, updated_at)"
        " VALUES (?, ?, ?, ?, ?)",
        (conv_id, collection, None, now, now),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,)).fetchone()
    conn.close()
    return dict(row)


def list_conversations(collection: str | None = None) -> list[dict]:
    """Return conversations, optionally filtered by collection."""
    conn = get_db()
    if collection:
        rows = conn.execute(
            "SELECT * FROM conversations WHERE collection = ? ORDER BY updated_at DESC",
            (collection,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM conversations ORDER BY updated_at DESC"
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_conversation(conv_id: str) -> dict | None:
    """Return a conversation with its messages, or None if not found."""
    conn = get_db()
    conv = conn.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,)).fetchone()
    if not conv:
        conn.close()
        return None
    msgs = conn.execute(
        "SELECT * FROM messages WHERE conversation_id = ? ORDER BY position",
        (conv_id,),
    ).fetchall()
    conn.close()
    result = dict(conv)
    result["messages"] = [
        {**dict(m), "sources": json.loads(m["sources"]) if m["sources"] else None}
        for m in msgs
    ]
    return result


def delete_conversation(conv_id: str) -> None:
    """Delete a conversation and its messages (cascade)."""
    conn = get_db()
    conn.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
    conn.commit()
    conn.close()


def add_message(
    conv_id: str, role: str, content: str, sources: list | None = None,
) -> dict:
    """Append a message to a conversation. Auto-sets title on first user message."""
    conn = get_db()
    msg_id = str(uuid.uuid4())
    now = _now()
    row = conn.execute(
        "SELECT COALESCE(MAX(position), -1) + 1 as next_pos"
        " FROM messages WHERE conversation_id = ?",
        (conv_id,),
    ).fetchone()
    position = row["next_pos"]
    sources_json = json.dumps(sources) if sources else None
    conn.execute(
        "INSERT INTO messages (id, conversation_id, role, content, sources, created_at, position)"
        " VALUES (?, ?, ?, ?, ?, ?, ?)",
        (msg_id, conv_id, role, content, sources_json, now, position),
    )
    conn.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conv_id))
    if position == 0 and role == "user":
        conn.execute(
            "UPDATE conversations SET title = ? WHERE id = ?", (content[:60], conv_id)
        )
    conn.commit()
    conn.close()
    return {"id": msg_id, "role": role, "content": content, "sources": sources}
