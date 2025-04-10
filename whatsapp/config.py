import os

from dotenv import load_dotenv

load_dotenv()

# WhatsApp Cloud API credentials
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
WHATSAPP_VERSION = os.getenv("WHATSAPP_VERSION")

# WhatsApp API endpoints
WHATSAPP_API_URL = (
    f"https://graph.facebook.com/{WHATSAPP_VERSION}/{WHATSAPP_PHONE_ID}/messages"
)
