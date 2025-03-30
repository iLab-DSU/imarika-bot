import requests

from app.config import DEFAULT_MODEL, OLLAMA_API_URL
from app.utils.logger import log


def call_ollama_api(messages: list) -> str:
    """
    Calls the Ollama API to generate a response for the given prompt.
    """
    # search for similar documents in the database

    headers = {"Content-Type": "application/json"}
    payload = {
        "model": DEFAULT_MODEL,  # Specify your desired model here
        "messages": messages,
        "stream": False,
    }
    try:
        response = requests.post(
            OLLAMA_API_URL, headers=headers, json=payload, timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            content = data.get("message", {}).get("content", "No response content.")
            return content
        else:
            log("ERROR", f"Ollama API error {response.status_code}: {response.text}")
            return f"API Error: {response.status_code}"
    except Exception as e:
        log("ERROR", f"Exception calling Ollama API: {e}")
        return f"API Error: {e}"


def format_message(message: str) -> str:
    """
    Helper to format messages.
    """
    return message.strip()
