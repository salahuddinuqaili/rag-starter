# How RAG Works

RAG (Retrieval-Augmented Generation) gives an LLM access to your private
documents by retrieving relevant pieces before generating an answer. This
section walks you through each step of the pipeline, from raw files to a
grounded answer.

## The pipeline at a glance

```
 Your documents          Your question
      |                       |
      v                       v
 +-----------+          +-----------+
 | 1. LOAD   |          |           |
 +-----------+          |           |
      |                 |           |
      v                 |           |
 +-----------+          |           |
 | 2. CHUNK  |          |           |
 +-----------+          |           |
      |                 |           |
      v                 v           |
 +-----------+    +-----------+     |
 | 3. EMBED  |    | 3. EMBED  |     |
 +-----------+    +-----------+     |
      |                 |           |
      v                 v           |
 +-----------+    +-----------+     |
 | 4. STORE  |--->| 4. SEARCH |     |
 +-----------+    +-----------+     |
                        |           |
                        v           |
                  +-----------+     |
                  | 5. GENERATE|<---+
                  +-----------+
                        |
                        v
                     Answer
```

## RAG in 5 steps

### Step 1: Loading

Your documents arrive in different formats — PDFs, markdown files, plain text.
The loading step reads each file and converts it into a simple, uniform
structure: a block of text plus metadata (the filename and page number). This
gives every downstream step a consistent input to work with, regardless of the
original format.

Read more: [01-loading.md](01-loading.md)

### Step 2: Chunking

A single document can be thousands of words long, but you only need a few
relevant paragraphs to answer a question. The chunking step splits each
document into small, overlapping pieces (typically around 500 characters).
Smaller pieces mean more precise retrieval — the system can find exactly the
paragraph that matters instead of returning an entire chapter.

Read more: [02-chunking.md](02-chunking.md)

### Step 3: Embedding

Computers cannot search by meaning using raw text. The embedding step converts
each chunk into a list of 768 numbers (a vector) that captures what the text
means. Texts with similar meanings end up with similar numbers, which makes it
possible to find relevant chunks by comparing vectors instead of matching
keywords.

Read more: [03-embedding.md](03-embedding.md)

### Step 4: Storing and searching

The vectors are saved in a vector database (ChromaDB) so you do not have to
re-embed your documents every time you ask a question. When a question comes
in, the database compares the question's vector against every stored vector and
returns the closest matches — the chunks most likely to contain your answer.

Read more: [04-storing.md](04-storing.md)

### Step 5: Generation

The retrieved chunks are inserted into a prompt alongside your question. The
LLM reads this context and generates an answer grounded in your actual
documents, not its general training data. If the context does not contain
enough information, the model says so instead of making something up.

Read more: [05-generation.md](05-generation.md)

## Running the code

Every step maps directly to a file in the `src/` directory:

```
src/loader.py    → Step 1: Loading
src/chunker.py   → Step 2: Chunking
src/embedder.py  → Step 3: Embedding
src/store.py     → Step 4: Storing and searching
src/generator.py → Step 5: Generation
src/pipeline.py  → Orchestrates all five steps
```

You can run the entire pipeline with a single command:

```bash
python quickstart/my_first_rag.py --verbose
```

The `--verbose` flag prints what each stage is doing and how long it takes,
so you can see the pipeline in action.
