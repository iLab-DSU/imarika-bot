import asyncio
import time

import streamlit as st
import websockets

from app.config import WS_ENDPOINT


def init_session():
    # Initialize session state variables if they don't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_activity" not in st.session_state:
        st.session_state.last_activity = time.time()


def display_chat_history():
    # Displays all messages stored in session state
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def clear_chat():
    # Clears the chat history and resets session state
    st.session_state.messages = []
    st.session_state.last_activity = time.time()


def check_inactivity(timeout: int = 60):
    # Clears chat if inactive for the specified timeout (test with 60 seconds)
    if time.time() - st.session_state.last_activity > timeout:
        clear_chat()


async def send_message(user_input: str) -> str:
    # Sends a message via WebSocket and returns the response
    try:
        async with websockets.connect(WS_ENDPOINT) as websocket:
            await websocket.send(user_input)
            return await websocket.recv()
    except Exception as e:
        return f"Connection error: {e}"


def handle_user_input():
    # Handles user input, sends message, receives response, and updates session
    if user_input := st.chat_input("Enter your message..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = asyncio.run(send_message(user_input))
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.last_activity = time.time()
