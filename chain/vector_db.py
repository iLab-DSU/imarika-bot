# chain/vector_db.py
import os
import asyncio
from typing import List
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, Text, select
from sqlalchemy.sql import text
from pgvector import Vector

# Database connection string for Postgres
DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    # Assuming an embedding dimension of 1536. Adjust as needed.
    embedding = Column(Vector(dim=1536), nullable=False)

# Create an async engine and session maker
engine = create_async_engine(DATABASE_URL, echo=False, pool_size=10, max_overflow=20, pool_timeout=30)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_similar_documents(query_embedding: List[float], top_k: int = 5) -> List[Document]:
    """
    Retrieve the top_k documents from the database whose embeddings are most similar
    to the query_embedding using the pgvector "<->" distance operator.
    """
    async with async_session() as session:
        # pgvector similarity search: ORDER BY embedding <-> :query_embedding
        stmt = text("""
            SELECT id, text, embedding
            FROM documents
            ORDER BY embedding <-> :query_embedding
            LIMIT :top_k
        """).bindparams(query_embedding=query_embedding, top_k=top_k)
        result = await session.execute(stmt)
        rows = result.fetchall()
        # Convert rows to a list of Document-like dicts
        return [dict(row) for row in rows]

async def add_document_if_not_exists(text_value: str, embedding: List[float]) -> None:
    """
    Adds a document to the vector DB if it doesn't already exist.
    This function checks by text value for simplicity.
    """
    async with async_session() as session:
        stmt = select(Document).where(Document.text == text_value)
        result = await session.execute(stmt)
        doc = result.scalar_one_or_none()
        if not doc:
            new_doc = Document(text=text_value, embedding=embedding)
            session.add(new_doc)
            await session.commit()

# Example usage:
# asyncio.run(add_document_if_not_exists("Example document text", [0.1]*1536))
