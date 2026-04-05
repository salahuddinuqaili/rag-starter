# What is RAG

Retrieval-Augmented Generation (RAG) gives a large language model access to
your private documents so it can answer questions using your actual data,
not just what it memorised during training.

## The Problem

Large language models like GPT and Llama are trained on public text from the
internet. They know nothing about your files -- your company wiki, your
research papers, your meeting notes. Ask about those and the model will
either hallucinate (generate a confident answer that is factually wrong) or
admit it does not know.

You might try pasting your documents into the chat, but that hits a ceiling
called the context window (the maximum text a model can read in one request,
measured in tokens -- roughly three-quarters of a word each). Even models
with large context windows lose accuracy when you dump in hundreds of pages
because the model has no way to know which paragraph matters.

## The Solution

RAG adds a search step before generation. Instead of feeding everything to
the model, you find only the relevant passages first, then send those
passages alongside the question. The model gets focused context and produces
an answer grounded in what your documents actually say. Think of it like
handing a research assistant a folder of highlighted excerpts rather than
pointing them at an entire filing cabinet.

## The Pipeline

A RAG system works in six stages. To make this concrete, imagine you have
50 internal company memos and you want to ask questions about them.

1. **Load** -- Read your documents (PDFs, markdown, text files) and extract
   raw text. For the 50 memos, this means opening every file and pulling out
   the words, stripping away formatting and page numbers.

2. **Chunk** -- Split each document into smaller, overlapping pieces, typically
   a few hundred characters each. You do this because you want to retrieve
   specific passages, not entire 10-page memos. Overlap (repeating the last
   few sentences at the start of the next chunk) ensures ideas on a boundary
   are not lost.

3. **Embed** -- Convert each chunk into an embedding (a list of numbers,
   typically 768, that captures the meaning of the text). These numbers form
   vectors (ordered lists of numbers representing a point in high-dimensional
   space). Similar ideas produce nearby vectors, which is what makes search
   possible. Your 50 memos might produce 400 chunks, each becoming one vector.

4. **Store** -- Save the chunks and their vectors in a vector database (a
   database designed for searching by meaning rather than exact keywords).
   Once built, you can search this index instantly without re-reading the
   original files.

5. **Retrieve** -- When you ask a question, the system embeds it the same way,
   producing a query vector. It searches the database for stored chunks whose
   vectors are closest to your query. You control how many come back with a
   setting called top-k (the number of most-similar chunks to return, commonly
   3 to 10). Ask "What was the outcome of the Q3 product review?" and the
   system pulls back the five chunks most related to that question.

6. **Generate** -- Send your question and the retrieved chunks to the language
   model. It reads only that focused context and writes an answer based on
   what the documents actually say. Because the context is small and relevant,
   you get a specific, grounded response instead of a vague or fabricated one.

## RAG vs Fine-Tuning

Fine-tuning means modifying the model's weights (the millions of internal
numbers learned during training) so new knowledge becomes baked into the
model itself. This requires a GPU, specially formatted training data, and
hours of compute. When your documents change next week, you fine-tune again.

RAG keeps your documents outside the model in a searchable index. When
information changes, you re-index and the system has immediate access. No
retraining, no GPU time, no waiting. For most use cases -- internal Q&A,
document search, customer support, onboarding -- RAG is faster, cheaper, and
easier to maintain. Fine-tuning still has its place for teaching a model a
new writing style or specialised vocabulary, but if your goal is "answer
questions about my documents," start with RAG.

## Limitations

**Retrieval quality is the bottleneck.** If the system pulls the wrong
chunks, the model generates a confident answer from irrelevant context.
Tuning chunk size, chunk overlap, and top-k makes a measurable difference
and is the single most effective way to improve answers.

**The answer must exist in your documents.** RAG cannot synthesise what is
not there. If your memos never mention Q4 revenue, no retrieval setting
will produce that number. A well-configured system says "I don't have enough
information" rather than guessing -- a poorly prompted one may hallucinate.

**Chunk boundaries can split context.** If a key fact spans two paragraphs
and the split falls between them, neither chunk tells the full story.
Increasing overlap helps but trades off against precision.

**Embedding models have blind spots.** Domain-specific jargon or acronyms
rare in the embedding model's training data may not be captured well. When
retrieval misses relevant passages, the problem is often in the embedding
step, not the language model.
