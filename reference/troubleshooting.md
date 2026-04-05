# Troubleshooting

Solutions to the ten most common problems you will hit when running rag-starter.
Each section describes the problem, explains the cause, and gives you a
copy-pasteable fix.

## Ollama Not Found

You see `ollama: command not found` or `'ollama' is not recognized` when
running a script.

**Cause.** Ollama is not installed, or its binary is not on your system PATH.
This usually means you downloaded Ollama but haven't completed the installation
step that adds it to your shell.

**Fix.** Install Ollama from the official site and restart your terminal so the
PATH update takes effect.

```bash
# macOS / Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download the installer from https://ollama.ai and run it.
# After installation, close and reopen your terminal.
```

Verify it worked:

```bash
ollama --version
```

## Model Not Found

You see `model 'llama3.1:8b' not found` or a similar message when running
a query.

**Cause.** The model has not been downloaded yet. Ollama requires you to pull
(download) each model before you can use it.

**Fix.** Pull the required models. The first run downloads several gigabytes,
so it may take a few minutes on a slow connection.

```bash
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

Verify both are available:

```bash
ollama list
```

## Connection Refused

You see `ConnectionError: Could not connect to Ollama` or
`connection refused on localhost:11434`.

**Cause.** The Ollama service is not running. Ollama needs a background process
(`ollama serve`) to handle requests, and it does not always start automatically
after a reboot.

**Fix.** Start the Ollama service.

```bash
ollama serve
```

On macOS, you can also launch the Ollama desktop app, which starts the service
automatically. On Linux, if you installed via the official script, the service
should be managed by systemd:

```bash
sudo systemctl start ollama
```

## ChromaDB Permission Error

You see `PermissionError: [Errno 13] Permission denied: './chroma_db'` when
indexing or querying.

**Cause.** The `chroma_db/` directory was created by a different user or with
restricted permissions, often because a previous run used `sudo` or a different
Python environment.

**Fix.** Take ownership of the directory, or delete it and re-index.

```bash
# Option 1: Fix permissions (Linux/macOS)
sudo chown -R $(whoami) ./chroma_db

# Option 2: Delete and re-index
rm -rf ./chroma_db
python bring-your-own-docs/index_folder.py /path/to/your/docs
```

On Windows, right-click the `chroma_db` folder, go to Properties > Security,
and grant your user Full Control.

## Empty Results

Your query returns an answer like "I don't have enough information" even though
you know the answer is in your documents.

**Cause.** This usually means one of three things: the documents were not indexed
successfully, the chunks are too large for the question (so the relevant sentence
is buried in a long chunk and does not rank highly), or the embedding model is
not capturing the right meaning.

**Fix.** First, confirm that indexing actually completed by checking for the
`chroma_db/` directory and running a simple query with `--verbose` to see which
chunks are retrieved.

```bash
python bring-your-own-docs/query.py "test question" --verbose
```

If chunks are being retrieved but they are not relevant, try reducing the chunk
size and re-indexing:

```bash
rm -rf ./chroma_db
python bring-your-own-docs/index_folder.py /path/to/docs --chunk-size 300 --verbose
```

## Slow Responses

Queries take 30 seconds or longer to return an answer.

**Cause.** The language model is running on CPU, which is significantly slower
than GPU inference. The default model (llama3.1:8b) needs about 5 GB of memory
and benefits heavily from GPU acceleration.

**Fix.** If you have an NVIDIA GPU with at least 8 GB of VRAM, make sure you
have the latest NVIDIA drivers installed -- Ollama will detect and use the GPU
automatically. You can verify GPU usage by running:

```bash
ollama ps
```

If you do not have a GPU, you can switch to a smaller model for faster
responses:

```bash
python bring-your-own-docs/query.py "your question" --model llama3.2:3b
```

Alternatively, use a cloud LLM for faster inference -- see
`guides/use-cloud-llm.md`.

## Out of Memory

You see `OutOfMemoryError`, `CUDA out of memory`, or the process gets killed
by the OS during indexing or querying.

**Cause.** The model does not fit in your available RAM (for CPU) or VRAM
(for GPU). The llama3.1:8b model needs roughly 5 GB, and ChromaDB keeps some
data in memory during indexing.

**Fix.** Close other memory-intensive applications and try again. If that is
not enough, switch to a smaller model:

```bash
ollama pull llama3.2:3b
python bring-your-own-docs/query.py "your question" --model llama3.2:3b
```

For large document collections, index in batches by splitting your documents
across multiple folders and indexing each one separately.

## Python Version Error

You see `SyntaxError` on lines with type hints like `list[str]`, or the
install script reports that your Python version is too old.

**Cause.** rag-starter requires Python 3.10 or newer. The `list[str]` syntax
for type hints was introduced in Python 3.9, and some dependencies require
3.10+.

**Fix.** Check your Python version and upgrade if needed.

```bash
python --version
```

If you see 3.9 or older, install a newer version:

```bash
# macOS (with Homebrew)
brew install python@3.12

# Ubuntu / Debian
sudo apt update && sudo apt install python3.12

# Windows
# Download from https://www.python.org/downloads/ and run the installer.
# Make sure to check "Add Python to PATH" during installation.
```

After installing, verify the new version is active:

```bash
python3.12 --version
```

## Import Errors

You see `ModuleNotFoundError: No module named 'chromadb'` or similar errors
for any dependency.

**Cause.** The required Python packages are not installed in the active
environment, or you are running a different Python interpreter than the one
where you installed the packages.

**Fix.** Make sure you are in the correct virtual environment and install the
dependencies.

```bash
# Activate the virtual environment (if you created one during setup)
# Linux / macOS
source .venv/bin/activate
# Windows
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r quickstart/requirements.txt
```

If you are still seeing errors, verify which Python is being used:

```bash
which python    # Linux / macOS
where python    # Windows
```

Make sure it points to the Python inside `.venv/`, not a system-level install.

## Windows Path Issues

You see errors like `FileNotFoundError` or `No such file or directory` when
passing folder paths on Windows, especially paths with spaces or backslashes.

**Cause.** Windows uses backslashes (`\`) in file paths, which Python can
interpret as escape characters. Paths with spaces also cause problems if they
are not quoted.

**Fix.** Wrap paths in double quotes and use either forward slashes or raw
strings.

```bash
# Use forward slashes (works everywhere)
python bring-your-own-docs/index_folder.py "C:/Users/You/My Documents/notes"

# Or use double backslashes
python bring-your-own-docs/index_folder.py "C:\\Users\\You\\My Documents\\notes"
```

If you are calling the pipeline from Python code, use `pathlib.Path` which
handles platform differences automatically:

```python
from pathlib import Path

folder = Path("C:/Users/You/My Documents/notes")
```
