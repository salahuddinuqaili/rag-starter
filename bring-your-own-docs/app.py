"""Streamlit web UI for indexing documents and asking questions via RAG."""

import os
import sys
import threading
import time

# Add project root to path so we can import src/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st  # Web UI framework — builds interactive apps from Python scripts

from src.errors import RagStarterError
from src.pipeline import index_documents, query_documents
from src.store import store_exists

st.set_page_config(page_title="rag-starter", page_icon="📄", layout="wide")

# --- Session state defaults ---
for key, default in {
    "messages": [],
    "indexed_folder": None,
    "indexed_count": 0,
    "prefill_question": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def _check_ollama() -> bool:
    """Return True if Ollama is reachable, False otherwise."""
    try:
        import ollama  # Ollama Python client — talks to local LLM server
        ollama.list()
        return True
    except Exception:
        return False


def _relevance_badge(distance: float) -> str:
    """Return a colored relevance string based on distance."""
    pct = (1 - distance) * 100
    if pct > 70:
        return f":green[{pct:.0f}% match]"
    if pct > 40:
        return f":orange[{pct:.0f}% match]"
    return f":red[{pct:.0f}% match]"


def _render_sources(sources: list[dict]) -> None:
    """Display source chunks with relevance badges inside an expander."""
    if not sources:
        return
    with st.expander("View sources"):
        for source in sources:
            name = source["metadata"].get("source", "unknown")
            st.markdown(f"**{name}** — {_relevance_badge(source['distance'])}")
            content = source["content"]
            st.text(content[:300] + "..." if len(content) > 300 else content)
            st.divider()


# --- Ollama connectivity banner ---
if not _check_ollama():
    st.warning(
        "Ollama appears unreachable. Start it with `ollama serve` "
        "or install from https://ollama.ai"
    )

# --- Sidebar ---
with st.sidebar:
    st.header("Basic Setup")

    folder_path = st.text_input(
        "Document folder path",
        value="./sample-docs",
        help="Path to the folder containing your PDF, MD, or TXT files",
    )

    if st.button("Index Documents", type="primary", use_container_width=True):
        if not os.path.isdir(folder_path):
            st.error(f"Folder not found: {folder_path}")
        else:
            try:
                progress_bar = st.progress(0, text="Starting indexing...")
                result_holder: dict = {}

                def _run_indexing() -> None:
                    result_holder["stats"] = index_documents(
                        folder_path=folder_path,
                        db_path=st.session_state.get("db_path", "./chroma_db"),
                        chunk_size=st.session_state.get("chunk_size", 500),
                    )

                thread = threading.Thread(target=_run_indexing)
                thread.start()
                # Approximate progress while the real work happens
                step = 0
                while thread.is_alive():
                    step = min(step + 3, 90)
                    progress_bar.progress(step, text="Indexing documents...")
                    time.sleep(0.3)
                thread.join()
                progress_bar.progress(100, text="Done!")

                if "stats" in result_holder:
                    stats = result_holder["stats"]
                    st.session_state.indexed_folder = folder_path
                    st.session_state.indexed_count = stats["chunks_created"]
                    st.success(
                        f"Indexed {stats['files_loaded']} files "
                        f"({stats['chunks_created']} chunks) in {stats['time_seconds']:.1f}s"
                    )
            except RagStarterError as exc:
                st.error(f"{exc}\n\nCheck that Ollama is running: `ollama serve`")

    # Status indicator
    db_path_val = st.session_state.get("db_path", "./chroma_db")
    if st.session_state.indexed_folder:
        st.info(
            f"Indexed: {st.session_state.indexed_count} chunks "
            f"from {st.session_state.indexed_folder}"
        )
    elif store_exists(db_path_val):
        st.info("Index found — ask questions below!")
    else:
        st.warning("No index yet. Set a folder and click Index Documents.")

    with st.expander("Advanced Settings"):
        st.text_input(
            "Database path", value="./chroma_db", key="db_path",
            help="Where to store the ChromaDB vector database",
        )
        st.slider(
            "Chunk size (characters)", 100, 2000, 500, step=50, key="chunk_size",
            help="Larger chunks keep more context but may be less precise",
        )
        st.slider(
            "Results to retrieve (top-k)", 1, 20, 5, key="top_k",
            help="More results give the LLM more context but may add noise",
        )
        st.text_input(
            "LLM model", value="llama3.1:8b", key="model",
            help="The Ollama model to use for generating answers",
        )

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Main area ---
st.title("rag-starter")

effective_db = st.session_state.get("db_path", "./chroma_db")
has_index = store_exists(effective_db)

# Onboarding: shown when no index exists and chat is empty
if not has_index and not st.session_state.messages:
    st.markdown("**Ask questions about your documents using local AI.**")
    st.markdown(
        "**Getting started:** 1. Set your folder path in the sidebar "
        "→ 2. Click **Index Documents** → 3. Ask a question below"
    )
    st.markdown("**Try an example question:**")
    cols = st.columns(3)
    examples = [
        "What are the best practices for async communication?",
        "How does supervised learning differ from unsupervised?",
        "What neighbourhoods should I visit in Berlin?",
    ]
    for col, q in zip(cols, examples):
        if col.button(q, use_container_width=True):
            st.session_state.prefill_question = q
            st.rerun()

# Replay chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg:
            _render_sources(msg["sources"])

# Chat input — pick up prefilled question or user typing
question = st.chat_input("Ask a question about your documents")
if st.session_state.prefill_question:
    question = st.session_state.prefill_question
    st.session_state.prefill_question = None

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    if not store_exists(effective_db):
        response = "No documents indexed yet. Use the sidebar to index a folder first."
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    else:
        with st.chat_message("assistant"):
            try:
                with st.spinner("Searching and generating answer..."):
                    result = query_documents(
                        question=question,
                        db_path=effective_db,
                        top_k=st.session_state.get("top_k", 5),
                        model=st.session_state.get("model", "llama3.1:8b"),
                    )
                st.markdown(result["answer"])
                _render_sources(result["sources"])
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result["sources"],
                })
            except RagStarterError as exc:
                error_msg = f"Something went wrong: {exc}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )
