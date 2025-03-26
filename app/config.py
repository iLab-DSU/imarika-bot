import os

from dotenv import load_dotenv

# Load environment variables from a .env file (located at project root)
load_dotenv()

# Now safely retrieve the DATABASE_URL
WS_ENDPOINT = os.getenv("WS_ENDPOINT")
DATABASE_URL = os.getenv("DATABASE_URL")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

# AI Models
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

# Instructions
CHAT_SYSTEM_INSTRUCTION = """
        You are an AI assistant on the Imarika App. Follow these rules:
        1. Stay Relevant: Only answer questions related to farming. Politely decline unrelated queries.
        2. Be Concise: Deliver clear and focused responses, aligning with the platform's purpose.
        Stay professional, helpful, and user-focused.
"""  # noqa: E501
