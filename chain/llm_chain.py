from app.utils.helpers import call_ollama_api
from app.utils.logger import log
from chain.memory import MemoryManager
from chain.vector_db import query_chroma_doc


def generate_response(prompt: str, memory: MemoryManager) -> str:
    try:
        context = query_chroma_doc(prompt)
        # Step 1: Update system message with vector context if provided
        if context:
            memory.update_system_message(context)

        # Step 2: Add user message to memory
        memory.add_message(role="user", content=prompt)

        # Step 3: Get full conversation history
        history = memory.get_history()

        # Step 4: Call Ollama API with full context
        response = call_ollama_api(history)

        # Step 5: Check and handle API response
        if not response or response.startswith("API Error"):
            log(
                "WARNING",
                f"Empty or error response from Ollama API for prompt: {prompt}",
            )
            return "Sorry, I'm having trouble generating a response at the moment."

        # Step 6: Add assistant response to memory
        memory.add_message(role="assistant", content=response)

        return response

    except Exception as e:
        log("ERROR", f"Exception in generate_response: {e}")
        return "An unexpected error occurred."
