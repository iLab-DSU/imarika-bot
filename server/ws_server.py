from typing import Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.utils.logger import log_to_db
from chain.conversation import save_message
from chain.llm_chain import generate_response
from chain.memory import MemoryManager

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        # Store active WebSocket connections keyed by session_id
        self.active_connections: Dict[int, WebSocket] = {}
        # Store conversation memory for each user
        self.user_memories: Dict[int, MemoryManager] = {}

    async def connect(self, session_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[session_id] = websocket
        # Initialize memory for this user if not exists
        if session_id not in self.user_memories:
            self.user_memories[session_id] = MemoryManager()
        await log_to_db("INFO", f"User {session_id} connected via websocket.")

    async def disconnect(self, session_id: str) -> None:
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            await log_to_db("INFO", f"User {session_id} disconnected.")

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        await websocket.send_text(message)

    def get_memory(self, session_id: str) -> MemoryManager:
        # Create memory if it does not exist
        if session_id not in self.user_memories:
            self.user_memories[session_id] = MemoryManager()
        return self.user_memories[session_id]


manager = ConnectionManager()


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(session_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await log_to_db("DEBUG", f"Received message from user {session_id}: {data}")

            # Get memory for this user
            memory = manager.get_memory(session_id)

            # Save the user's message to DB and memory
            await save_message(session_id, "user", data)
            memory.add_message("user", data)

            # Generate bot response with memory context
            response = generate_response(data, memory)

            # Save bot response to DB and memory
            await save_message(session_id, "bot", response)
            memory.add_message("assistant", response)

            await log_to_db(
                "DEBUG", f"Sending response to user {session_id}: {response}"
            )
            await manager.send_personal_message(response, websocket)
    except WebSocketDisconnect:
        await manager.disconnect(session_id)
    except Exception as e:
        await log_to_db("ERROR", f"Error in websocket for user {session_id}: {e}")
