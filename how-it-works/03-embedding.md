# Embedding Text

[← Back to overview](README.md)

The embedding step converts each chunk of text into a list of numbers (called a
vector) that captures what the text means, so the pipeline can search by
meaning instead of by keywords.

## What is an embedding?

An embedding is a list of numbers — 768 numbers, to be exact, when using the
default model. Each number represents one dimension of meaning. You cannot read
individual numbers and say "this one means the text is about cooking," but
taken together, the 768 numbers form a unique fingerprint for that piece of
text.

The key property: **texts with similar meanings get similar numbers.** A chunk
about "async communication in distributed teams" and a chunk about "remote
collaboration and messaging" will produce vectors that are close to each other,
even though they share almost no words. This is what makes semantic search
(searching by meaning) possible.

## Why keywords are not enough

Traditional search matches exact words. If your document says "distributed
teams" but you search for "remote work," a keyword search finds nothing. An
embedding-based search finds it immediately because both phrases point to
nearly the same location in the 768-dimensional space.

This matters especially for RAG, where your users will phrase questions in
their own words, not the exact words your documents use.

## How nomic-embed-text works

rag-starter uses a model called nomic-embed-text, which runs locally through
Ollama. When you pass it a string of text, it returns a list of 768 floating-
point numbers. The model was trained on millions of text pairs so that related
texts produce similar vectors.

Because it runs locally, your documents never leave your machine. There is no
API call, no cloud service, and no cost per request. The tradeoff is speed —
embedding runs on your CPU (or GPU if available), and large document sets take
longer than a cloud API would.

## Embedding documents and queries the same way

A critical detail: you must embed your documents and your questions using the
same model. If the documents were embedded with nomic-embed-text, your question
must also be embedded with nomic-embed-text. Using different models produces
vectors in different "coordinate systems" that cannot be compared meaningfully.

This is why `src/embedder.py` exposes two functions that both use the same
model:

```python
# Embed all your document chunks (during indexing)
vectors = embed_texts(["chunk one text", "chunk two text"])

# Embed a question (during querying)
query_vector = embed_query("What are the best remote work practices?")
```

Both calls go through the same nomic-embed-text model, producing vectors in
the same 768-dimensional space.

## What the numbers look like

A single embedding is a list of 768 decimal numbers, typically between -1 and
1:

```
[0.0231, -0.1092, 0.0587, ..., -0.0341]   # 768 numbers total
```

You never need to read or interpret these numbers directly. They exist so the
vector database (the next step) can compare them mathematically.

## Cloud alternative

If you prefer speed or do not want to run models locally, you can use OpenAI's
embedding API instead. Set the `OPENAI_API_KEY` environment variable and use
the `embed_texts_openai()` function. See the
[cloud LLM guide](../guides/use-cloud-llm.md) for details.

## Next step

Now that every chunk is a vector, you need somewhere to store them and a way to
search through them. That is [storing](04-storing.md).
