import os
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import List, Dict, Any

# Database connection string for Postgres
DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=False, pool_size=10, max_overflow=20, pool_timeout=30)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    message = Column(Text, nullable=False)
    sender = Column(String(50), nullable=False)  # 'user' or 'bot'
    timestamp = Column(DateTime, server_default=func.now())

async def save_message(user_id: int, sender: str, message: str) -> None:
    async with async_session() as session:
        async with session.begin():
            entry = Conversation(user_id=user_id, sender=sender, message=message)
            session.add(entry)

async def get_conversation(user_id: int) -> List[Dict[str, Any]]:
    async with async_session() as session:
        result = await session.execute(
            Conversation.__table__.select().where(Conversation.user_id == user_id).order_by(Conversation.timestamp)
        )
        return [dict(row) for row in result.fetchall()]
