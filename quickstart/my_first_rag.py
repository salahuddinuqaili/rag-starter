"""Your first RAG pipeline — index sample docs and ask questions in under a minute."""

import argparse
import os
import shutil
import sys
import tempfile

# Add project root to path so we can import src/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline import index_documents, query_documents


SAMPLE_QUESTIONS = [
    "What are the best practices for async communication in remote teams?",
    "How does supervised learning differ from unsupervised learning?",
    "What neighbourhoods should I visit in Berlin?",
]


def main() -> None:
    """Index sample-docs/ into a temp ChromaDB and ask 3 cross-topic questions."""
    parser = argparse.ArgumentParser(description="Run your first RAG pipeline")
    parser.add_argument("--verbose", action="store_true", help="Show detailed pipeline output")
    args = parser.parse_args()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_dir = os.path.join(project_root, "sample-docs")

    if not os.path.isdir(sample_dir):
        print(f"Sample docs not found at {sample_dir}")
        sys.exit(1)

    # Use a temp directory so we don't pollute the project with index data
    tmp_db = tempfile.mkdtemp(prefix="rag_starter_")

    try:
        print("=" * 60)
        print("  rag-starter: Your First RAG Pipeline")
        print("=" * 60)
        print()

        # Step 1: Index
        print("Step 1: Indexing sample documents...")
        print()
        stats = index_documents(
            folder_path=sample_dir,
            db_path=tmp_db,
            verbose=args.verbose,
        )
        print(f"Indexed {stats['files_loaded']} files → {stats['chunks_created']} chunks "
              f"in {stats['time_seconds']:.1f}s")
        print()

        # Step 2: Ask questions
        print("Step 2: Asking questions across your documents...")
        print()

        for question in SAMPLE_QUESTIONS:
            print("-" * 60)
            print(f"Question: {question}")
            print()

            result = query_documents(
                question=question,
                db_path=tmp_db,
                top_k=3,
                verbose=args.verbose,
            )

            print(f"Answer: {result['answer']}")
            print()

            if result["sources"]:
                sources = set(s["metadata"].get("source", "unknown") for s in result["sources"])
                print(f"Sources: {', '.join(sources)}")
            print()

        print("=" * 60)
        print("  Done! Now try it on YOUR documents:")
        print("  python bring-your-own-docs/index_folder.py /path/to/your/folder")
        print("  python bring-your-own-docs/query.py \"your question here\"")
        print("=" * 60)

    finally:
        # Clean up temp database
        shutil.rmtree(tmp_db, ignore_errors=True)


if __name__ == "__main__":
    main()


# Expected output (answers will vary based on the LLM):
# ============================================================
#   rag-starter: Your First RAG Pipeline
# ============================================================
#
# Step 1: Indexing sample documents...
# Indexed 6 files → ~42 chunks in 3.2s
#
# Step 2: Asking questions across your documents...
#
# ------------------------------------------------------------
# Question: What are the best practices for async communication in remote teams?
# Answer: Based on the context, the best practices include writing decisions down
#         rather than relying on Slack, sharing meeting notes within 24 hours...
# Sources: remote-work-best-practices.md
#
# ------------------------------------------------------------
# Question: How does supervised learning differ from unsupervised learning?
# Answer: Supervised learning uses labelled training data (like spam/not-spam),
#         while unsupervised learning finds patterns in unlabelled data...
# Sources: intro-to-machine-learning.md
#
# ------------------------------------------------------------
# Question: What neighbourhoods should I visit in Berlin?
# Answer: Kreuzberg for culture, Mitte for museums, Prenzlauer Berg for brunch,
#         and Neukölln for nightlife...
# Sources: berlin-travel-guide.md
