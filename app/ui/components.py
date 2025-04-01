import asyncio
import json
import random
import time
from typing import Any, Dict

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
    if "current_response" not in st.session_state:
        st.session_state.current_response = ""


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
    st.session_state.current_response = ""


def check_inactivity(timeout: int = 600):
    # Clears chat if inactive for the specified timeout in seconds
    if time.time() - st.session_state.last_activity > timeout:
        clear_chat()


async def receive_message(websocket) -> Dict[str, Any]:
    # process streaming messages from the websocket
    response = ""
    placeholder = st.empty()

    while True:
        try:
            data = await websocket.recv()
            message = json.loads(data)

            message_type = message.get("type", "")

            if message_type == "stream_start":
                st.session_state.current_response = ""

            elif message_type == "stream_chunk":
                chunk = message.get("content", "")
                st.session_state.current_response += chunk
                # Update the displayed message with each chunk
                placeholder.markdown(st.session_state.current_response)

            elif message_type == "stream_end":
                response = message.get(
                    "full_content", st.session_state.current_response
                )
                placeholder.markdown(response)
                return {"content": response}

            elif message_type == "error":
                error_msg = message.get("message", "An unknown error occurred")
                placeholder.markdown(f"⚠️ {error_msg}")
                return {"content": error_msg}

        except Exception as e:
            return {"content": f"Connection error: {e}"}


async def send_message(user_input: str) -> Dict[str, Any]:
    # Sends a message via WebSocket and returns the response
    try:
        async with websockets.connect(
            f"{WS_ENDPOINT}/{st.session_state['user_id']}"
        ) as websocket:
            await websocket.send(user_input)
            return await receive_message(websocket)
    except Exception as e:
        return {"content": f"Connection error: {e}"}


def handle_user_input():
    # Handles user input, sends message, receives response, and updates session
    if user_input := st.chat_input("Enter your message..."):
        with st.chat_message("user"):
            st.markdown(user_input)

        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.memory.add_message(role="user", content=user_input)

        with st.chat_message("assistant"):
            response = asyncio.run(send_message(user_input))

        st.session_state.messages.append(
            {"role": "assistant", "content": response["content"]}
        )
        st.session_state.last_activity = time.time()
