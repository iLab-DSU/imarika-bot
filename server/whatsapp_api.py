import uuid

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.utils.logger import log
from whatsapp.client import check_session_expired
from whatsapp.config import WHATSAPP_VERIFY_TOKEN
from whatsapp.handler import process_whatsapp_message

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Map phone numbers to session IDs to avoid storing PII
phone_to_session = {}


@app.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode and token and mode == "subscribe" and token == WHATSAPP_VERIFY_TOKEN:
        log("INFO", "WhatsApp webhook verified")
        return Response(content=challenge, media_type="text/plain")

    raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
async def receive_message(request: Request):
    try:
        body = await request.json()

        if body.get("object") != "whatsapp_business_account":
            return {"status": "success"}

        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})

                for message in value.get("messages", []):
                    if message.get("type") == "text":
                        phone_number = message.get("from")
                        message_body = message.get("text", {}).get("body")

                        if phone_number and message_body:
                            # Check if session expired, and regenerate if needed
                            if (
                                phone_number not in phone_to_session
                                or check_session_expired(phone_to_session[phone_number])
                            ):
                                phone_to_session[phone_number] = str(uuid.uuid4())

                            session_id = phone_to_session[phone_number]
                            await process_whatsapp_message(
                                session_id, message_body, phone_number
                            )

        return {"status": "success"}
    except Exception as e:
        log("ERROR", f"Webhook error: {str(e)}")
        return {"status": "success"}
