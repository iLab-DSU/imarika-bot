import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from core.langgraph_imarika import run_imarika_agent
from utils.weather_widget import render_weather_widget
from utils.typing_animation import show_typing_animation

def render_chat_interface():
    """Render enhanced chat interface"""
    
    # Weather widget
    render_weather_widget()
    
    # Chat container
    st.markdown('<div class="chat-container fade-in">', unsafe_allow_html=True)
    
    # Quick suggestions
    st.markdown("### 💡 Quick Suggestions")
    
    col1, col2, col3 = st.columns(3)
    
    suggestions = [
        "What nutrients does maize need?",
        "How do I manage bean pests?",
        "What weather is good for cassava?"
    ]
    
    for i, (col, suggestion) in enumerate(zip([col1, col2, col3], suggestions)):
        with col:
            if st.button(f"💬 {suggestion}", key=f"suggestion_{i}", use_container_width=True):
                st.session_state.suggested_query = suggestion
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "🌾 Habari! Mimi ni Imarika, mshauri wako wa kilimo wa mazao ya Afrika Mashariki. Ninaweza kukusaidia na maswali kuhusu mahindi, maharage, mihogo, ulezi, mtama, na viazi vitamu. Uliza swali lolote!"
            }
        ]
    
    # Display chat messages
    st.markdown("### 💬 Chat with Imarika")
    
    # Chat messages container
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message fade-in">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <div style="font-size: 1.2rem; margin-right: 0.5rem;">👤</div>
                        <div style="font-weight: 600; color: #1976D2;">You</div>
                    </div>
                    <div>{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message fade-in">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <div style="font-size: 1.2rem; margin-right: 0.5rem;">🌾</div>
                        <div style="font-weight: 600; color: #2E8B57;">Imarika</div>
                        <div style="margin-left: auto; font-size: 0.8rem; color: #666;">Enhanced AI</div>
                    </div>
                    <div>{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    
    # Handle suggested query
    default_query = ""
    if hasattr(st.session_state, 'suggested_query'):
        default_query = st.session_state.suggested_query
        del st.session_state.suggested_query
    
    # Input form
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "Ask Imarika about agriculture...",
                value=default_query,
                placeholder="e.g., What nutrients does maize need?",
                label_visibility="collapsed"
            )
        
        with col2:
            submit_button = st.form_submit_button("Send 🚀", use_container_width=True)
    
    # Process user input
    if submit_button and user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Show typing animation
        with st.spinner("🤔 Imarika is thinking..."):
            # Get AI response
            try:
                response = run_imarika_agent(user_input)
                
                # Add assistant response
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_response = f"Samahani, kuna tatizo la kiufundi. Jaribu tena baadaye. (Sorry, there's a technical issue. Please try again later.) Error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_response})
        
        # Rerun to show new messages
        st.rerun()
    
    # Handle quick actions
    if hasattr(st.session_state, 'quick_action'):
        if st.session_state.quick_action == "weather":
            location = st.session_state.get('user_location', 'Nairobi')
            weather_query = f"What's the weather like in {location} for farming?"
            st.session_state.messages.append({"role": "user", "content": weather_query})
            
            with st.spinner("🌤️ Getting weather information..."):
                response = run_imarika_agent(weather_query)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            del st.session_state.quick_action
            st.rerun()
        
        elif st.session_state.quick_action == "knowledge_graph":
            kg_query = "Tell me about the relationships between crops, nutrients, and pests in your knowledge graph"
            st.session_state.messages.append({"role": "user", "content": kg_query})
            
            with st.spinner("📊 Accessing knowledge graph..."):
                response = run_imarika_agent(kg_query)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            del st.session_state.quick_action
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat statistics
    if len(st.session_state.messages) > 1:
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💬 Messages", len(st.session_state.messages))
        
        with col2:
            user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
            st.metric("❓ Questions Asked", user_messages)
        
        with col3:
            avg_response_length = sum(len(m["content"]) for m in st.session_state.messages if m["role"] == "assistant") // max(1, len([m for m in st.session_state.messages if m["role"] == "assistant"]))
            st.metric("📝 Avg Response Length", f"{avg_response_length} chars")