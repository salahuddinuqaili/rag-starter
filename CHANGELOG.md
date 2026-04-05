# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [0.1.0] - Unreleased

### Added

- Core RAG pipeline: load, chunk, embed, store, retrieve, generate
- Support for PDF, Markdown, and plain-text documents
- Local-first with Ollama (llama3.1:8b + nomic-embed-text)
- Optional OpenAI cloud path
- ChromaDB for persistent vector storage
- Quickstart script with health check and sample documents
- CLI tools: index_folder.py and query.py with interactive mode
- Streamlit web UI for chat-style Q&A
- 6 original sample documents covering diverse topics
- 5-part "How it Works" educational content
- Glossary, FAQ, and troubleshooting reference
- Jupyter notebooks for Colab (Groq) and local (Ollama)
- CI pipeline with ruff linting and pytest on Python 3.10 + 3.12
- Guide stubs for cloud LLM, tuning, LangChain, LlamaIndex, DOCX, and vector DB migration
