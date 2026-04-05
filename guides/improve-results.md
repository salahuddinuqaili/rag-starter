# Improve Your Results

Five tuning knobs that control the quality of your RAG answers, each with a
concrete experiment you can run in under five minutes. Start here when your
pipeline works but the answers are not good enough.

Every knob below is exposed as a CLI flag on `index_folder.py` or `query.py`,
so you can experiment without editing any code. When you find values that work,
you can hard-code them into your own scripts by passing the same parameters to
`index_documents()` and `query_documents()` in `src/pipeline.py`.


## Chunk Size

Chunk size controls how many characters of text go into each chunk before it is
embedded (turned into a list of numbers) and stored. It is the single biggest
lever you have over retrieval quality.

**Why it matters.** A smaller chunk size means each chunk covers a narrow topic,
so retrieval is more precise -- when a chunk matches your question, it is
probably relevant. But small chunks carry less surrounding context, so the LLM
may not have enough information to generate a complete answer. Larger chunks
carry more context but are more likely to contain irrelevant sentences alongside
the relevant ones, which can confuse the model.

**The tradeoff.** Too small (under 150) and your chunks become sentence
fragments that lack meaning on their own. Too large (over 2000) and you lose
the precision that makes retrieval useful -- you might as well paste the whole
document into the prompt.

### Try this

Index the same folder at three different chunk sizes and compare retrieval:

```bash
python bring-your-own-docs/index_folder.py ./sample-docs --chunk-size 200 --db-path ./chroma_200 --verbose
python bring-your-own-docs/query.py "What is overfitting?" --db-path ./chroma_200 --verbose

python bring-your-own-docs/index_folder.py ./sample-docs --chunk-size 500 --db-path ./chroma_500 --verbose
python bring-your-own-docs/query.py "What is overfitting?" --db-path ./chroma_500 --verbose

python bring-your-own-docs/index_folder.py ./sample-docs --chunk-size 1000 --db-path ./chroma_1000 --verbose
python bring-your-own-docs/query.py "What is overfitting?" --db-path ./chroma_1000 --verbose
```

Look at the retrieved chunks in the `--verbose` output. With 200 you will see
a tight, focused passage. With 1000 you will see a broader section that
includes surrounding paragraphs.

**Recommended starting values.** Use 500 (the default) as your baseline. Drop
to 200-300 for precise factual Q&A ("What year was X founded?"). Increase to
800-1000 for summarization or questions that need broader context ("Summarize
the key findings of this report").


## Chunk Overlap

Overlap controls how many characters from the end of one chunk are repeated at
the start of the next chunk. It exists to prevent losing context that falls
exactly on a chunk boundary.

**Why it matters.** Imagine a sentence that spans the border between two chunks.
Without overlap, the first chunk has the beginning of the sentence and the
second chunk has the end -- neither chunk contains the full thought, so neither
will match a query about that sentence. Overlap duplicates those boundary
characters so at least one chunk captures the complete idea.

**The tradeoff.** Too low (0) and you will get blind spots at every boundary.
Too high (say, 400 with a chunk size of 500) and most of your chunks are
redundant copies of each other, wasting storage and embedding compute without
improving retrieval.

### Try this

```bash
python bring-your-own-docs/index_folder.py ./sample-docs --chunk-overlap 0 --db-path ./chroma_ov0 --verbose
python bring-your-own-docs/query.py "How should meeting notes be shared?" --db-path ./chroma_ov0 --verbose

python bring-your-own-docs/index_folder.py ./sample-docs --chunk-overlap 100 --db-path ./chroma_ov100 --verbose
python bring-your-own-docs/query.py "How should meeting notes be shared?" --db-path ./chroma_ov100 --verbose
```

Compare whether the overlap-100 run retrieves a more complete passage around
the boundary.

**Recommended starting values.** Use 50 (the default) for most workloads. Bump
to 100 if you notice answers that seem to miss context you know is in the
documents -- this often means the relevant text was split across two chunks.
Stay below 20% of your chunk size (e.g., overlap 100 with chunk size 500).


## Top-k Retrieval

Top-k controls how many chunks are retrieved from the vector store and sent
to the LLM as context. It directly affects the signal-to-noise ratio in your
prompt.

**Why it matters.** A higher top-k gives the LLM more material to work with,
which helps for broad or multi-faceted questions ("Compare remote work policies
across all our office locations"). A lower top-k gives the LLM fewer, more
relevant chunks, which helps for focused factual questions where extra context
just adds noise.

**The tradeoff.** Too low (1-2) and you risk missing relevant chunks, especially
if the best chunk was not ranked first. Too high (20+) and you flood the LLM
context window with marginally relevant text, which can cause the model to
hallucinate or average across contradictory passages.

### Try this

```bash
python bring-your-own-docs/query.py "What neighbourhoods should I visit in Berlin?" --top-k 3 --verbose
python bring-your-own-docs/query.py "What neighbourhoods should I visit in Berlin?" --top-k 5 --verbose
python bring-your-own-docs/query.py "What neighbourhoods should I visit in Berlin?" --top-k 10 --verbose
```

With `--verbose` you will see each retrieved chunk and its distance score. Watch
how the later chunks at top-k 10 have higher distances (less relevant) and may
pull in content about food or transport that dilutes the neighbourhood answer.

**Recommended starting values.** Use 5 (the default) as your baseline. Drop to
3 for focused, single-fact questions. Increase to 8-10 for broad questions or
when your documents cover the same topic from different angles.


## Prompt Template

The prompt template is the instruction you give the LLM along with the
retrieved context. Editing it is the fastest way to change the style, format,
and accuracy of your answers without touching any retrieval logic.

**Why it matters.** The default template in `src/generator.py` tells the LLM to
answer based only on the provided context and to say "I don't have enough
information" when the context is insufficient. Changing the template lets you
control tone, length, citation style, and output format.

**The tradeoff.** A too-vague prompt gives the LLM freedom to hallucinate. A
too-restrictive prompt can cause it to refuse valid answers or produce
awkwardly constrained responses.

### Try this

Open `src/generator.py` and find the `RAG_PROMPT_TEMPLATE` variable near the
top of the file. Replace it with one of these alternatives and re-run a query.

**Concise answers** -- good for dashboards or chatbots where brevity matters:

```python
RAG_PROMPT_TEMPLATE = """Answer the question in 1-2 sentences using ONLY the context below. If the context does not contain the answer, say "Not found in documents."

Context:
{context}

Question: {question}

Answer:"""
```

**Cited sources** -- good for research or compliance use cases:

```python
RAG_PROMPT_TEMPLATE = """Answer the question using ONLY the context below. After your answer, list the source filenames you used in a "Sources:" section. If the context is insufficient, say so.

Context:
{context}

Question: {question}

Answer:"""
```

**Comparison format** -- good when the user is comparing options or topics:

```python
RAG_PROMPT_TEMPLATE = """Using ONLY the context below, compare the relevant options or approaches. Structure your answer with clear headings for each option and bullet points for pros and cons. If the context does not support a comparison, say so.

Context:
{context}

Question: {question}

Comparison:"""
```

After editing the template, test it without re-indexing -- the template only
affects the generation step:

```bash
python bring-your-own-docs/query.py "How does supervised learning differ from unsupervised?" --verbose
```

**Recommended starting point.** Keep the default template until you know your
use case. Switch to the concise template for chatbots. Switch to the cited
sources template when users need to verify answers against the original
documents.


## Embedding Model

The embedding model converts text into vectors (lists of numbers). Different
models produce vectors of different dimensions and capture meaning with
different levels of nuance.

**Why it matters.** A higher-quality embedding model produces vectors that
better capture semantic similarity, so retrieval returns more relevant chunks.
The tradeoff is speed and resource usage -- larger models are slower to embed
and produce bigger vectors that take more storage.

**The tradeoff.** `nomic-embed-text` (768 dimensions) is fast and good enough
for most use cases. `mxbai-embed-large` (1024 dimensions) captures finer
semantic distinctions but takes longer to embed and uses more memory. For
small document sets (under 1000 pages) the speed difference is negligible;
for large corpora it adds up.

### Try this

First, pull the alternative model:

```bash
ollama pull mxbai-embed-large
```

Then re-index your documents. You must re-index because the new model produces
different vectors -- you cannot mix embeddings from different models in the
same store.

```bash
python bring-your-own-docs/index_folder.py ./sample-docs --db-path ./chroma_mxbai --verbose
```

To actually use the new model, you need to pass it to the embedding functions.
Open `src/pipeline.py` and change the `model` argument in the `embed_texts()`
call inside `index_documents()` from `"nomic-embed-text"` to
`"mxbai-embed-large"`. Make the same change in the `embed_query()` call inside
`query_documents()`. Then run your query:

```bash
python bring-your-own-docs/query.py "What is the plate method for portion control?" --db-path ./chroma_mxbai --verbose
```

Compare the retrieved chunks and answer quality against the default
`nomic-embed-text` index.

**Recommended starting point.** Use `nomic-embed-text` (the default) until you
have evidence that retrieval quality is the bottleneck. Switch to
`mxbai-embed-large` if you see that the right chunks exist in your documents
but are not being retrieved. Remember: changing the embedding model always
requires a full re-index.


## Debugging Bad Results

When your answers are wrong, `--verbose` is your best diagnostic tool. It shows
you exactly which chunks were retrieved and how far they are from the query
vector. Use that output to figure out which part of the pipeline is failing.

### Retrieved chunks are wrong

The pipeline found the wrong passages. This is a retrieval problem.

- Try a smaller chunk size so each chunk is more focused.
- Try a different embedding model (`mxbai-embed-large`) for better semantic
  matching.
- Check that your documents actually contain the information you are asking
  about. Search them manually with `grep` or your editor.

### Retrieved chunks are right but the answer is wrong

The pipeline found the right passages but the LLM generated a bad answer.
This is a generation problem.

- Edit the prompt template to be more specific about the expected output
  format.
- Try a more capable LLM model: pass `--model llama3.1:70b` if you have
  enough VRAM, or switch to a cloud model (see `guides/use-cloud-llm.md`).
- Reduce top-k to cut noise -- fewer chunks means less for the LLM to
  get confused by.

### Results are empty or "I don't have enough information"

The pipeline found no relevant chunks, or the chunks were too far from the
query.

- Verify your documents were indexed: check that `./chroma_db/` (or your
  custom `--db-path`) exists and is not empty.
- Try a simpler, more direct question. "What is X?" works better than
  "Can you elaborate on the various aspects of X and its implications?"
- Increase top-k to cast a wider net.
- Check `--verbose` output for distance scores. If all distances are high
  (above 1.5), the query may be too different from the document vocabulary.
  Try rephrasing using words that appear in your documents.

## More Resources

- [How RAG Works](../how-it-works/README.md) — understand each pipeline stage
- [Glossary](../reference/glossary.md) — definitions for terms used in this guide
- [Troubleshooting](../reference/troubleshooting.md) — fix specific errors
- [Use a Cloud LLM](use-cloud-llm.md) — swap Ollama for OpenAI or Groq
