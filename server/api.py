from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chain.conversation import get_conversation

app = FastAPI()

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
