import os
import streamlit as st
import asyncio
import websockets
from app.ui.components import display_message

# WebSocket endpoint for conversation server (append user id as needed)
WS_ENDPOINT = os.getenv("WS_ENDPOINT")

st.title("Advanced AI Bot")

user_input = st.text_input("Enter your message:")

if st.button("Send"):
    async def send_message():
        try:
            async with websockets.connect(WS_ENDPOINT) as websocket:
                await websocket.send(user_input)
                response = await websocket.recv()
                display_message("Bot", response)
        except Exception as e:
            display_message("Error", f"Connection error: {e}")

    asyncio.run(send_message())

