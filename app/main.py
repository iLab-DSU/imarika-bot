import asyncio
import os

import streamlit as st
import websockets

from app.config import WS_ENDPOINT
from app.ui.components import display_message
from chain.vector_db import (add_documents_from_csv,
                             query_chroma_doc)

# Chat header
st.title("Imarika AI Chat Assistant")

user_input = st.text_input("Enter your message:")

# Get the parent directory and remove 4 characters from the end
parent_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = parent_dir[:-4]
st.write("Parent Directory: " + parent_dir)
data_path = os.path.join(parent_dir, "data")
st.write("Data Path: " + data_path)

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

elif st.button("Add Docs"):
    response = add_documents_from_csv(data_path)
    display_message("VectorDB", response)
    display_message("VectorDB", "created successfully using data from " + data_path)

elif st.button("Query Docs"):
    response = query_chroma_doc(user_input, 5)
    display_message("VectorDB", response[2])
