# Contributing to rag-starter

Thanks for your interest in contributing! This project is designed to be
beginner-friendly — both for users and contributors.

## Filing issues

Use the issue templates on GitHub:

- **Bug report** — Something isn't working. Include your OS, Python version,
  and the full error output.
- **Workflow request** — You want to use RAG for a specific use case and need
  guidance or a new feature.
- **Beginner question** — No question is too basic. We've all been there.

## Submitting a pull request

1. **Fork** the repository and clone your fork.
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Install dev dependencies:**
   ```bash
   pip install -r quickstart/requirements.txt
   pip install -r requirements-dev.txt
   ```
4. **Make your changes.** Follow the code rules below.
5. **Run tests and lint:**
   ```bash
   pytest tests/ -v
   ruff check .
   ```
6. **Commit** with a clear message in imperative mood:
   ```
   Add DOCX support to loader
   ```
7. **Push** and open a pull request against `main`.

## Code style

- **Functions over classes.** No class hierarchies.
- **Type hints everywhere.** Every function signature needs annotations.
- **Docstrings on every function.** Plain English, no jargon.
- **Max 150 lines of code per file** (excluding comments and docstrings).
- **No print() in src/ files.** Use `logging` in library code.
- Run `ruff check .` and `ruff format .` before committing.

For the full set of rules, see the Code Rules section in
[CLAUDE.md](CLAUDE.md).

## Good first issues

Look for issues labelled
[good first issue](../../labels/good%20first%20issue) — these are scoped,
well-described tasks that are a great way to get started. The
[add DOCX support guide](guides/add-docx-support.md) is specifically
designed as a first contribution.

## Development setup

```bash
# Clone
git clone https://github.com/salahuddinuqaili/rag-starter.git
cd rag-starter

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows

# Install all dependencies
pip install -r quickstart/requirements.txt
pip install -r requirements-dev.txt

# Run the test suite
pytest tests/ -v

# Run the linter
ruff check .
```

## Questions?

Open a [beginner question](../../issues/new?template=beginner_question.md)
issue — we're happy to help.
