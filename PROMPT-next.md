# Next Stage Prompt

Paste this into a new Claude Code session.

---

```
This project just shipped v0.2 (FastAPI + React web app with multi-collection,
chat history, and document management). The core RAG library (src/) is stable.

Three tasks for this session, in priority order:

## 1. Backend API tests

Add tests for the new backend endpoints in tests/test_api.py. Use FastAPI's
TestClient (from starlette.testclient). Mock all Ollama calls — tests must
pass without Ollama.

Test at minimum:
- GET /api/health returns { ollama, models }
- POST/GET/DELETE /api/collections CRUD lifecycle
- POST /api/collections/{name}/upload with a .txt fixture
- GET /api/collections/{name}/documents returns uploaded file
- DELETE /api/collections/{name}/documents/{source} removes it
- POST/GET/DELETE /api/conversations lifecycle
- POST /api/conversations/{id}/messages adds messages
- GET /api/conversations/{id} returns messages in order

## 2. Flesh out guide stubs

Five guides under guides/ are currently headers + TODOs. Write real content
for each (~100-150 lines). Use guides/improve-results.md as the structural
template (it's 298 lines and fully fleshed out).

Guides to write:
- guides/use-cloud-llm.md — OpenAI/Groq setup, .env config, model selection
- guides/use-langchain.md — rebuild the pipeline with LangChain
- guides/use-llamaindex.md — rebuild with LlamaIndex
- guides/add-docx-support.md — add python-docx, extend loader.py
- guides/migrate-vector-db.md — when/how to move from ChromaDB to Pinecone/Weaviate/pgvector

Follow the writing rules in CLAUDE.md. Every guide should be copy-pasteable
and end with a "Next Steps" section linking to related content.

## 3. Update Colab notebook

The Colab notebook (notebooks/rag_starter_colab.ipynb) still uses the old
quickstart flow. Update it to mention the web app as the primary interface
and add a cell showing the new collection/upload API.

Create branch feat/api-tests-and-guides for all three tasks.
```
