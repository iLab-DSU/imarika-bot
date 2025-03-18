import os
import requests
from typing import Any

# Database connection string for Postgres
OLLAMA_URL = os.getenv("OLLAMA_URL")

def call_ollama_api(prompt: str) -> str:
    """
    Calls the Ollama API to generate a response for the given prompt.
    """
    try:
        response = requests.post(OLLAMA_URL, json={"prompt": prompt}, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "No response received.")
    except requests.RequestException as e:
        return f"API Error: {e}"

def format_message(message: str) -> str:
    """
    Helper to format messages.
    """
    return message.strip()

