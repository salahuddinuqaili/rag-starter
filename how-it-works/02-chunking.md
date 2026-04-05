# Chunking Text

[← Back to overview](README.md)

The chunking step splits your documents into small, overlapping pieces so the
pipeline can retrieve the specific paragraphs that answer your question, rather
than returning entire files.

## Why not use whole documents?

Two practical reasons force you to break documents into chunks:

1. **LLMs have context limits.** Even large models can only read a fixed amount
   of text at once (the context window). If you try to paste five full
   documents into a prompt, you will exceed that limit.
2. **Smaller pieces retrieve better.** When someone asks "What is the plate
   method for portion control?", you want to return the two paragraphs that
   discuss it — not a 3,000-word nutrition guide. Smaller chunks mean the
   search step can be more precise.

## How the recursive character splitter works

rag-starter uses a hand-written recursive splitter instead of a framework. It
tries to break text at natural boundaries, starting with the largest and
falling back to smaller ones:

1. **Paragraph breaks** (`\n\n`) — the best split point, because paragraphs
   are self-contained units of thought.
2. **Line breaks** (`\n`) — useful for lists and bullet points where double
   newlines are missing.
3. **Sentence endings** (`. `) — splits mid-paragraph while keeping full
   sentences intact.
4. **Spaces** (` `) — splits between words as a last resort before the final
   fallback.
5. **Characters** — only used when a single word is longer than the chunk size,
   which is rare in normal text.

The splitter tries each level in order. If a piece of text fits within the
chunk size after splitting on paragraphs, it stops there. If not, it takes the
oversized pieces and tries the next level down.

## What overlap does

When you split text into chunks, you can lose context at the boundaries. Imagine
a sentence that starts at the end of chunk 3 and finishes at the beginning of
chunk 4 — if you only retrieve chunk 4, you miss the setup.

Overlap fixes this by repeating the last N characters of each chunk at the
start of the next one. With the default overlap of 50 characters, the tail end
of chunk 3 also appears at the beginning of chunk 4. This means either chunk
can stand on its own without losing the connecting sentence.

## How chunk size affects quality

The default chunk size is 500 characters, which is roughly a long paragraph.
This is a good starting point, but you can tune it:

- **Smaller chunks (200-300)** — more precise retrieval, but each chunk carries
  less context. Good for factual Q&A where answers are short.
- **Larger chunks (800-1500)** — each chunk carries more context, but retrieval
  is less precise. Good for summarisation or questions that need broader
  background.

You can experiment with chunk size using the `--chunk-size` flag:

```bash
python bring-your-own-docs/index_folder.py ~/my-docs --chunk-size 300 --verbose
```

## Metadata survives chunking

Each chunk inherits the metadata from its parent Document — the source filename
and page number. The chunker also adds a `chunk_index` so you can trace every
chunk back to its position in the original file. This metadata is what powers
the "Source:" lines you see in query results.

## Next step

Now that your text is in small, manageable pieces, each piece needs to be
converted into numbers that capture its meaning. That is
[embedding](03-embedding.md).
