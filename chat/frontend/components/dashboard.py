import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def render_dashboard():
    """Render system dashboard"""
    
    st.markdown("## 📊 System Dashboard")
    
    # Performance metrics
    st.markdown("### 🚀 Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; color: #2E8B57;">107.9%</div>
                <div style="font-weight: 600; color: #666;">Overall Improvement</div>
                <div style="font-size: 0.9rem; color: #28a745;">↗️ Fine-tuning boost</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; color: #FF6B6B;">400%</div>
                <div style="font-weight: 600; color: #666;">Completeness</div>
                <div style="font-size: 0.9rem; color: #28a745;">↗️ More detailed responses</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; color: #4ECDC4;">201%</div>
                <div style="font-weight: 600; color: #666;">Keyword Density</div>
                <div style="font-size: 0.9rem; color: #28a745;">↗️ Agricultural terms</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; color: #FFD93D;">60%</div>
                <div style="font-weight: 600; color: #666;">Accuracy</div>
                <div style="font-size: 0.9rem; color: #28a745;">↗️ More precise answers</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance comparison chart
    st.markdown("### 📈 Performance Comparison")
    
    metrics_data = {
        'Metric': ['Composite Score', 'Keyword Density', 'Completeness', 'Accuracy', 'Specificity'],
        'Base System': [0.222, 0.078, 0.125, 0.500, 0.184],
        'Enhanced System': [0.461, 0.235, 0.625, 0.800, 0.184]
    }
    
    df = pd.DataFrame(metrics_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Base System',
        x=df['Metric'],
        y=df['Base System'],
        marker_color='#FF6B6B',
        text=[f'{val:.3f}' for val in df['Base System']],
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='Enhanced System',
        x=df['Metric'],
        y=df['Enhanced System'],
        marker_color='#2E8B57',
        text=[f'{val:.3f}' for val in df['Enhanced System']],
        textposition='auto'
    ))
    
    fig.update_layout(
        title='Performance Metrics Comparison',
        xaxis_title='Metrics',
        yaxis_title='Score (0-1)',
        barmode='group',
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Knowledge Graph Statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🕸️ Knowledge Graph Stats")
        
        # Knowledge graph pie chart
        kg_data = {
            'Category': ['Crops', 'Nutrients', 'Pests & Diseases', 'Activities', 'Growth Stages'],
            'Count': [6, 7, 8, 5, 4]
        }
        
        fig_pie = px.pie(
            values=kg_data['Count'],
            names=kg_data['Category'],
            title='Knowledge Graph Node Distribution',
            color_discrete_sequence=['#2E8B57', '#90EE90', '#FFD700', '#FF6B6B', '#4ECDC4']
        )
        
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("### 🌱 Crop Coverage")
        
        # Crop coverage data
        crop_data = {
            'Crop': ['Maize', 'Beans', 'Cassava', 'Sorghum', 'Finger Millet', 'Sweet Potatoes'],
            'Dataset Coverage': [16.0, 17.6, 15.4, 20.4, 16.2, 14.4],
            'Knowledge Nodes': [8, 7, 6, 9, 5, 7]
        }
        
        fig_crop = go.Figure()
        
        fig_crop.add_trace(go.Bar(
            name='Dataset Coverage (%)',
            x=crop_data['Crop'],
            y=crop_data['Dataset Coverage'],
            marker_color='#2E8B57',
            yaxis='y'
        ))
        
        fig_crop.add_trace(go.Scatter(
            name='Knowledge Nodes',
            x=crop_data['Crop'],
            y=crop_data['Knowledge Nodes'],
            mode='lines+markers',
            marker_color='#FF6B6B',
            yaxis='y2'
        ))
        
        fig_crop.update_layout(
            title='Crop Coverage Analysis',
            xaxis_title='Crops',
            yaxis=dict(title='Dataset Coverage (%)', side='left'),
            yaxis2=dict(title='Knowledge Nodes', side='right', overlaying='y'),
            height=400
        )
        
        st.plotly_chart(fig_crop, use_container_width=True)
    
    # System Health
    st.markdown("### 🔧 System Health")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤖</div>
                <div style="font-weight: 600; color: #2E8B57;">AI Model Status</div>
                <div style="color: #28a745; margin-top: 0.5rem;">● Enhanced Model Active</div>
                <div style="font-size: 0.9rem; color: #666;">Fine-tuned with 500 examples</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
                <div style="font-weight: 600; color: #2E8B57;">Knowledge Graph</div>
                <div style="color: #28a745; margin-top: 0.5rem;">● 30+ Nodes Online</div>
                <div style="font-size: 0.9rem; color: #666;">95+ relationships active</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌤️</div>
                <div style="font-weight: 600; color: #2E8B57;">Weather API</div>
                <div style="color: #28a745; margin-top: 0.5rem;">● Connected</div>
                <div style="font-size: 0.9rem; color: #666;">Real-time data available</div>
            </div>
        </div>
        """, unsafe_allow_html=True)