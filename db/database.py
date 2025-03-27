# db/database.py
import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables from a .env file (located at project root)
load_dotenv()

# Now safely retrieve the DATABASE_URL
DATABASE_URL = os.getenv("AS_DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL, echo=False, pool_size=10, max_overflow=20, pool_timeout=30
)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
