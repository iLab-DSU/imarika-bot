# chain/vector_db.py
from typing import List

from langchain_community.document_loaders import CSVLoader, DirectoryLoader
from langchain_ollama import OllamaEmbeddings
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, Text, select
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import text

from app.config import EMBEDDING_MODEL, OLLAMA_BASE_URL
from db.database import async_session  # DRY: use shared async_session

Base = declarative_base()
chroma_db = None


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    # Assuming an embedding dimension of 1536. Adjust as needed.
    embedding = Column(Vector(1536), nullable=False)


ollamma_embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)


async def get_similar_documents(
    query_embedding: List[float], top_k: int = 5
) -> List[Document]:
    """
    Retrieve the top_k documents from the database whose embeddings are most similar
    to the query_embedding using the pgvector "<->" distance operator.
    """
    async with async_session() as session:
        stmt = text(
            """
            SELECT id, text, embedding
            FROM documents
            ORDER BY embedding <-> :query_embedding
            LIMIT :top_k
        """
        ).bindparams(query_embedding=query_embedding, top_k=top_k)
        result = await session.execute(stmt)
        rows = result.fetchall()
        return [dict(row) for row in rows]


async def add_documents_from_csv(path: str) -> str:
    """
    Load csv documents from data directory into the vector database.
    """
    resp = ""

    loader = DirectoryLoader(
        path, glob="**/*.csv", loader_cls=CSVLoader, loader_kwargs={"encoding": "utf-8"}
    )

    # Load documents from CSV files
    documents = loader.load()
    """
    Document Object Format:
    document = {
        page_content: str,
        metadata: {str: str}
    }
    """
    resp += "Loaded {len(documents)} documents\n"

    for doc in documents:
        emb = ollamma_embeddings.embed_query(doc["page_content"])
        await add_document_if_not_exists(doc.metadata["source"], emb)
    return resp + "Added documents to the database"


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
