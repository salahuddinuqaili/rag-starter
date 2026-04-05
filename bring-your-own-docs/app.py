"""Streamlit web UI for indexing documents and asking questions via RAG."""

import os
import sys

# Add project root to path so we can import src/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st  # Web UI framework — builds interactive apps from Python scripts

from src.errors import RagStarterError
from src.pipeline import index_documents, query_documents
from src.store import store_exists

st.set_page_config(page_title="rag-starter", page_icon="📄", layout="wide")
st.title("rag-starter")
st.caption("Ask questions about your documents using local AI")

# --- Sidebar: Configuration ---
with st.sidebar:
    st.header("Settings")

    folder_path = st.text_input(
        "Document folder path",
        value="./sample-docs",
        help="Path to the folder containing your PDF, MD, or TXT files",
    )

    db_path = st.text_input(
        "Database path",
        value="./chroma_db",
        help="Where to store the ChromaDB vector database",
    )

    chunk_size = st.slider(
        "Chunk size (characters)",
        min_value=100,
        max_value=2000,
        value=500,
        step=50,
        help="Larger chunks keep more context but may be less precise",
    )

    top_k = st.slider(
        "Results to retrieve (top-k)",
        min_value=1,
        max_value=20,
        value=5,
        help="More results give the LLM more context but may add noise",
    )

    model = st.text_input(
        "LLM model",
        value="llama3.1:8b",
        help="The Ollama model to use for generating answers",
    )

    st.divider()

    if st.button("Index Documents", type="primary", use_container_width=True):
        if not os.path.isdir(folder_path):
            st.error(f"Folder not found: {folder_path}")
        else:
            try:
                with st.spinner("Indexing documents..."):
                    stats = index_documents(
                        folder_path=folder_path,
                        db_path=db_path,
                        chunk_size=chunk_size,
                    )
                st.success(
                    f"Indexed {stats['files_loaded']} files → "
                    f"{stats['chunks_created']} chunks in {stats['time_seconds']:.1f}s"
                )
            except RagStarterError as e:
                st.error(str(e))

    if store_exists(db_path):
        st.info("Index ready — ask questions below!")
    else:
        st.warning("No documents indexed yet. Set a folder path and click 'Index Documents'.")

# --- Main area: Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("View sources"):
                for source in message["sources"]:
                    name = source["metadata"].get("source", "unknown")
                    distance = source["distance"]
                    st.markdown(f"**{name}** (relevance: {1 - distance:.2f})")
                    content = source["content"]
                    st.text(content[:300] + "..." if len(content) > 300 else content)
                    st.divider()

# Chat input
if question := st.chat_input("Ask a question about your documents"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    if not store_exists(db_path):
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
                        db_path=db_path,
                        top_k=top_k,
                        model=model,
                    )

                st.markdown(result["answer"])

                if result["sources"]:
                    with st.expander("View sources"):
                        for source in result["sources"]:
                            name = source["metadata"].get("source", "unknown")
                            distance = source["distance"]
                            st.markdown(f"**{name}** (relevance: {1 - distance:.2f})")
                            content = source["content"]
                            st.text(content[:300] + "..." if len(content) > 300 else content)
                            st.divider()

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result["sources"],
                })
            except RagStarterError as e:
                error_msg = f"Error: {e}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                })
