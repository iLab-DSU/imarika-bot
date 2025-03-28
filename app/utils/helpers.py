import requests

from app.config import DEFAULT_MODEL, OLLAMA_API_URL
from chain.vector_db import query_chroma_doc


def call_ollama_api(prompt: str) -> str:
    """
    Calls the Ollama API to generate a response for the given prompt.
    """
    # search for similar documents in the database
    context = query_chroma_doc(prompt)
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": DEFAULT_MODEL,  # Specify your desired model here
        "messages": [
            {
                "role": "user",
                "content": "Based on the following context, answer the question below.",
            },
            {"role": "user", "content": context},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
    }
    try:
        response = requests.post(
            OLLAMA_API_URL, headers=headers, json=payload, timeout=10
        )
        response.raise_for_status()
        content = (
            response.json().get("message", {}).get("content", "No response content.")
        )
        return content
    except requests.RequestException as e:
        return f"API Error: {e}"


def format_message(message: str) -> str:
    """
    Helper to format messages.
    """
    return message.strip()
