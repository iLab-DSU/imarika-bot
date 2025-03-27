import streamlit as st

from app.ui.components import (check_inactivity, clear_chat,
                               display_chat_history, handle_user_input,
                               init_session)

init_session()

st.set_page_config(page_title="Imarika Chat", page_icon="💬", layout="wide")

# Chat header
st.header("Imarika AI Chat Assistant :farmer:", divider="gray")

# Sidebar
if st.sidebar.button("Start New Chat"):
    clear_chat()

check_inactivity()

display_chat_history()

user_id = st.session_state["user_id"]

handle_user_input()
