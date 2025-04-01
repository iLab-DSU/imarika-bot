from typing import Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.utils.logger import log_to_db
from chain.conversation import save_message
from chain.llm_chain import generate_response
from chain.memory import MemoryManager

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        # Store active WebSocket connections keyed by user_id
        self.active_connections: Dict[int, WebSocket] = {}
        # Store conversation memory for each user
        self.user_memories: Dict[int, MemoryManager] = {}

    async def connect(self, user_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[user_id] = websocket
        # Initialize memory for this user if not exists
        if user_id not in self.user_memories:
            self.user_memories[user_id] = MemoryManager()
        await log_to_db("INFO", f"User {user_id} connected via websocket.")

    async def disconnect(self, user_id: int) -> None:
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            await log_to_db("INFO", f"User {user_id} disconnected.")

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        await websocket.send_text(message)

    def get_memory(self, user_id: int) -> MemoryManager:
        # Create memory if it does not exist
        if user_id not in self.user_memories:
            self.user_memories[user_id] = MemoryManager()
        return self.user_memories[user_id]


manager = ConnectionManager()


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await log_to_db("DEBUG", f"Received message from user {user_id}: {data}")

            # Get memory for this user
            memory = manager.get_memory(user_id)

            # Save the user's message to DB and memory
            await save_message(user_id, "user", data)

            # Signal stream start
            await websocket.send_json({"type": "stream_start"})

            response = ""

            async for chunk in generate_response(data, memory):
                response += chunk
                await websocket.send_json({"type": "stream_chunk", "content": chunk})

            # Signal end of streaming with full response
            await websocket.send_json({"type": "stream_end", "full_content": response})

            # Save bot response to DB and memory
            await save_message(user_id, "bot", response)

            await log_to_db(
                "DEBUG", f"Completed streaming response to user {user_id}: {response}"
            )
    except WebSocketDisconnect:
        await manager.disconnect(user_id)
    except Exception as e:
        await log_to_db("ERROR", f"Error in websocket for user {user_id}: {e}")
        try:
            await websocket.send_json(
                {"type": "error", "message": f"An error occurred: {str(e)}"}
            )
        except Exception as send_error:
            await log_to_db(
                "ERROR", f"Failed to send error message to user {user_id}: {send_error}"
            )
