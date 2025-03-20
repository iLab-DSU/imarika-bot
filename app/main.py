import asyncio

import streamlit as st
import websockets

from app.config import WS_ENDPOINT
from app.ui.components import chat_input, display_message

# Chat header
st.title("Imarika AI Chat Assistant")

# Sidebar
st.sidebar.header("Chat History")
# Add code to display previous chats as a list
st.sidebar.button("Start New Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    display_message(message["role"], message["content"])

# React to user input
if user_input := chat_input():
    display_message("user", user_input)
    try:

        async def send_message():
            async with websockets.connect(WS_ENDPOINT) as websocket:
                await websocket.send(user_input)
                return await websocket.recv()

        # Run the async function and get the response
        response = asyncio.run(send_message())

    except Exception as e:
        response = f"Connection error: {e}"

    display_message("assistant", response)
