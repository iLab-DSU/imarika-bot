# chain/vector_db.py
from typing import List
from langchain_community.document_loaders import CSVLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from db.chroma.chroma import chroma_db

# from db.database import async_session  # DRY: use shared async_session


def query_chroma_doc(query: str, top_k: int = 5) -> List[Document]:
    """
    Query the database for similar documents.
    """
    res = chroma_db.similarity_search(query, top_k)
    return res


def add_documents_from_csv(path: str) -> str:
    """
    Load csv documents from data directory into the vector database.

    Document Object Format:
    document = {
        page_content: str,
        metadata: {str: str}
    }
    """
    resp = ""

    loader = DirectoryLoader(
        path, glob="**/*.csv", loader_cls=CSVLoader, loader_kwargs={"encoding": "utf-8"}
    )

    # Load documents from CSV files
    documents = loader.load()
    resp += "Loaded " + str(len(documents)) + " documents"
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, length_function=len
    )

    chunks = splitter.split_documents(documents)
    chroma_db.add_documents(chunks)
    return resp + "Added documents to the database"
