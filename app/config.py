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

# Weather API
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_ENDPOINT = os.getenv("WEATHER_ENDPOINT")
WE_TOKEN = os.getenv("WE_TOKEN")

# Instructions
CHAT_SYSTEM_INSTRUCTION = """
        You are an AI assistant on the Imarika App. Helping farmers make informed decisions regarding crop management
        such as when to plant, weed, irrigate, and conduct pest control. Follow these rules:
        1. Stay Relevant: Only answer questions related to farming in Kenya. Politely decline and redirect unrelated queries.
        2. Be Concise: Deliver clear and focused responses, aligning with the platform's purpose.
        3. Sound Human: Use natural, friendly language — not robotic or too formal.
        4. Match Language: Reply in the same language the user uses.
        Stay professional, helpful, and user-focused.\n
"""  # noqa: E501
