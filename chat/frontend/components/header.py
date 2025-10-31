import streamlit as st
from datetime import datetime

def render_header():
    """Render professional header with branding"""
    
    st.markdown("""
    <div class="main-header fade-in">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h1>🌾 Imarika</h1>
                <p>Advanced Agricultural AI Assistant for East African Farmers</p>
            </div>
            <div style="text-align: right; color: rgba(255,255,255,0.8);">
                <div style="font-size: 0.9rem;">Powered by LangGraph & Knowledge Graph</div>
                <div style="font-size: 0.8rem; margin-top: 0.5rem;">Enhanced with Fine-Tuned AI</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Status indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 2rem; margin-right: 1rem;">🤖</div>
                <div>
                    <div style="font-weight: 600; color: #2E8B57;">AI Status</div>
                    <div style="color: #28a745; font-size: 0.9rem;">● Online</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 2rem; margin-right: 1rem;">📊</div>
                <div>
                    <div style="font-weight: 600; color: #2E8B57;">Knowledge Graph</div>
                    <div style="color: #28a745; font-size: 0.9rem;">30+ Nodes Active</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 2rem; margin-right: 1rem;">🌱</div>
                <div>
                    <div style="font-weight: 600; color: #2E8B57;">Supported Crops</div>
                    <div style="color: #28a745; font-size: 0.9rem;">6 Crops Ready</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 2rem; margin-right: 1rem;">⏰</div>
                <div>
                    <div style="font-weight: 600; color: #2E8B57;">Last Updated</div>
                    <div style="color: #666; font-size: 0.9rem;">{datetime.now().strftime('%H:%M')}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)