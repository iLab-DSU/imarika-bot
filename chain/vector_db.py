import os
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader, DirectoryLoader
from langchain_core.documents import Document

from db.chroma.chroma import chroma_db


def query_chroma_doc(query: str, top_k: int = 2) -> str:
    """
    Query the database for similar documents.
    """
    res = chroma_db.similarity_search(query, top_k)
    text = ""
    for doc in res:
        text += doc.page_content + "\n"
    return text


def query_with_metadata(query: str, fltr: str, top_k: int = 5) -> str:
    """
    Query the database for similar documents using metadata.

    query = question as string
    fltr = metadata as string
    top_k = number of similar documents to return

    """
    f = {"name": fltr}
    res = chroma_db.similarity_search(query, top_k, filter=f)
    text = ""
    for doc in res:
        text += doc.page_content + "\n"
    return text


def get_documents() -> List[Document]:
    """
    Gets 5 documents from the vector database.
    """
    return chroma_db.get(limit=5)


def add_documents_from_csv(path: str = None, reset: bool = False) -> str:
    """
    Load csv documents from data directory into the vector database.
    """
    resp = ""

    # set default path to data directory
    if path is None:
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = parent_dir[:-6]
        path = os.path.join(parent_dir, "data")

    # csv loader params
    csv_loader_kwargs = {"encoding": "utf-8"}

    # Load CSV files from directory
    loader = DirectoryLoader(
        path, glob="**/*.csv", loader_cls=CSVLoader, loader_kwargs=csv_loader_kwargs
    )

    # Reset collection
    if reset:
        chroma_db.reset_collection()
        resp += "Reset collection, "

    # Load documents from CSV files
    documents = loader.load()
    resp += "Loaded " + str(len(documents)) + " documents, "
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, length_function=len
    )
    for doc in documents:
        # add file name as metadata
        source_name = doc.metadata["source"].split("/")[-1].replace(".csv", "")
        doc.metadata["name"] = source_name

    # split into chunks and store in database
    chunks = splitter.split_documents(documents)
    chroma_db.add_documents(chunks)

    return resp + "Added documents to the database"
