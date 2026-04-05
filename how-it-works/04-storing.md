# Storing and Searching Vectors

The storing step saves your embeddings (lists of numbers representing meaning)
in a vector database so you can search through them instantly when a question
arrives.

## What is a vector database?

A vector database is a search engine for meaning, not keywords. A regular
database finds rows where a column equals a value. A vector database finds
entries whose vectors are closest to a given vector — meaning it finds the
chunks whose meaning most closely matches your question.

Think of it like a library, but instead of searching by title or author, you
describe the topic you care about and the librarian hands you the most relevant
pages.

## Why ChromaDB?

rag-starter uses ChromaDB because it is the simplest option for getting
started:

- **Embedded** — it runs inside your Python process. No separate server to
  install, configure, or keep running.
- **File-based persistence** — your indexed data is saved to a folder
  (`./chroma_db/` by default) and survives restarts. You index once, then
  query as many times as you want.
- **Zero configuration** — no accounts, no API keys, no port numbers. It just
  works.

The tradeoff is scale. ChromaDB handles thousands of documents comfortably, but
if you grow to hundreds of thousands, you may want a dedicated vector database
like Qdrant or Pinecone. See the
[migration guide](../guides/migrate-vector-db.md) for when and how to switch.

## How cosine similarity works

When you ask a question, the pipeline embeds your question into a vector (the
same 768 numbers as your document chunks) and then compares it against every
stored vector. The comparison method is cosine similarity — it measures the
angle between two vectors rather than the distance between them.

Imagine two arrows pointing from the centre of a circle. If they point in
almost the same direction, their cosine similarity is close to 1 (very
similar). If they point in completely different directions, the similarity is
close to 0 (unrelated). The actual length of the arrows does not matter — only
the direction, which represents meaning.

ChromaDB returns a distance score (lower is better) rather than a similarity
score. A distance of 0.1 means the chunk is very relevant; a distance of 1.5
means it is probably not.

## What top-k retrieval does

You do not want every chunk in the database — just the most relevant ones. The
top-k parameter controls how many chunks are returned. With the default of
`top_k=5`, ChromaDB returns the 5 chunks with the lowest distance scores.

Choosing the right k involves a tradeoff:

- **Lower k (2-3)** — fewer chunks means less noise in the context, but you
  might miss relevant information spread across multiple chunks.
- **Higher k (10-20)** — more chunks means broader coverage, but irrelevant
  chunks can confuse the LLM or exceed the context window.

You can tune this per query:

```bash
python bring-your-own-docs/query.py "your question" --top-k 10
```

## What gets stored

For each chunk, ChromaDB stores three things:

1. **The vector** — the 768 numbers from the embedding step.
2. **The text** — the original chunk content, so it can be returned in results.
3. **The metadata** — the source filename, page number, and chunk index, so you
   know where each result came from.

## Persistence and re-indexing

Once you run the indexing command, your data is saved to disk at `./chroma_db/`.
You can close the terminal, shut down your computer, and come back later — the
index is still there. You only need to re-index if your documents change.

To check whether an index already exists:

```python
from src.store import store_exists
print(store_exists("./chroma_db"))  # True or False
```

## Next step

You now have a database full of vectors ready to be searched. The final step
is sending the retrieved chunks to an LLM to generate an answer. That is
[generation](05-generation.md).
