# app/utils/logger.py
import asyncio
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import declarative_base
from db.database import async_session  # DRY: use shared async_session

Base = declarative_base()

class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    level = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())

async def log_to_db(level: str, message: str) -> None:
    async with async_session() as session:
        async with session.begin():
            log_entry = Log(level=level, message=message)
            session.add(log_entry)

def log(level: str, message: str) -> None:
    asyncio.run(log_to_db(level, message))
