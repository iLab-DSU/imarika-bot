import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import random

def render_analytics():
    """Render analytics and insights page"""
    
    st.markdown("## 📈 Analytics & Insights")
    
    # Generate sample analytics data
    def generate_sample_data():
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        return {
            'dates': dates,
            'queries': [random.randint(10, 50) for _ in dates],
            'response_time': [random.uniform(1.5, 4.0) for _ in dates],
            'satisfaction': [random.uniform(3.5, 5.0) for _ in dates]
        }
    
    data = generate_sample_data()
    
    # Key metrics overview
    st.markdown("### 📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_queries = sum(data['queries'])
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; color: #2E8B57;">{total_queries}</div>
                <div style="font-weight: 600; color: #666;">Total Queries</div>
                <div style="font-size: 0.9rem; color: #28a745;">↗️ Last 30 days</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_response_time = sum(data['response_time']) / len(data['response_time'])
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; color: #4ECDC4;">{avg_response_time:.1f}s</div>
                <div style="font-weight: 600; color: #666;">Avg Response Time</div>
                <div style="font-size: 0.9rem; color: #28a745;">↗️ Fast responses</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_satisfaction = sum(data['satisfaction']) / len(data['satisfaction'])
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; color: #FFD93D;">{avg_satisfaction:.1f}/5</div>
                <div style="font-weight: 600; color: #666;">User Satisfaction</div>
                <div style="font-size: 0.9rem; color: #28a745;">↗️ High rating</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        uptime = 99.8
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; color: #96CEB4;">{uptime}%</div>
                <div style="font-weight: 600; color: #666;">System Uptime</div>
                <div style="font-size: 0.9rem; color: #28a745;">↗️ Reliable service</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Usage trends
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Query Volume Trends")
        
        fig_queries = go.Figure()
        fig_queries.add_trace(go.Scatter(
            x=data['dates'],
            y=data['queries'],
            mode='lines+markers',
            name='Daily Queries',
            line=dict(color='#2E8B57', width=3),
            marker=dict(size=6)
        ))
        
        fig_queries.update_layout(
            title='Daily Query Volume',
            xaxis_title='Date',
            yaxis_title='Number of Queries',
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig_queries, use_container_width=True)
    
    with col2:
        st.markdown("### ⚡ Response Time Analysis")
        
        fig_response = go.Figure()
        fig_response.add_trace(go.Scatter(
            x=data['dates'],
            y=data['response_time'],
            mode='lines+markers',
            name='Response Time',
            line=dict(color='#4ECDC4', width=3),
            marker=dict(size=6)
        ))
        
        fig_response.update_layout(
            title='Average Response Time',
            xaxis_title='Date',
            yaxis_title='Response Time (seconds)',
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig_response, use_container_width=True)
    
    # Query categories analysis
    st.markdown("### 🏷️ Query Categories")
    
    categories_data = {
        'Category': ['Nutrients', 'Pest Management', 'Weather', 'Planting', 'Harvesting', 'General'],
        'Count': [180, 150, 120, 100, 80, 70],
        'Avg Satisfaction': [4.2, 4.0, 4.5, 4.1, 3.9, 4.3]
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_categories = px.bar(
            x=categories_data['Category'],
            y=categories_data['Count'],
            title='Queries by Category',
            color=categories_data['Count'],
            color_continuous_scale='Greens'
        )
        fig_categories.update_layout(height=400)
        st.plotly_chart(fig_categories, use_container_width=True)
    
    with col2:
        fig_satisfaction = px.bar(
            x=categories_data['Category'],
            y=categories_data['Avg Satisfaction'],
            title='Satisfaction by Category',
            color=categories_data['Avg Satisfaction'],
            color_continuous_scale='Blues'
        )
        fig_satisfaction.update_layout(height=400)
        st.plotly_chart(fig_satisfaction, use_container_width=True)
    
    # Geographic distribution
    st.markdown("### 🌍 Geographic Usage")
    
    location_data = {
        'Location': ['Nairobi', 'Kampala', 'Dar es Salaam', 'Kigali', 'Dodoma', 'Mombasa'],
        'Users': [45, 32, 28, 25, 18, 15],
        'Queries': [320, 240, 200, 180, 120, 100]
    }
    
    fig_geo = go.Figure()
    
    fig_geo.add_trace(go.Bar(
        name='Users',
        x=location_data['Location'],
        y=location_data['Users'],
        marker_color='#2E8B57',
        yaxis='y'
    ))
    
    fig_geo.add_trace(go.Scatter(
        name='Queries',
        x=location_data['Location'],
        y=location_data['Queries'],
        mode='lines+markers',
        marker_color='#FF6B6B',
        yaxis='y2'
    ))
    
    fig_geo.update_layout(
        title='Usage by Location',
        xaxis_title='Location',
        yaxis=dict(title='Number of Users', side='left'),
        yaxis2=dict(title='Number of Queries', side='right', overlaying='y'),
        height=400
    )
    
    st.plotly_chart(fig_geo, use_container_width=True)
    
    # System insights
    st.markdown("### 💡 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #2E8B57; margin-bottom: 1rem;">🎯 Performance Highlights</h4>
            <ul style="list-style: none; padding: 0;">
                <li style="margin-bottom: 0.5rem;">✅ 107.9% improvement in overall performance</li>
                <li style="margin-bottom: 0.5rem;">✅ 400% increase in response completeness</li>
                <li style="margin-bottom: 0.5rem;">✅ 60% improvement in accuracy</li>
                <li style="margin-bottom: 0.5rem;">✅ 99.8% system uptime maintained</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #2E8B57; margin-bottom: 1rem;">📊 Usage Patterns</h4>
            <ul style="list-style: none; padding: 0;">
                <li style="margin-bottom: 0.5rem;">📈 Peak usage during planting season</li>
                <li style="margin-bottom: 0.5rem;">🌍 Highest adoption in Kenya and Uganda</li>
                <li style="margin-bottom: 0.5rem;">💬 Nutrient queries most common (25%)</li>
                <li style="margin-bottom: 0.5rem;">⭐ 4.2/5 average user satisfaction</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)