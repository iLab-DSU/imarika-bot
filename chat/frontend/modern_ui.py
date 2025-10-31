import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.langgraph_imarika import run_imarika_agent

st.set_page_config(
    page_title="Imarika AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.main-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.hero-section {
    text-align: center;
    padding: 3rem 0;
    color: white;
}

.hero-title {
    font-size: 4rem;
    font-weight: 700;
    margin-bottom: 1rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.hero-subtitle {
    font-size: 1.5rem;
    font-weight: 300;
    opacity: 0.9;
    margin-bottom: 2rem;
}

.chat-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 2rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    margin: 2rem 0;
    flex: 1;
}

.message-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 1rem 0;
    margin-bottom: 2rem;
}

.message {
    margin-bottom: 1.5rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}

.message.user {
    flex-direction: row-reverse;
}

.message-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    flex-shrink: 0;
}

.message.user .message-avatar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.message.assistant .message-avatar {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    color: white;
}

.message-content {
    background: #f8f9fa;
    padding: 1rem 1.5rem;
    border-radius: 20px;
    max-width: 70%;
    line-height: 1.6;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.message.user .message-content {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.input-section {
    position: relative;
}

.input-container {
    display: flex;
    gap: 1rem;
    align-items: center;
    background: white;
    border-radius: 50px;
    padding: 0.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    border: 2px solid transparent;
    transition: all 0.3s ease;
}

.input-container:focus-within {
    border-color: #667eea;
    box-shadow: 0 4px 20px rgba(102,126,234,0.3);
}

.suggestions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}

.suggestion-card {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 16px;
    padding: 1.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
    color: white;
}

.suggestion-card:hover {
    background: rgba(255,255,255,0.2);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}

.suggestion-icon {
    font-size: 2rem;
    margin-bottom: 1rem;
}

.suggestion-title {
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.suggestion-desc {
    opacity: 0.8;
    font-size: 0.9rem;
}

.typing-indicator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem 1.5rem;
    background: #f8f9fa;
    border-radius: 20px;
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
    background: #667eea;
    animation: typing 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {
    0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
    40% { transform: scale(1); opacity: 1; }
}

.stats-bar {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin: 2rem 0;
    flex-wrap: wrap;
}

.stat-item {
    text-align: center;
    color: white;
}

.stat-number {
    font-size: 2rem;
    font-weight: 700;
    display: block;
}

.stat-label {
    font-size: 0.9rem;
    opacity: 0.8;
}

@media (max-width: 768px) {
    .hero-title { font-size: 2.5rem; }
    .hero-subtitle { font-size: 1.2rem; }
    .chat-card { padding: 1rem; margin: 1rem 0; }
    .suggestions-grid { grid-template-columns: 1fr; }
    .message-content { max-width: 85%; }
}
</style>
""", unsafe_allow_html=True)

def render_suggestions():
    suggestions = [
        {
            "icon": "🌽",
            "title": "Maize Nutrition",
            "desc": "Learn about nutrients needed for healthy maize growth",
            "query": "What nutrients does maize need for optimal growth?"
        },
        {
            "icon": "🐛",
            "title": "Pest Management",
            "desc": "Get advice on managing pests in your crops",
            "query": "How do I manage pests in beans effectively?"
        },
        {
            "icon": "🌤️",
            "title": "Weather Impact",
            "desc": "Understand how weather affects your farming",
            "query": "How does current weather affect cassava farming?"
        }
    ]
    
    cols = st.columns(3)
    for i, suggestion in enumerate(suggestions):
        with cols[i]:
            if st.button(f"{suggestion['icon']} {suggestion['title']}", key=f"sug_{i}", use_container_width=True):
                st.session_state.suggested_query = suggestion['query']

def main():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🌾 Imarika</div>
        <div class="hero-subtitle">AI-Powered Agricultural Assistant for East Africa</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Bar
    st.markdown("""
    <div class="stats-bar">
        <div class="stat-item">
            <span class="stat-number">6</span>
            <span class="stat-label">Supported Crops</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">107%</span>
            <span class="stat-label">AI Improvement</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">30+</span>
            <span class="stat-label">Knowledge Nodes</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">24/7</span>
            <span class="stat-label">Available</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat Card
    st.markdown('<div class="chat-card">', unsafe_allow_html=True)
    
    # Suggestions (only when no messages)
    if not st.session_state.messages:
        render_suggestions()
    
    # Messages
    if st.session_state.messages:
        st.markdown('<div class="message-container">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                st.markdown(f"""
                <div class="message user">
                    <div class="message-content">{content}</div>
                    <div class="message-avatar">👤</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message assistant">
                    <div class="message-avatar">🌾</div>
                    <div class="message-content">{content}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Input Section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    # Handle suggested query
    default_query = ""
    if hasattr(st.session_state, 'suggested_query'):
        default_query = st.session_state.suggested_query
        del st.session_state.suggested_query
    
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input(
                "Ask about maize, beans, cassava, sorghum, finger millet, or sweet potatoes...",
                value=default_query,
                label_visibility="collapsed"
            )
        with col2:
            submit = st.form_submit_button("Send", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle input
    if submit and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.spinner("🤔 Thinking..."):
            try:
                response = run_imarika_agent(user_input)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": "Sorry, I'm experiencing technical difficulties. Please try again."
                })
        
        st.rerun()

if __name__ == "__main__":
    main()