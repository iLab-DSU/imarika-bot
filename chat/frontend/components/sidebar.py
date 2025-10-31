import streamlit as st

def render_sidebar():
    """Render enhanced sidebar with navigation and controls"""
    
    with st.sidebar:
        # Logo and branding
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; border-bottom: 2px solid #E0E0E0; margin-bottom: 1.5rem;">
            <div style="font-size: 3rem;">🌾</div>
            <div style="font-weight: 700; color: #2E8B57; font-size: 1.2rem;">Imarika AI</div>
            <div style="color: #666; font-size: 0.9rem;">Agricultural Assistant</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("### 🧭 Navigation")
        page = st.radio(
            "Select Page",
            ["Chat", "Dashboard", "Analytics"],
            index=0,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Location settings
        st.markdown("### 📍 Location Settings")
        location = st.selectbox(
            "Your Location",
            ["Nairobi", "Kampala", "Dar es Salaam", "Kigali", "Dodoma", "Mombasa", "Kisumu", "Nakuru"],
            index=0
        )
        
        if 'user_location' not in st.session_state:
            st.session_state.user_location = location
        else:
            st.session_state.user_location = location
        
        # Language settings
        st.markdown("### 🌍 Language")
        language = st.selectbox(
            "Preferred Language",
            ["English", "Swahili"],
            index=0
        )
        
        st.session_state.language = language
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🌤️ Check Weather", use_container_width=True):
            st.session_state.quick_action = "weather"
        
        if st.button("📊 View Knowledge Graph", use_container_width=True):
            st.session_state.quick_action = "knowledge_graph"
        
        if st.button("🔄 Clear Chat History", use_container_width=True):
            if 'messages' in st.session_state:
                st.session_state.messages = []
            st.success("Chat history cleared!")
        
        st.markdown("---")
        
        # System information
        st.markdown("### ℹ️ System Info")
        
        with st.expander("Performance Metrics"):
            st.markdown("""
            **Fine-Tuning Improvements:**
            - Overall Performance: +107.9%
            - Keyword Density: +201.3%
            - Completeness: +400.0%
            - Accuracy: +60.0%
            """)
        
        with st.expander("Supported Crops"):
            crops = [
                "🌽 Maize (Mahindi)",
                "🫘 Beans (Maharage)", 
                "🍠 Cassava (Mihogo)",
                "🌾 Finger Millet (Ulezi)",
                "🌾 Sorghum (Mtama)",
                "🍠 Sweet Potatoes (Viazi vitamu)"
            ]
            for crop in crops:
                st.markdown(f"- {crop}")
        
        with st.expander("Knowledge Graph Stats"):
            st.markdown("""
            - **Nodes**: 30+ agricultural entities
            - **Relationships**: 95+ connections
            - **Categories**: Crops, Nutrients, Pests, Activities
            - **Coverage**: Complete East African context
            """)
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.8rem;">
            <div>Version 2.0</div>
            <div>Enhanced with Fine-Tuning</div>
            <div style="margin-top: 0.5rem;">🚀 Built with LangGraph</div>
        </div>
        """, unsafe_allow_html=True)
    
    return page