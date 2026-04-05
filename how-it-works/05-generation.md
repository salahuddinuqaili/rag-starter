# Generating Answers

[← Back to overview](README.md)

The generation step sends your question and the retrieved chunks to a large
language model (LLM), which reads the context and produces a grounded answer
based on your actual documents.

## How it works

By this point, the pipeline has already found the most relevant chunks from
your documents. The generation step assembles them into a single prompt that
looks like this:

```
You are a helpful assistant. Answer the question based ONLY on the
following context. If the context doesn't contain enough information
to answer, say "I don't have enough information to answer that."

Context:
[chunk 1 text]
---
[chunk 2 text]
---
[chunk 3 text]

Question: What are the best practices for async communication?

Answer:
```

The LLM reads this prompt and generates an answer. Because the prompt
explicitly tells the model to use only the provided context, the answer is
grounded in your documents rather than the model's general training data.

## Why grounding matters

Without RAG, an LLM answers from memory — the data it was trained on. That
training data might be outdated, incomplete, or simply wrong about your
specific domain. Worse, LLMs are confident even when they are wrong, a
behaviour called hallucination (generating plausible-sounding but incorrect
information).

Grounding the model in retrieved context reduces hallucination because the
model has the actual source text in front of it. It does not eliminate
hallucination entirely — the model can still misinterpret context or combine
chunks in misleading ways — but it dramatically improves accuracy for questions
your documents can answer.

## The prompt template

The prompt template is the most important piece of "configuration" in the
entire pipeline. It lives as a plain string constant in `src/generator.py`,
and you are encouraged to edit it.

A few things the default template does deliberately:

- **"Based ONLY on the following context"** — prevents the model from mixing in
  outside knowledge. Remove this constraint if you want the model to supplement
  with its general knowledge.
- **"Say I don't have enough information"** — teaches the model to admit
  ignorance instead of guessing. This is critical for trust.
- **Context chunks separated by `---`** — the dashes help the model distinguish
  between different source passages.

If your results are not good enough, tuning the prompt is often more effective
than changing the chunk size or model. See
[improve results](../guides/improve-results.md) for experiments you can try.

## How Ollama runs models locally

rag-starter uses Ollama to run LLMs on your own machine. Ollama downloads the
model weights once (about 4.7 GB for llama3.1:8b) and runs inference locally.
Your questions and documents never leave your computer — there is no API call,
no cloud service, and no usage cost.

The default model is llama3.1:8b, an 8-billion-parameter model that balances
quality with speed on consumer hardware. If you have a GPU with enough VRAM
(8 GB or more), Ollama will use it automatically. On CPU alone, expect answers
in 10-30 seconds depending on length.

You can swap the model with the `--model` flag:

```bash
python bring-your-own-docs/query.py "your question" --model mistral
```

Any model available through Ollama works — just pull it first with
`ollama pull model-name`.

## When context is insufficient

Sometimes the retrieved chunks do not contain enough information to answer the
question. This happens when:

- The question is about a topic your documents do not cover.
- The relevant information was not retrieved (try increasing `--top-k`).
- The chunks are too small and the answer spans multiple chunks that were not
  all retrieved.

In these cases, the default prompt template instructs the model to say "I don't
have enough information to answer that." This is the correct behaviour — a
system that admits its limits is more trustworthy than one that invents answers.

## Cloud alternative

If you want faster generation or access to more powerful models like GPT-4,
you can switch to OpenAI's API by setting the `OPENAI_API_KEY` environment
variable. See the [cloud LLM guide](../guides/use-cloud-llm.md) for a
three-line code change.

## Wrapping up

You have now seen every step of the RAG pipeline: loading documents, chunking
them into pieces, embedding those pieces into vectors, storing and searching
those vectors, and generating answers from the retrieved context.

To run the full pipeline yourself:

```bash
python quickstart/my_first_rag.py --verbose
```

To use it on your own documents:

```bash
python bring-your-own-docs/index_folder.py ~/my-docs --verbose
python bring-your-own-docs/query.py "your question here" --verbose
```

## What's Next?

- [Improve Your Results](../guides/improve-results.md) — tune chunk size, prompts, and retrieval
- [Glossary](../reference/glossary.md) — definitions for all technical terms
- [Troubleshooting](../reference/troubleshooting.md) — fix common issues
- [Use Your Own Documents](../bring-your-own-docs/README.md) — try it on your files
