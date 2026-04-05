"""Health check: verify Python, packages, Ollama, and required models are ready."""

import argparse
import shutil
import sys

import ollama  # Local LLM runner — used to check service status and available models


def check_python() -> bool:
    """Verify Python >= 3.10 is running."""
    v = sys.version_info
    ok = v.major == 3 and v.minor >= 10
    label = f"Python {v.major}.{v.minor}.{v.micro}"
    _report(ok, label, "Python 3.10+ required. Download from https://python.org")
    return ok


def check_package(name: str) -> bool:
    """Verify a pip package is importable."""
    try:
        __import__(name)
        _report(True, f"Package: {name}")
        return True
    except ImportError:
        _report(False, f"Package: {name}", f"Install with: pip install {name}")
        return False


def check_ollama_binary() -> bool:
    """Verify the Ollama binary is on PATH."""
    found = shutil.which("ollama") is not None
    _report(found, "Ollama binary", "Install from https://ollama.ai")
    return found


def check_ollama_running() -> bool:
    """Verify the Ollama service is responding."""
    try:
        ollama.list()
        _report(True, "Ollama service running")
        return True
    except Exception:
        _report(False, "Ollama service running", "Start it with: ollama serve")
        return False


def check_model(model_name: str) -> bool:
    """Verify a specific model is available in Ollama."""
    try:
        models = ollama.list()
        available = [m.model for m in models.models] if hasattr(models, "models") else []
        # Check if model name matches (with or without :latest tag)
        found = any(
            model_name in name or name.startswith(model_name)
            for name in available
        )
        _report(found, f"Model: {model_name}", f"Pull it with: ollama pull {model_name}")
        return found
    except Exception:
        _report(False, f"Model: {model_name}", "Ollama must be running first")
        return False


def _report(ok: bool, label: str, fix: str = "") -> None:
    """Print a ✓ or ✗ status line."""
    if ok:
        print(f"  \u2713 {label}")
    else:
        print(f"  \u2717 {label} \u2014 {fix}")


def main() -> None:
    """Run all health checks in order."""
    parser = argparse.ArgumentParser(description="Check rag-starter prerequisites")
    parser.add_argument("--verbose", action="store_true", help="Show extra detail")
    parser.parse_args()

    print("\nrag-starter health check\n")
    all_ok = True

    # 1. Python version
    all_ok = check_python() and all_ok

    # 2. Required packages
    packages = ["chromadb", "pymupdf", "pymupdf4llm", "ollama", "streamlit", "dotenv"]
    for pkg in packages:
        all_ok = check_package(pkg) and all_ok

    # 3. Ollama binary
    if not check_ollama_binary():
        all_ok = False
        print("\n  Skipping Ollama service and model checks (binary not found).\n")
        sys.exit(1)

    # 4. Ollama service
    if not check_ollama_running():
        all_ok = False
        print("\n  Skipping model checks (service not responding).\n")
        sys.exit(1)

    # 5. Required models
    all_ok = check_model("llama3.1:8b") and all_ok
    all_ok = check_model("nomic-embed-text") and all_ok

    print()
    if all_ok:
        print("All checks passed! You're ready to go.")
    else:
        print("Some checks failed. Fix the issues above and run this again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
