# What is RAG

Retrieval-Augmented Generation (RAG) is a technique that lets a large language model
(LLM) answer questions using your own documents instead of relying solely on what
it learned during training. This document explains how it works in plain English.

## The Problem

LLMs like GPT and Llama are trained on vast amounts of public text, but they have
no knowledge of your private files — your company wiki, your research papers, your
meeting notes. If you ask an LLM a question about your internal documentation, it
will either hallucinate (make up a plausible-sounding but wrong answer) or admit it
does not know.

You could paste your documents into the chat prompt, but that hits a practical
limit fast. Most LLMs have a context window (the maximum amount of text they can
process at once) measured in thousands of tokens. Your document collection might be
hundreds of pages. You cannot fit it all in.

## The Solution

RAG solves this by adding a retrieval step before generation. Instead of feeding
the entire document collection to the LLM, you find just the relevant passages
first, then send only those passages along with the question. The LLM gets focused
context and produces a grounded answer.

## The Pipeline

A RAG system has six stages:

1. **Load** — Read your documents (PDFs, markdown files, text files) and extract
   the raw text from each one.

2. **Chunk** — Split the text into smaller pieces, typically a few hundred
   characters each. This is necessary because you want to retrieve specific
   passages, not entire documents.

3. **Embed** — Convert each chunk into an embedding (a list of numbers that
   captures the meaning of the text). Similar ideas produce similar numbers,
   which is how search works later.

4. **Store** — Save the chunks and their embeddings in a vector database (a
   database designed for searching by similarity rather than by exact keywords).

5. **Retrieve** — When a user asks a question, embed the question using the same
   method, then find the stored chunks with the most similar embeddings. These
   are your "relevant context."

6. **Generate** — Send the question and the retrieved chunks to the LLM. The model
   reads the context and writes an answer based on what the documents actually say.

## RAG vs. Fine-Tuning

Fine-tuning means retraining the LLM itself on your data so the knowledge becomes
part of the model's weights. This is expensive, time-consuming, and hard to update
when your documents change.

RAG is cheaper and more flexible. You update your documents, re-index them, and the
system immediately has access to the new information. No retraining required. For
most use cases — internal Q&A, document search, customer support — RAG is the
better starting point.

## Limitations

RAG is not magic. The quality of your answers depends heavily on the retrieval step.
If the system pulls the wrong chunks, the LLM will generate a confident answer
based on irrelevant context. Tuning chunk size, overlap, and the number of results
retrieved (top-k) can make a significant difference.

RAG also does not help if the answer is not in your documents at all. The LLM can
only work with the context you give it. If your documents do not cover a topic, RAG
cannot invent the information — and a well-configured system will tell you "I don't
have enough information" rather than guessing.
