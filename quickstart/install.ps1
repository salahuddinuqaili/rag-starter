# rag-starter installer for Windows (PowerShell)

Write-Host ""
Write-Host "rag-starter installer"
Write-Host "====================="
Write-Host ""

# 1. Check Python >= 3.10
try {
    $pythonVersion = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
    $parts = $pythonVersion.Split(".")
    $major = [int]$parts[0]
    $minor = [int]$parts[1]

    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 10)) {
        Write-Host "✗ Python $pythonVersion found, but 3.10+ is required." -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Python $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Install Python 3.10+ from https://python.org" -ForegroundColor Red
    exit 1
}

# 2. Create virtual environment (idempotent)
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment at .venv/ ..."
    python -m venv .venv
} else {
    Write-Host "✓ Virtual environment already exists at .venv/" -ForegroundColor Green
}

# 3. Activate venv
try {
    & .venv\Scripts\Activate.ps1
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "✗ Could not activate virtual environment." -ForegroundColor Red
    Write-Host "  If you see an execution policy error, run this first:" -ForegroundColor Yellow
    Write-Host "  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Write-Host "  Then re-run this script."
    exit 1
}

# 4. Install Python dependencies
Write-Host "Installing Python dependencies..."
pip install -r quickstart\requirements.txt --quiet
Write-Host "✓ Python packages installed" -ForegroundColor Green

# 5. Check Ollama
$ollamaPath = Get-Command ollama -ErrorAction SilentlyContinue
if (-not $ollamaPath) {
    Write-Host ""
    Write-Host "✗ Ollama not found." -ForegroundColor Red
    Write-Host "  Install it from: https://ollama.ai" -ForegroundColor Yellow
    Write-Host "  Then re-run this script."
    exit 1
}
Write-Host "✓ Ollama found" -ForegroundColor Green

# 6. Pull required models
Write-Host "Pulling LLM model (llama3.1:8b) — this may take a few minutes on first run..."
ollama pull llama3.1:8b

Write-Host "Pulling embedding model (nomic-embed-text)..."
ollama pull nomic-embed-text

Write-Host "✓ Models ready" -ForegroundColor Green

# 7. Run health check
Write-Host ""
Write-Host "Running health check..."
python quickstart\check.py

Write-Host ""
Write-Host "Setup complete! Try:" -ForegroundColor Green
Write-Host "  .venv\Scripts\Activate.ps1"
Write-Host "  python quickstart\my_first_rag.py"
Write-Host ""
