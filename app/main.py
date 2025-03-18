import os
import streamlit as st
import asyncio
import websockets
from app.ui.components import display_message
from app.config import WS_ENDPOINT

# Chat header
st.title("Imarika AI Chat Assistant")

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

