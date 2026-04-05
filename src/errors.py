"""Custom exceptions for rag-starter so library code never calls sys.exit()."""


class RagStarterError(Exception):
    """Base exception for all rag-starter errors."""


class OllamaConnectionError(RagStarterError):
    """Raised when Ollama is not running or unreachable.

    Fix: Start Ollama with `ollama serve`, then retry.
    """

    def __init__(self, message: str = "") -> None:
        default = (
            "Could not connect to Ollama. Is it running? "
            "Start it with: ollama serve"
        )
        super().__init__(message or default)


class OllamaModelNotFoundError(RagStarterError):
    """Raised when a requested Ollama model is not available locally.

    Fix: Pull the model with `ollama pull <model-name>`.
    """

    def __init__(self, model: str) -> None:
        super().__init__(
            f"Model '{model}' not found. Pull it with: ollama pull {model}"
        )


class MissingAPIKeyError(RagStarterError):
    """Raised when a cloud API key is required but not set.

    Fix: Export the key, e.g. `export OPENAI_API_KEY=your-key-here`.
    """

    def __init__(self, key_name: str = "OPENAI_API_KEY") -> None:
        super().__init__(
            f"{key_name} not set. Export it or use Ollama instead."
        )


class IndexNotFoundError(RagStarterError):
    """Raised when querying a ChromaDB path that has no index.

    Fix: Run index_documents() or index_folder.py first.
    """

    def __init__(self, db_path: str) -> None:
        super().__init__(
            f"No index found at '{db_path}'. "
            "Run index_documents() or index_folder.py first."
        )
