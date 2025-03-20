import streamlit as st


def chat_input() -> str:
    return st.chat_input("Enter your message...")


def display_message(sender: str, message: str) -> None:
    role = "user" if sender.lower() == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message)

    if "messages" in st.session_state:
        # Check if this exact message isn't the last one (to avoid duplicates)
        if not st.session_state.messages or st.session_state.messages[-1] != {
            "role": role,
            "content": message,
        }:
            st.session_state.messages.append({"role": role, "content": message})
