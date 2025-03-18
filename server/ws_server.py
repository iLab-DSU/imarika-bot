import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from chain.llm_chain import generate_response
from chain.conversation import save_message
from app.utils.logger import log_to_db
from typing import Dict

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        # Store active WebSocket connections keyed by user_id
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[user_id] = websocket
        await log_to_db("INFO", f"User {user_id} connected via websocket.")

    async def disconnect(self, user_id: int) -> None:
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            await log_to_db("INFO", f"User {user_id} disconnected.")

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        await websocket.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await log_to_db("DEBUG", f"Received message from user {user_id}: {data}")
            # Save the user's message
            await save_message(user_id, "user", data)
            # Generate bot response
            response = generate_response(data)
            await save_message(user_id, "bot", response)
            await log_to_db("DEBUG", f"Sending response to user {user_id}: {response}")
            await manager.send_personal_message(response, websocket)
    except WebSocketDisconnect:
        await manager.disconnect(user_id)
    except Exception as e:
        await log_to_db("ERROR", f"Error in websocket for user {user_id}: {e}")
