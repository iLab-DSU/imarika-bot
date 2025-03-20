from app.utils.helpers import call_ollama_api
from app.utils.logger import log


def generate_response(prompt: str) -> str:
    """
    Generate a response by calling the Ollama API.
    Improved with error handling and logging.
    """
    try:
        response = call_ollama_api(prompt)
        if not response or response.startswith("API Error"):
            log(
                "WARNING",
                f"Empty or error response from Ollama API for prompt: {prompt}",
            )
            return "Sorry, I'm having trouble generating a response at the moment."
        return response
    except Exception as e:
        log("ERROR", f"Exception in generate_response: {e}")
        return "An unexpected error occurred."
