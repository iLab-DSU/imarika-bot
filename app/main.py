import streamlit as st

from app.ui.components import (
    check_inactivity,
    clear_chat,
    display_chat_history,
    handle_user_input,
    init_session,
)
from chain.vector_db import add_documents_from_csv

init_session()

st.set_page_config(page_title="Imarika Chat", page_icon="💬", layout="wide")

# Chat header
st.title("Imarika AI Chat Assistant")

# Sidebar
if st.sidebar.button("Start New Chat"):
    clear_chat()
if st.sidebar.button("Load Docs"):
    res = add_documents_from_csv()
    st.info(res)
check_inactivity()

display_chat_history()

user_id = st.session_state["user_id"]

handle_user_input()
