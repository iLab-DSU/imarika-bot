# whatsapp/handler.py
from typing import Dict, Optional

from app.utils.logger import log
from chain.conversation import save_message
from chain.llm_chain import generate_response
from chain.memory import MemoryManager
from whatsapp.client import send_whatsapp_message

# Store conversation memories for each user
user_memories: Dict[str, MemoryManager] = {}


def get_user_memory(session_id: str) -> MemoryManager:
    if session_id not in user_memories:
        user_memories[session_id] = MemoryManager()
    return user_memories[session_id]


async def process_whatsapp_message(
    session_id: str, message_text: str, phone_number: str = None
) -> Optional[str]:
    try:
        memory = get_user_memory(session_id)

        # Save user message to DB
        await save_message(session_id, "user", message_text)

        # Generate response
        response_text = ""
        try:
            async for chunk in generate_response(message_text, memory):
                response_text += chunk

            if not response_text.strip():
                response_text = (
                    "I'm sorry, I couldn't generate a response. Please try again."
                )
        except Exception as e:
            log("ERROR", f"Response generation error: {str(e)}")
            response_text = (
                "I'm sorry, I encountered an error while processing your request."
            )

        # Save bot response to DB
        await save_message(session_id, "bot", response_text)

        # Send response via WhatsApp if phone_number is provided
        if phone_number:
            await send_whatsapp_message(phone_number, response_text)

        return response_text

    except Exception as e:
        log("ERROR", f"WhatsApp message processing error: {str(e)}")
        if phone_number:
            await send_whatsapp_message(
                phone_number, "Sorry, I encountered an error. Please try again later."
            )
        return None
