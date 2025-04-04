from typing import AsyncIterator

from app.utils.logger import log
from chain.memory import MemoryManager
from chain.vector_db import query_chroma_doc


async def generate_response(prompt: str, memory: MemoryManager) -> AsyncIterator[str]:
    try:
        context = query_chroma_doc(prompt)
        # Step 1: Update system message with vector context if provided
        if context:
            memory.update_system_message(context)

        async for chunk in memory.generate_response(prompt):
            if chunk:
                yield chunk

    except Exception as e:
        log("ERROR", f"Exception in generate_response: {e}")
        yield "An unexpected error occurred."
