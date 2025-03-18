# chain/conversation.py
from sqlalchemy import Column, Integer, String, Text, DateTime, func, select
from sqlalchemy.orm import declarative_base
from typing import List, Dict, Any

from db.database import async_session  # DRY: use shared async_session

Base = declarative_base()

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
            select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.timestamp)
        )
        return [dict(row) for row in result.scalars().all()]

