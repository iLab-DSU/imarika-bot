import streamlit as st
import time
from langgraph_imarika import run_imarika_agent, create_graph

# Page config
st.set_page_config(
    page_title="Imarika LangGraph Agent",
    page_icon="🌾",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #2E8B57, #228B22);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.chat-message {
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    border-left: 4px solid #2E8B57;
    background-color: #f0f8f0;
}
.agent-flow {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #dee2e6;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🌾 Imarika LangGraph Agent</h1>
    <p>Advanced Agricultural Assistant with Dynamic Planning</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Architecture Info
with st.sidebar:
    st.header("🔧 LangGraph Architecture")
    st.markdown("""
    **Current Flow:**
    1. **Planner Agent** - Analyzes query
    2. **Tool Router** - Selects tools needed
    3. **Executor** - Runs weather/knowledge tools
    4. **Synthesizer** - Combines results
    5. **Response Generator** - Final output
    
    **Available Tools:**
    - 🌤️ Weather API
    - 📚 Knowledge Graph (6 crops)
    
    **Supported Crops:**
    - Beans, Cassava, Finger Millet
    - Maize, Sorghum, Sweet Potatoes
    """)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_steps" not in st.session_state:
    st.session_state.agent_steps = []

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Chat with Imarika")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about crops, weather, or farming practices..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Show agent processing
        with st.chat_message("assistant"):
            with st.spinner("🤖 Imarika is thinking..."):
                # Create placeholder for streaming
                response_placeholder = st.empty()
                
                # Run the LangGraph agent
                try:
                    response = run_imarika_agent(prompt)
                    
                    # Simulate streaming response
                    displayed_text = ""
                    for char in response:
                        displayed_text += char
                        response_placeholder.markdown(displayed_text + "▌")
                        time.sleep(0.01)
                    
                    # Final response without cursor
                    response_placeholder.markdown(response)
                    
                    # Add to session state
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = f"Samahani, kuna tatizo la kiufundi. Jaribu tena baadaye. (Error: {str(e)})"
                    response_placeholder.markdown(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

with col2:
    st.header("🔍 Agent Flow Monitor")
    
    # Show current architecture
    st.markdown("""
    <div class="agent-flow">
    <h4>🧠 Current Process Flow</h4>
    <ol>
        <li><strong>Planner Agent</strong><br>
        <small>Analyzes query intent</small></li>
        
        <li><strong>Tool Router</strong><br>
        <small>Selects appropriate tools</small></li>
        
        <li><strong>Executor</strong><br>
        <small>Runs weather/knowledge tools</small></li>
        
        <li><strong>Synthesizer</strong><br>
        <small>Combines tool outputs</small></li>
        
        <li><strong>Response Generator</strong><br>
        <small>Creates final answer</small></li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick test buttons
    st.subheader("🚀 Quick Tests")
    
    test_queries = [
        "What are the best practices for growing maize?",
        "How does current weather affect cassava farming in Nairobi?",
        "Tell me about beans cultivation",
        "What is quantum physics?"  # Should be rejected
    ]
    
    for i, query in enumerate(test_queries):
        if st.button(f"Test {i+1}: {query[:30]}...", key=f"test_{i}"):
            # Add to chat
            st.session_state.messages.append({"role": "user", "content": query})
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🌾 Imarika LangGraph Agent - Powered by Ollama & LangGraph</p>
    <p><small>Specialized in: Beans • Cassava • Finger Millet • Maize • Sorghum • Sweet Potatoes</small></p>
</div>
""", unsafe_allow_html=True)

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.session_state.agent_steps = []
    st.rerun()