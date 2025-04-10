import time
from typing import Any, Dict

import aiohttp

from app.utils.logger import log
from whatsapp.config import WHATSAPP_API_URL, WHATSAPP_TOKEN

# Track last active time for each user session
user_last_active: Dict[str, float] = {}
# Session timeout in seconds (e.g., 10 minutes)
SESSION_TIMEOUT = 600


async def send_whatsapp_message(phone_number: str, message: str) -> Dict[str, Any]:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone_number,
        "type": "text",
        "text": {"body": message},
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                WHATSAPP_API_URL, headers=headers, json=payload
            ) as response:
                result = await response.json()
                if response.status == 200:
                    return {"success": True, "data": result}
                else:
                    log("ERROR", f"WhatsApp API error: {result}")
                    return {"success": False, "error": result}
    except Exception as e:
        log("ERROR", f"WhatsApp send error: {str(e)}")
        return {"success": False, "error": str(e)}


def check_session_expired(session_id: str) -> bool:
    # Check if user session has expired
    current_time = time.time()
    last_active = user_last_active.get(session_id, 0)

    if last_active == 0:  # New user
        user_last_active[session_id] = current_time
        return True

    if (current_time - last_active) > SESSION_TIMEOUT:
        user_last_active[session_id] = current_time
        return True

    # Update last active time
    user_last_active[session_id] = current_time
    return False


# Update WhatsApp handler
async def handle_incoming_message(session_id: str, message: str, phone_number: str):
    check_session_expired(
        session_id
    )  # Still update session tracking, but don't send welcome message

    # Process the user's message normally
    from whatsapp.handler import process_whatsapp_message

    return await process_whatsapp_message(session_id, message, phone_number)
