import requests

from app.config import DEFAULT_MODEL, OLLAMA_API_URL


def call_ollama_api(prompt: str) -> str:
    """
    Calls the Ollama API to generate a response for the given prompt.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": DEFAULT_MODEL,  # Specify your desired model here
        "messages": [{"role": "user", "content": prompt}],
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


# langchain-ollama has direct function for this so api call is not needed
# def create_embeddings(text: str) -> List[float]:
#     """
#     Create embeddings for the given text using Ollama API.
#     """
#     headers = {"Content-Type": "application/json"}
#     payload = {
#         "model": EMBEDDING_MODEL,
#         "input": text
#     }
#     try:
#         response = requests.post(
#             OLLAMA_BASE_URL +"/api/embed", headers=headers, json=payload, timeout=10
#         )
#         response.raise_for_status()
#         embeddings = response.json().get("embeddings", [])
#     except requests.RequestException as e:
#         embeddings = []

#     return embeddings


def format_message(message: str) -> str:
    """
    Helper to format messages.
    """
    return message.strip()
