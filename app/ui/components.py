import streamlit as st

def chat_input() -> str:
    return st.text_input("Your message:")

def display_message(sender: str, message: str) -> None:
    st.markdown(f"**{sender}:** {message}")
