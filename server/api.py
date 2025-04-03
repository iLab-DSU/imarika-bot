from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter

from app.ui.components import api_send_message, get_user_id
from chain.conversation import get_conversation

app = FastAPI()
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production security
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/conversations/{user_id}")
async def read_conversation(user_id: int):
    """
    Retrieve the conversation history for a given user.
    """
    return await get_conversation(user_id)


@app.get("/test")
async def test():
    """
    Test endpoint to check if the server is running.
    """
    return {"message": "Server is running!"}


@app.get("/user_id")
async def get_user_id_endpoint():
    """
    Endpoint to retrieve the user ID from the session state.
    """
    user_id = get_user_id()
    return {"user_id": user_id}


@app.post("/chat/{user_id}")
async def chat(user_id: int, message: str) -> Union[str, dict]:
    """
    Handle chat messages and return responses.
    """
    # Placeholder for chat logic
    response = await api_send_message(message, user_id)
    return response
