# db/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from a .env file (located at project root)
load_dotenv()

# Now safely retrieve the DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30
)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
