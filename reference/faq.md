# Frequently Asked Questions

Ten questions that come up most often when people start using rag-starter.

## Do I need a GPU?

No. rag-starter runs on CPU by default, and Ollama handles the heavy lifting.
A modern laptop with 8 GB of RAM is enough for the default models. Responses
will be slower than on a GPU (expect 10-30 seconds per answer instead of 2-5),
but everything works. If you have an NVIDIA GPU with at least 8 GB of VRAM,
Ollama will use it automatically and you will see a significant speed boost.

## Is my data sent to the cloud?

No. By default, everything stays on your machine. Ollama runs the language
model and embedding model locally, and ChromaDB stores your vectors on your
local disk. Your documents never leave your computer unless you explicitly
switch to a cloud provider like OpenAI by setting the `OPENAI_API_KEY`
environment variable.

## Can I use this at work with confidential documents?

Yes, as long as you stick with the local Ollama setup (the default). Since no
data leaves your machine, rag-starter is safe for internal documents, contracts,
and other sensitive files. If you switch to a cloud LLM, your document chunks
will be sent to that provider's API, so check your company's data policies first.

## How much does it cost?

Nothing. Every component in the default stack is free and open-source: Python,
Ollama, ChromaDB, and the models (llama3.1:8b, nomic-embed-text). The only cost
is disk space (~4.7 GB for the two models) and your electricity. If you choose
to use OpenAI or another cloud LLM, you will pay per-token according to that
provider's pricing.

## What file types are supported?

rag-starter supports PDF (`.pdf`), Markdown (`.md`), and plain text (`.txt`)
files out of the box. PDF loading uses PyMuPDF, which handles most PDFs well
including multi-page reports. Scanned-image PDFs (without an embedded text layer)
are not supported yet. DOCX support is on the roadmap -- see
`guides/add-docx-support.md` for a guide on adding it yourself.

## How is this different from ChatGPT?

ChatGPT only knows what it was trained on and cannot read your private files.
rag-starter retrieves relevant passages from your own documents and feeds them
to the language model so it can answer based on your data. Think of it as the
difference between asking a stranger a question and asking someone who has
just read your files.

## Can I use a different LLM?

Yes. Pass `--model <model-name>` to any CLI command or set the `model` parameter
in code. Any model available through Ollama works (run `ollama list` to see what
you have installed). You can also use OpenAI models by setting the
`OPENAI_API_KEY` environment variable -- see `guides/use-cloud-llm.md` for
instructions.

## How many documents can this handle?

ChromaDB can comfortably handle tens of thousands of chunks on a single machine,
which translates to hundreds or even a few thousand documents depending on their
length. If you are working with more than 100,000 chunks or need multi-user
access, consider migrating to a dedicated vector database like Qdrant or
Pinecone -- see `guides/migrate-vector-db.md`.

## What if my results are bad?

Start by checking three things: chunk size, top-k, and your prompt template.
Smaller chunks (200-300 characters) work better for precise factual questions,
while larger chunks (800-1000) preserve more context for nuanced answers.
Increasing top-k from 5 to 10 gives the model more context to work with. See
`guides/improve-results.md` for a full tuning guide with experiments you can try.

## Can I contribute?

Absolutely. Check out `CONTRIBUTING.md` for how to file issues, submit pull
requests, and set up a development environment. Good first issues are labelled
`good first issue` on GitHub. Adding DOCX support, writing a new sample
document, or improving an explainer in `how-it-works/` are all great places
to start.

## More Resources

- [Glossary](glossary.md) — definitions for every technical term
- [Troubleshooting](troubleshooting.md) — fix specific errors
- [How RAG Works](../how-it-works/README.md) — the full pipeline explained
- [Improve Your Results](../guides/improve-results.md) — 5 tuning knobs with experiments
