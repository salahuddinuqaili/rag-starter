# PROMPT.md — Paste this into Claude Code

> Drop this file in `C:\Users\mulli\projects\rag-starter\` alongside `CLAUDE.md` before running Claude Code. Then paste the prompt below into Claude Code CLI.

---

## The Prompt

```
Read CLAUDE.md in this directory. It contains the complete project specification for rag-starter — a beginner-friendly RAG repository.

Build the entire repository by executing these phases in strict order. Do NOT skip ahead — later phases import from earlier ones.

PHASE 1 — Skeleton:
Create .gitignore, .env.example, LICENSE (MIT, 2025, "rag-starter contributors"), src/__init__.py, tests/__init__.py, quickstart/requirements.txt, and requirements-dev.txt. All specs are in CLAUDE.md.

PHASE 2 — Core module (src/):
Create all 6 files in src/ following the exact function signatures, type hints, docstrings, and error handling specified in CLAUDE.md under "Phase 2: Core module." Build in this order: loader.py → chunker.py → embedder.py → store.py → generator.py → pipeline.py. Each file must be <150 lines of code. Use logging (not print) in src/ files. Every function needs a plain-English docstring.

PHASE 3 — Quickstart:
Create quickstart/check.py, quickstart/my_first_rag.py, quickstart/install.sh, quickstart/install.ps1. These import from src/. check.py verifies Python, packages, Ollama, and models with ✓/✗ output. my_first_rag.py indexes sample-docs/ and asks 3 hardcoded cross-topic questions, printing answers with sources. Both support --verbose.

PHASE 4 — Bring your own docs:
Create bring-your-own-docs/README.md, index_folder.py, query.py, app.py. All three Python scripts use argparse and import from src.pipeline only (no direct calls to src/embedder or src/store). app.py is a Streamlit single-file app with sidebar controls and chat-style Q&A. query.py has an interactive mode (loop) when no question argument is given.

PHASE 5 — Content:
Create all 6 sample-docs/ markdown files (remote-work-best-practices.md, project-management-fundamentals.md, intro-to-machine-learning.md, healthy-eating-guide.md, berlin-travel-guide.md, what-is-rag.md) plus sample-docs/README.md. Each is 400-500 words of ORIGINAL content (CC0), written in the specific voice described in CLAUDE.md (company guide, training doc, explainer, wellness guide, travel blog, meta-explainer). Then create all how-it-works/ files (README.md, 01-loading.md through 05-generation.md) and all reference/ files (glossary.md with 25 terms, faq.md with 10 Q&As, troubleshooting.md with 10 issues).

PHASE 6 — Tests:
Create tests/conftest.py with shared fixtures (sample_text, sample_documents, mock_embeddings using deterministic 768-dim vectors, temp_chroma_path via tmp_path). Then test_chunker.py, test_loader.py, test_check.py, test_retrieval.py. All tests must pass WITHOUT Ollama installed — mock all LLM/embedding calls. Use plain assert statements, no unittest classes.

PHASE 7 — GitHub + docs:
Create .github/workflows/ci.yml (matrix: Python 3.10 + 3.12, install deps, ruff check, pytest), all 3 issue templates, PR template, CONTRIBUTING.md, CHANGELOG.md. Then create README.md LAST — it's the most important file. Follow the exact structure in CLAUDE.md: H1 + tagline + badges, one-sentence pitch, GIF placeholder, three-path quickstart (Colab/Local/Cloud), "Use on YOUR docs" section, then links to how-it-works, guides, FAQ, contributing.

PHASE 8 — Notebooks:
Create notebooks/rag_starter_colab.ipynb (uses Groq free tier since Ollama can't run in Colab, includes inline sample text, every cell has markdown explanation above it, ends with "try your own" cell) and notebooks/rag_starter_local.ipynb (uses Ollama locally, prerequisite check cell).

PHASE 9 — Guides (create as stubs with headers and TODOs):
Create guides/use-cloud-llm.md, improve-results.md, use-langchain.md, use-llamaindex.md, add-docx-support.md, migrate-vector-db.md. These are P2 (post-launch) — write the intro paragraph and section headers with TODO markers for full content.

After all phases complete:
1. Run `ruff check .` and fix any issues
2. Run `pytest tests/ -v` and fix any failures
3. Verify the directory tree matches the structure in CLAUDE.md
4. Report: total files created, any issues encountered, and which files are ready vs. need manual attention
```
