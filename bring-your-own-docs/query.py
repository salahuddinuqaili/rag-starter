"""CLI: Ask questions against your indexed documents."""

import argparse
import os
import sys

# Add project root to path so we can import src/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline import query_documents
from src.store import store_exists


def print_result(result: dict) -> None:
    """Format and print a query result with answer and sources."""
    print()
    print(f"Answer: {result['answer']}")
    print()

    if result["sources"]:
        print("Sources:")
        seen = set()
        for source in result["sources"]:
            name = source["metadata"].get("source", "unknown")
            distance = source["distance"]
            key = name
            if key not in seen:
                seen.add(key)
                print(f"  - {name} (relevance: {1 - distance:.2f})")
    print()


def interactive_mode(db_path: str, top_k: int, model: str, verbose: bool) -> None:
    """Enter a loop that prompts for questions until Ctrl+C."""
    print("Interactive mode — type your questions below. Press Ctrl+C to quit.")
    print()

    while True:
        try:
            question = input("Question: ").strip()
            if not question:
                continue

            result = query_documents(
                question=question,
                db_path=db_path,
                top_k=top_k,
                model=model,
                verbose=verbose,
            )
            print_result(result)

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break


def main() -> None:
    """Parse arguments and run a query or enter interactive mode."""
    parser = argparse.ArgumentParser(
        description="Ask questions against your indexed documents"
    )
    parser.add_argument(
        "question",
        nargs="?",
        default=None,
        help="Your question (omit for interactive mode)",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of chunks to retrieve (default: 5)",
    )
    parser.add_argument(
        "--model",
        default="llama3.1:8b",
        help="Ollama model for answer generation (default: llama3.1:8b)",
    )
    parser.add_argument(
        "--db-path",
        default="./chroma_db",
        help="Path to the ChromaDB database (default: ./chroma_db)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed timing for each pipeline stage",
    )
    args = parser.parse_args()

    if not store_exists(args.db_path):
        print("No index found. Run index_folder.py first:")
        print(f"  python bring-your-own-docs/index_folder.py /path/to/docs --db-path {args.db_path}")
        sys.exit(1)

    if args.question is None:
        interactive_mode(args.db_path, args.top_k, args.model, args.verbose)
    else:
        result = query_documents(
            question=args.question,
            db_path=args.db_path,
            top_k=args.top_k,
            model=args.model,
            verbose=args.verbose,
        )
        print_result(result)


if __name__ == "__main__":
    main()
