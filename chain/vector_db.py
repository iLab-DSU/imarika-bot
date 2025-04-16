import os
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader, DirectoryLoader
from langchain_core.documents import Document

from db.chroma.chroma import chroma_db


def _similarity_search_with_threshold(
    query: str, top_k: int, similarity_threshold: float, filter_dict: dict = None
) -> str:
    try:
        results = (
            chroma_db.similarity_search_with_score(query, k=top_k, filter=filter_dict)
            if filter_dict
            else chroma_db.similarity_search_with_score(query, k=top_k)
        )

        filtered = [
            doc.page_content for doc, score in results if score >= similarity_threshold
        ]
        return (
            "\n".join(filtered)
            if filtered
            else "No results above similarity threshold."
        )
    except Exception as e:
        return f"Error during similarity search: {e}"


def query_chroma_doc(
    query: str, top_k: int = 2, similarity_threshold: float = 0.5
) -> str:
    return _similarity_search_with_threshold(query, top_k, similarity_threshold)


def query_with_metadata(
    query: str,
    meta_title: str,
    fltr: str,
    top_k: int = 5,
    similarity_threshold: float = 0.5,
) -> str:
    return _similarity_search_with_threshold(
        query, top_k, similarity_threshold, filter_dict={meta_title: fltr}
    )


def get_documents() -> List[Document]:
    try:
        return chroma_db.get(limit=5)
    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return []


def add_documents_from_csv(path: str = None, reset: bool = False) -> str:
    try:
        response = []

        # Set default path
        if path is None:
            base_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), os.pardir)
            )
            path = os.path.join(base_dir, "data")

        # If not resetting, check if documents already exist
        if not reset:
            existing_docs = chroma_db.get(limit=1)
            if existing_docs:
                return "Chroma DB already has data. Skipping document addition."

        # Initialize loader with recursive loading and UTF-8 encoding
        loader = DirectoryLoader(
            path=path,
            glob="**/*.csv",
            loader_cls=CSVLoader,
            loader_kwargs={"encoding": "utf-8"},
            recursive=True,
            show_progress=True,
        )

        # Reset database if requested
        if reset:
            chroma_db.reset_collection()
            response.append("Collection reset.")

        # Load and tag documents
        documents = loader.load()
        for doc in documents:
            filename = os.path.basename(doc.metadata.get("source", "")).replace(
                ".csv", ""
            )
            if filename.endswith("_ca"):
                doc.metadata["type"] = "climate"
            doc.metadata["name"] = filename
            doc.metadata["type"] = "general"

        # Split documents into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = splitter.split_documents(documents)

        # Store in vector database
        chroma_db.add_documents(chunks)
        response.append(f"Loaded and added {len(chunks)} document chunks.")

        return " ".join(response)

    except Exception as e:
        return f"Error adding documents from CSV: {e}"
