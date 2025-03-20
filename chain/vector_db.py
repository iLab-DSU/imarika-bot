# chain/vector_db.py
import os
import asyncio
from typing import List
from sqlalchemy import Column, Integer, Text, select
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import text
from pgvector.sqlalchemy import Vector
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, CSVLoader


from db.database import async_session  # DRY: use shared async_session

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    # Assuming an embedding dimension of 1536. Adjust as needed.
    embedding = Column(Vector(1536), nullable=False)

async def get_similar_documents(query_embedding: List[float], top_k: int = 5) -> List[Document]:
    """
    Retrieve the top_k documents from the database whose embeddings are most similar
    to the query_embedding using the pgvector "<->" distance operator.
    """
    async with async_session() as session:
        stmt = text("""
            SELECT id, text, embedding
            FROM documents
            ORDER BY embedding <-> :query_embedding
            LIMIT :top_k
        """).bindparams(query_embedding=query_embedding, top_k=top_k)
        result = await session.execute(stmt)
        rows = result.fetchall()
        return [dict(row) for row in rows]

def create_vector_store(persist: bool, path: str = "") -> Chroma:
    """
    Create a Chroma vector store db. If persist is True, the db will be saved to disk and requires the path for where it will be stored.
    """
    embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

    if persist:
        vectordb = Chroma(
            collection_name="imarika_kb",
            embedding_function=embeddings,
            persist_directory=path
        )

        return vectordb
    else:
        vectordb = Chroma(
            collection_name="imarika_kb",
            embedding_function=embeddings
        )

        return vectordb

def add_documents_from_csv(database: Chroma, path: str) -> None:
    """
    Load csv documents from data directory into the vector database.
    """
    loader = DirectoryLoader(
        path,
        glob="**/*.csv",
        loader_cls=CSVLoader,
        loader_kwargs={"encoding": "utf-8"}
    )

    # Load documents from CSV files
    documents = loader.load()
    print(f"Loaded {len(documents)} documents from CSV files")

    try:
        database.add_documents(documents)
    except Exception as e:
        print(f"Error adding document: {e}")
    

def query_vector_db(database: Chroma, query: str, k: int) -> str:
    """
    Query the vector database with a text prompt.
    """
    return database.similarity_search(query, k)

async def add_document_if_not_exists(text_value: str, embedding: List[float]) -> None:
    """
    Adds a document to the vector DB if it doesn't already exist.
    Checks by text value for simplicity.
    """
    async with async_session() as session:
        stmt = select(Document).where(Document.text == text_value)
        result = await session.execute(stmt)
        doc = result.scalar_one_or_none()
        if not doc:
            new_doc = Document(text=text_value, embedding=embedding)
            session.add(new_doc)
            await session.commit()

def main():
    # Create and persist the vector store
    v_path = os.path.join(os.path.dirname(__file__), "db")
    print(f"Creating vector store at {v_path}")
    vectordb = create_vector_store(persist=True, path=v_path)

    # Load documents from CSV files
    data_path = os.path.join(os.path.dirname(__file__), "data")
    print(f"Loading documents from {data_path}")
    add_documents_from_csv(vectordb, data_path)

    # Query the vector database
    while True:
        # Code to execute at least once
        query = input("Enter a query:")
        k = int(input("Enter the number of results to return:"))
        result = query_vector_db(vectordb, query, k)
        print(result)
        
        # Condition to exit the loop
        continue_query = input("Do you want to query again? (yes/no): ").strip().lower()
        if continue_query != 'yes':
            break