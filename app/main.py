import os
import streamlit as st
import asyncio
import websockets
from app.ui.components import display_message
from app.config import WS_ENDPOINT
from chain.vector_db import create_vector_store, query_vector_db, add_documents_from_csv

# Chat header
st.title("Imarika AI Chat Assistant")

user_input = st.text_input("Enter your message:")

abs_path = os.path.abspath(__file__)
st.write("Absolute Path: " + abs_path)
# Get the parent directory and remove 4 characters from the end
parent_dir = os.path.dirname(abs_path)
parent_dir = parent_dir[:-4]
st.write("Parent Directory: " + parent_dir)
data_path = os.path.join(parent_dir, "data")
st.write("Data Path: " + data_path)
v_path = os.path.join(parent_dir, "db")
st.write("Vector Path: " + v_path)

if st.button("Send"):
    async def send_message():
        try:
            vdb = create_vector_store(persist=True, path=v_path)
            add_documents_from_csv(vdb, data_path)
            async with websockets.connect(WS_ENDPOINT) as ws:
                await ws.send(user_input)
                response = query_vector_db(vdb, user_input, 5)
                display_message("VectorDB", response)
        except Exception as e:
            display_message("Error", f"Connection error: {e}")

    asyncio.run(send_message())

