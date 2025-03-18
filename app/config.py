from dotenv import load_dotenv
import os

# Load environment variables from a .env file (located at project root)
load_dotenv()

# Now safely retrieve the DATABASE_URL
WS_ENDPOINT = os.getenv("WS_ENDPOINT")
DATABASE_URL = os.getenv("DATABASE_URL")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
