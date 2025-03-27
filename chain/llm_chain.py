from app.config import CHAT_SYSTEM_INSTRUCTION
from app.utils.helpers import call_ollama_api
from app.utils.logger import log
from chain.memory import MemoryManager


def generate_response(prompt: str, memory: MemoryManager) -> str:
    # Generate a response using conversation history from memory.
    try:
        context = memory.get_summary()

        enhanced_prompt = f"{CHAT_SYSTEM_INSTRUCTION}\n\n{context}\n\n{prompt}"

        response = call_ollama_api(enhanced_prompt)

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
