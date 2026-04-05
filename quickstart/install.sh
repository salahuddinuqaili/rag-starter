#!/usr/bin/env bash
set -e

echo ""
echo "rag-starter installer"
echo "====================="
echo ""

# 1. Check Python >= 3.10
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 not found. Install Python 3.10+ from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo "✗ Python $PYTHON_VERSION found, but 3.10+ is required."
    exit 1
fi
echo "✓ Python $PYTHON_VERSION"

# 2. Create virtual environment (idempotent — skips if already exists)
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment at .venv/ ..."
    python3 -m venv .venv
else
    echo "✓ Virtual environment already exists at .venv/"
fi

# 3. Activate venv
source .venv/bin/activate
echo "✓ Virtual environment activated"

# 4. Install Python dependencies
echo "Installing Python dependencies..."
pip install -r quickstart/requirements.txt --quiet
echo "✓ Python packages installed"

# 5. Check Ollama
if ! command -v ollama &> /dev/null; then
    echo ""
    echo "✗ Ollama not found."
    echo ""
    echo "  Ollama runs AI models locally on your machine."
    echo "  Install it from: https://ollama.ai"
    echo "  After installing, restart your terminal and re-run this script."
    exit 1
fi
echo "✓ Ollama found"

# 6. Pull required models (idempotent — skips if already downloaded)
echo "Pulling LLM model (llama3.1:8b) — this may take a few minutes on first run..."
ollama pull llama3.1:8b

echo "Pulling embedding model (nomic-embed-text)..."
ollama pull nomic-embed-text

echo "✓ Models ready"

# 7. Run health check
echo ""
echo "Running health check..."
python quickstart/check.py

echo ""
echo "Setup complete!"
echo ""
echo "Run the demo now:"
echo "  python quickstart/my_first_rag.py"
echo ""
echo "IMPORTANT: If you close this terminal, reactivate the"
echo "virtual environment first:"
echo "  source .venv/bin/activate"
echo ""
