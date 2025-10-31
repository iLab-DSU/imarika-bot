import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from components.header import render_header
from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface
from components.dashboard import render_dashboard
from components.analytics import render_analytics
from utils.session_manager import initialize_session
from utils.theme_manager import apply_custom_theme

# Page configuration
st.set_page_config(
    page_title="Imarika - Agricultural AI Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom theme
apply_custom_theme()

# Initialize session
initialize_session()

def main():
    """Main application entry point"""
    
    # Render header
    render_header()
    
    # Render sidebar and get current page
    current_page = render_sidebar()
    
    # Main content area
    if current_page == "Chat":
        render_chat_interface()
    elif current_page == "Dashboard":
        render_dashboard()
    elif current_page == "Analytics":
        render_analytics()
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<div style='text-align: center; color: #666; font-size: 0.9em;'>"
            "🌾 Imarika - Empowering East African Farmers with AI"
            "</div>",
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()