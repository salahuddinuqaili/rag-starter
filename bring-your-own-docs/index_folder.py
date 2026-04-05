"""CLI: Index any folder of documents into ChromaDB for RAG querying."""

import argparse
import os
import sys

# Add project root to path so we can import src/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline import index_documents


def main() -> None:
    """Parse arguments and run the indexing pipeline."""
    parser = argparse.ArgumentParser(
        description="Index a folder of documents (PDF, MD, TXT) into ChromaDB"
    )
    parser.add_argument(
        "folder",
        help="Path to the folder containing your documents",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        help="Maximum characters per chunk (default: 500)",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=50,
        help="Characters of overlap between chunks (default: 50)",
    )
    parser.add_argument(
        "--db-path",
        default="./chroma_db",
        help="Where to store the ChromaDB database (default: ./chroma_db)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed timing for each pipeline stage",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print(f"Error: Folder not found: {args.folder}")
        sys.exit(1)

    if not os.listdir(args.folder):
        print(f"Error: Folder is empty: {args.folder}")
        sys.exit(1)

    print(f"Indexing documents from: {args.folder}")
    print()

    stats = index_documents(
        folder_path=args.folder,
        db_path=args.db_path,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        verbose=args.verbose,
    )

    print()
    print(f"Done! Indexed {stats['files_loaded']} files → {stats['chunks_created']} chunks "
          f"in {stats['time_seconds']:.1f}s")
    print(f"Database saved to: {os.path.abspath(args.db_path)}")
    print()
    print("Next step — ask a question:")
    print(f'  python bring-your-own-docs/query.py "your question here" --db-path {args.db_path}')


if __name__ == "__main__":
    main()
