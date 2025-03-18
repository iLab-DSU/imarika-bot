import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker

# Database connection string for Postgres
DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=False, pool_size=10, max_overflow=20, pool_timeout=30)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

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
    # Optionally await engine.dispose() during shutdown

# Convenience wrapper for synchronous calls (for use in synchronous contexts)
def log(level: str, message: str) -> None:
    asyncio.run(log_to_db(level, message))
