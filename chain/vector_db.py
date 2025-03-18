# chain/vector_db.py
import os
import asyncio
from typing import List
from sqlalchemy import Column, Integer, Text, select
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import text
from pgvector import Vector

from db.database import async_session  # DRY: use shared async_session

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    # Assuming an embedding dimension of 1536. Adjust as needed.
    embedding = Column(Vector(dim=1536), nullable=False)

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
