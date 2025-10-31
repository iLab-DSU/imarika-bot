import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.langgraph_imarika import run_imarika_agent

# Page config
st.set_page_config(
    page_title="Imarika - Agricultural AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ChatGPT-style CSS
st.markdown("""
<style>
/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}

/* Main container */
.main {
    padding: 0;
    margin: 0;
}

/* ChatGPT-style layout */
.chat-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    height: 100vh;
    display: flex;
    flex-direction: column;
}

/* Header */
.chat-header {
    text-align: center;
    padding: 20px 0;
    border-bottom: 1px solid #e5e5e5;
    margin-bottom: 20px;
}

.chat-header h1 {
    font-size: 2rem;
    color: #2d3748;
    margin: 0;
    font-weight: 600;
}

.chat-header p {
    color: #718096;
    margin: 5px 0 0 0;
    font-size: 1rem;
}

/* Messages area */
.messages-container {
    flex: 1;
    overflow-y: auto;
    padding: 20px 0;
}

/* Message bubbles */
.message {
    margin-bottom: 20px;
    display: flex;
    align-items: flex-start;
}

.message.user {
    justify-content: flex-end;
}

.message.assistant {
    justify-content: flex-start;
}

.message-content {
    max-width: 70%;
    padding: 12px 16px;
    border-radius: 18px;
    font-size: 0.95rem;
    line-height: 1.4;
}

.message.user .message-content {
    background: #007bff;
    color: white;
    border-bottom-right-radius: 4px;
}

.message.assistant .message-content {
    background: #f1f3f4;
    color: #2d3748;
    border-bottom-left-radius: 4px;
}

/* Avatar */
.avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    margin: 0 10px;
    flex-shrink: 0;
}

.avatar.user {
    background: #007bff;
    color: white;
}

.avatar.assistant {
    background: #10a37f;
    color: white;
}

/* Input area */
.input-container {
    border-top: 1px solid #e5e5e5;
    padding: 20px 0;
    position: sticky;
    bottom: 0;
    background: white;
}

.input-box {
    display: flex;
    align-items: center;
    background: white;
    border: 1px solid #d1d5db;
    border-radius: 12px;
    padding: 12px 16px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.input-box:focus-within {
    border-color: #10a37f;
    box-shadow: 0 0 0 3px rgba(16,163,127,0.1);
}

/* Suggestions */
.suggestions {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    flex-wrap: wrap;
    justify-content: center;
}

.suggestion-chip {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 20px;
    padding: 8px 16px;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s;
}

.suggestion-chip:hover {
    background: #e9ecef;
    border-color: #10a37f;
}

/* Typing indicator */
.typing-indicator {
    display: flex;
    align-items: center;
    padding: 12px 16px;
    background: #f1f3f4;
    border-radius: 18px;
    border-bottom-left-radius: 4px;
    max-width: 70%;
}

.typing-dots {
    display: flex;
    gap: 4px;
}

.typing-dots span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #9ca3af;
    animation: typing 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {
    0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
    40% { transform: scale(1); opacity: 1; }
}

/* Responsive */
@media (max-width: 768px) {
    .chat-container {
        padding: 10px;
    }
    
    .message-content {
        max-width: 85%;
    }
    
    .suggestions {
        flex-direction: column;
    }
}
</style>
""", unsafe_allow_html=True)

def render_message(role, content, avatar_emoji):
    """Render a chat message"""
    if role == "user":
        st.markdown(f"""
        <div class="message user">
            <div class="message-content">{content}</div>
            <div class="avatar user">{avatar_emoji}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message assistant">
            <div class="avatar assistant">{avatar_emoji}</div>
            <div class="message-content">{content}</div>
        </div>
        """, unsafe_allow_html=True)

def show_typing_indicator():
    """Show typing indicator"""
    st.markdown("""
    <div class="message assistant">
        <div class="avatar assistant">🌾</div>
        <div class="typing-indicator">
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Main container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="chat-header">
        <h1>🌾 Imarika</h1>
        <p>Your AI Agricultural Assistant for East African Crops</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Suggestions (only show when no messages)
    if not st.session_state.messages:
        st.markdown("""
        <div class="suggestions">
            <div class="suggestion-chip" onclick="document.querySelector('input').value='What nutrients does maize need?'">
                What nutrients does maize need?
            </div>
            <div class="suggestion-chip" onclick="document.querySelector('input').value='How do I manage bean pests?'">
                How do I manage bean pests?
            </div>
            <div class="suggestion-chip" onclick="document.querySelector('input').value='What weather is good for cassava?'">
                What weather is good for cassava?
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Messages container
    messages_container = st.container()
    
    with messages_container:
        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                render_message("user", message["content"], "👤")
            else:
                render_message("assistant", message["content"], "🌾")
    
    # Input area
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Chat input
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        
        with col1:
            user_input = st.text_input(
                "Message Imarika...",
                placeholder="Ask about maize, beans, cassava, sorghum, finger millet, or sweet potatoes",
                label_visibility="collapsed"
            )
        
        with col2:
            submit = st.form_submit_button("Send", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle user input
    if submit and user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Show typing indicator
        with messages_container:
            render_message("user", user_input, "👤")
            show_typing_indicator()
        
        # Get AI response
        with st.spinner(""):
            try:
                response = run_imarika_agent(user_input)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = "Sorry, I'm having technical difficulties. Please try again."
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        st.rerun()

if __name__ == "__main__":
    main()