import asyncio
import random
import time

import streamlit as st
import websockets

from app.config import WS_ENDPOINT
from chain.memory import MemoryManager


def init_session():
    # Initialize session state variables if they don't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_activity" not in st.session_state:
        st.session_state.last_activity = time.time()
    if "memory" not in st.session_state:
        st.session_state.memory = MemoryManager()
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = random.randint(
            1, 2147483647
        )  # get a better replacement for this


def display_chat_history():
    # Displays all messages stored in session state
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def clear_chat():
    # Clears the chat history and resets session state
    st.session_state.messages = []
    st.session_state.last_activity = time.time()
    if "memory" in st.session_state:
        st.session_state.memory.clear()
    else:
        st.session_state.memory = MemoryManager()


def check_inactivity(timeout: int = 600):
    # Clears chat if inactive for the specified timeout in seconds
    if time.time() - st.session_state.last_activity > timeout:
        clear_chat()


async def send_message(user_input: str) -> str:
    # Sends a message via WebSocket and returns the response
    try:
        async with websockets.connect(
            f"{WS_ENDPOINT}/{st.session_state['user_id']}"
        ) as websocket:
            await websocket.send(user_input)
            response = await websocket.recv()
            return response
    except Exception as e:
        return f"Connection error: {e}"


def handle_user_input():
    # Handles user input, sends message, receives response, and updates session
    if user_input := st.chat_input("Enter your message..."):
        with st.chat_message("user"):
            st.markdown(user_input)

        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.memory.add_message(role="user", content=user_input)

        with st.spinner(""):
            response = asyncio.run(send_message(user_input))

        def response_generator():
            for word in response.split():
                yield word + " "
                time.sleep(0.05)

        with st.chat_message("assistant"):
            response = st.write_stream(response_generator())

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.memory.add_message(role="assistant", content=response)

        st.session_state.last_activity = time.time()
