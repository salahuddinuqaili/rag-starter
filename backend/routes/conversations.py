"""Routes for conversation and message persistence."""

from fastapi import APIRouter  # APIRouter groups related endpoints
from fastapi.responses import JSONResponse
from pydantic import BaseModel  # Request validation — bundled with FastAPI

from backend.db import (
    add_message,
    create_conversation,
    delete_conversation,
    get_conversation,
    list_conversations,
)

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


class ConversationCreate(BaseModel):
    """Body for POST /api/conversations."""

    collection: str


class MessageCreate(BaseModel):
    """Body for POST /api/conversations/{id}/messages."""

    role: str
    content: str
    sources: list | None = None


@router.get("")
def list_all(collection: str | None = None) -> list[dict]:
    """List conversations, optionally filtered by collection name."""
    return list_conversations(collection)


@router.post("")
def create(body: ConversationCreate) -> dict:
    """Create a new conversation linked to a collection."""
    return create_conversation(body.collection)


@router.get("/{conv_id}", response_model=None)
def get(conv_id: str) -> dict | JSONResponse:
    """Get a conversation with all its messages."""
    result = get_conversation(conv_id)
    if not result:
        return JSONResponse(status_code=404, content={"error": "Not found"})
    return result


@router.delete("/{conv_id}", status_code=204)
def delete(conv_id: str) -> None:
    """Delete a conversation and all its messages."""
    delete_conversation(conv_id)


@router.post("/{conv_id}/messages")
def post_message(conv_id: str, body: MessageCreate) -> dict:
    """Add a message to a conversation."""
    return add_message(conv_id, body.role, body.content, body.sources)
