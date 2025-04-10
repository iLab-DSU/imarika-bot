import streamlit as st

from app.ui.components import (
    check_inactivity,
    clear_chat,
    display_chat_history,
    handle_user_input,
    init_session,
)
from chain.vector_db import add_documents_from_csv

# Initialize session state
init_session()

# Set page config
st.set_page_config(page_title="Imarika Chat", page_icon="💬", layout="wide")

# Run on first load only: Add documents from CSV
if "docs_loaded" not in st.session_state:
    res = add_documents_from_csv()
    st.session_state["docs_loaded"] = True
    # st.info(f"Documents loaded: {res}")

# Header
st.title("Imarika AI Chat Assistant")

# Sidebar controls
with st.sidebar:
    if st.button("Start New Chat"):
        clear_chat()

    st.markdown("---")

    # WhatsApp URL
    # whatsapp_url = f"https://wa.me/15556413352" # update phone number in production
    # if st.button("Chat on WhatsApp"):
    #     st.markdown(f"[Click here: ]({whatsapp_url})", unsafe_allow_html=True)

    # if st.button("Reload Docs"):
    #     res = add_documents_from_csv()
    # st.info(f"Documents reloaded: {res}")

# Inactivity check
check_inactivity()

# Display chat history
display_chat_history()

# Handle user input
handle_user_input()
