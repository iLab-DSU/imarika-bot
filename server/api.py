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


@app.get("/conversations/{session_id}")
async def read_conversation(session_id: str):
    """
    Retrieve the conversation history for a given user.
    """
    return await get_conversation(session_id)
