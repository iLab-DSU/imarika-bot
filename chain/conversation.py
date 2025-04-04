# chain/conversation.py
from typing import Any, Dict, List

from sqlalchemy import Column, DateTime, Integer, String, Text, func, select
from sqlalchemy.orm import declarative_base

from db.database import async_session  # DRY: use shared async_session

Base = declarative_base()


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(36), nullable=False)
    message = Column(Text, nullable=False)
    sender = Column(String(50), nullable=False)  # 'user' or 'bot'
    timestamp = Column(DateTime, server_default=func.now())


async def save_message(session_id: str, sender: str, message: str) -> None:
    async with async_session() as session:
        async with session.begin():
            entry = Conversation(session_id=session_id, sender=sender, message=message)
            session.add(entry)


async def get_conversation(session_id: str) -> List[Dict[str, Any]]:
    async with async_session() as session:
        result = await session.execute(
            select(Conversation)
            .where(Conversation.session_id == session_id)
            .order_by(Conversation.timestamp)
        )
        return [dict(row) for row in result.scalars().all()]
