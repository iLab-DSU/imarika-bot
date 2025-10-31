import streamlit as st
import time
import sys
import os
import requests # Import requests here for cleaner code
import matplotlib.pyplot as plt
import networkx as nx

# Add parent directory to path to allow import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Assuming these modules are in the path or same directory
# Ensure langgraph_imarika.py and knowledge_graph.py exist alongside this script
try:
    from langgraph_imarika_streaming import run_imarika_agent_fast, run_imarika_agent_streaming
    from knowledge_graph import AgriKnowledgeGraph
    STREAMING_AVAILABLE = True
except ImportError:
    try:
        from langgraph_imarika import run_imarika_agent as run_imarika_agent_fast
        from knowledge_graph import AgriKnowledgeGraph
        run_imarika_agent_streaming = None
        STREAMING_AVAILABLE = False
    except ImportError as e:
        st.error(f"Module import error: {e}. Please ensure agent modules are accessible.")
        def run_imarika_agent_fast(prompt): return "Error: Agent not loaded."
        run_imarika_agent_streaming = None
        STREAMING_AVAILABLE = False
        class AgriKnowledgeGraph:
            def __init__(self):
                self.graph = nx.DiGraph()
                self.graph.add_nodes_from(['A', 'B', 'C'])
                self.graph.add_edges_from([('A', 'B', {'relation': 'test'}), ('B', 'C', {'relation': 'test'})])
            def number_of_nodes(self): return 0
            def number_of_edges(self): return 0

# Page config
st.set_page_config(
    page_title="Imarika",
    page_icon="🌾",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_location" not in st.session_state:
    st.session_state.user_location = "Nairobi" # Default location for better start
if "weather_data" not in st.session_state:
    st.session_state.weather_data = None

# --- Sidebar ---
with st.sidebar:
    st.markdown("## 🌾 Imarika AI") # Larger title for branding
    st.markdown("**Your Agricultural Assistant**")
    
    st.markdown("---") # Visual separator
    
    # Navigation Block (Using a container for visual grouping)
    with st.container(border=True):
        st.subheader("🧭 Navigation")
        page = st.selectbox(
            "Go to:", # More direct label
            ["💬 Chat", "📊 Knowledge Graph", "📋 Graph Data"],
            label_visibility="collapsed" # Hide the default label for a cleaner look
        )

    st.markdown("---")
    
    # Location and Weather Block (Using a form for better UX)
    st.markdown("### 📍 Location & Weather")
    
    with st.form("location_form", clear_on_submit=False):
        location_input = st.text_input(
            "Enter your location:",
            value=st.session_state.user_location,
            placeholder="e.g., Nairobi, Kampala, Dar es Salaam",
            label_visibility="collapsed" # Save space
        )
        
        submitted = st.form_submit_button("🌤️ Get Weather Data", use_container_width=True, type="primary") # Primary button style
        
        if submitted:
            if location_input:
                st.session_state.user_location = location_input
                # Fetch weather data
                try:
                    # NOTE: Replace 'your_api_key_here' with an actual key or use os.getenv
                    api_key = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here") 
                    if api_key == "your_api_key_here":
                        st.error("Please set the OPENWEATHER_API_KEY environment variable.")
                    else:
                        url = f"http://api.openweathermap.org/data/2.5/weather?q={location_input}&appid={api_key}&units=metric"
                        response = requests.get(url, timeout=10)
                        
                        if response.status_code == 200:
                            st.session_state.weather_data = response.json()
                            st.toast(f"Weather updated for {location_input}!", icon='✅')
                        else:
                            st.error(f"Could not fetch weather data for {location_input}. Status: {response.status_code}")
                            st.session_state.weather_data = None
                except requests.exceptions.RequestException:
                    st.error("Weather service unavailable or network error.")
                st.rerun() # Rerun to update weather display

    # Display current weather with st.metric
    if st.session_state.weather_data:
        weather = st.session_state.weather_data
        
        with st.container(border=True):
            st.markdown(f"**Current Weather in {st.session_state.user_location}:**")
            col_t, col_h = st.columns(2)
            
            # Use st.metric for professional data display
            col_t.metric(
                label="Temperature", 
                value=f"{weather['main']['temp']}°C", 
                delta=weather['weather'][0]['main'] # Main condition
            )
            col_h.metric(
                label="Humidity", 
                value=f"{weather['main']['humidity']}%",
                delta=weather['weather'][0]['description'].title() # Detailed description
            )
            
    st.markdown("---")
    
    # Utility Buttons
    col_clear, col_reset = st.columns(2)
    with col_clear:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col_reset:
        if st.button("🔄 Reset All", use_container_width=True):
            st.session_state.messages = []
            st.session_state.user_location = "Nairobi"
            st.session_state.weather_data = None
            st.rerun()
            
    st.markdown("---")
    
    # System info with performance indicators
    with st.expander("**⚙️ System Info**"):
        streaming_status = "✅ Enabled" if STREAMING_AVAILABLE else "❌ Disabled"
        st.markdown(f"""
        - **Model**: Llama3 + LangGraph 🧠
        - **Streaming**: {streaming_status} 📡
        - **Knowledge**: 22 nodes, 72 edges 📊
        - **Crops**: 6 specialized crops 🌱
        - **Languages**: English & Swahili 🇰🇪
        - **Response Time**: ~2-5s ⚡
        """)

# --- Main Content Area ---

if page == "💬 Chat":
    streaming_indicator = " 📡" if STREAMING_AVAILABLE else " ⚡"
    st.title(f"💬 Chat with Imarika{streaming_indicator}")
    
    # Welcome message if no chat history
    if not st.session_state.messages:
        st.header("👋 Habari! Welcome to your agricultural advisor.")
        st.markdown("""
        Get help with **6 specialized crops** (Maize, Beans, Cassava, Millet, Sorghum, Sweet Potatoes) 
        and receive **weather-contextualized advice** on nutrients, pests, and farming practices.
        
        🚀 **Enhanced Performance**: Fast responses with streaming support for better user experience! 
        """)
        
        # --- REMOVED QUICK START BUTTONS HERE ---
        # st.subheader("💡 Quick Start Questions:")
        # cols = st.columns(4) 
        # questions = [...]
        # for i, q in enumerate(questions):
        #      with cols[i]:
        #         if st.button(q, use_container_width=True, help="Click to send this question to Imarika."):
        #             st.session_state.messages.append({"role": "user", "content": q})
        #             st.rerun()
        # --- END OF REMOVED SECTION ---

        # Add a final encouraging prompt after removing the buttons
        st.markdown("**Start by typing your question in the chat box below!**")
        
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # Chat input
    location_prompt = f" for {st.session_state.user_location}" if st.session_state.user_location else ""
    prompt_placeholder = f"Ask about crops, weather, or farming practices{location_prompt}..."
    
    if prompt := st.chat_input(prompt_placeholder):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Generate response with streaming support
        with st.chat_message("assistant"):
            try:
                location_context = f" [User location: {st.session_state.user_location}]" if st.session_state.user_location else ""
                enhanced_prompt = prompt + location_context
                
                if STREAMING_AVAILABLE and run_imarika_agent_streaming:
                    # Streaming response
                    response_placeholder = st.empty()
                    full_response = ""
                    
                    with st.spinner("🌾 Imarika is thinking..."):
                        for chunk in run_imarika_agent_streaming(enhanced_prompt):
                            full_response += chunk
                            response_placeholder.markdown(full_response + "▌")  # Cursor effect
                            time.sleep(0.02)  # Smooth streaming
                    
                    response_placeholder.markdown(full_response)  # Final response
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    # Fast non-streaming response
                    with st.spinner("🚀 Generating response..."):
                        response = run_imarika_agent_fast(enhanced_prompt)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        
            except Exception as e:
                error_msg = f"🚨 Samahani, kuna tatizo la kiufundi. Jaribu tena baadaye.\n\nError: {str(e)[:100]}..."
                st.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

elif page == "📊 Knowledge Graph":
    st.title("📊 Knowledge Graph Visualization")
    
    try:
        kg = AgriKnowledgeGraph()
        
        # Statistics (using metrics)
        st.subheader("Graph Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Nodes", kg.graph.number_of_nodes())
        with col2:
            st.metric("Total Edges", kg.graph.number_of_edges())
        with col3:
            node_types = len(set(d.get('type', 'unknown') for _, d in kg.graph.nodes(data=True)))
            st.metric("Distinct Node Types", node_types)
            
        st.markdown("---")
            
        st.subheader("Interactive Visualization")
        
        # Create visualization (Matplotlib is used here, though pyvis is recommended for v2)
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Using a fixed seed for layout stability
        pos = nx.spring_layout(kg.graph, k=2, iterations=50, seed=42) 
        
        # Colors for node types
        colors = {
            'crop': '#10b981', 'nutrient': '#3b82f6', 'pest': '#ef4444',
            'activity': '#f59e0b', 'stage': '#8b5cf6', 'unknown': '#64748b'
        }
        
        # Collect nodes by type and draw
        for node_type, color in colors.items():
            nodes = [n for n, d in kg.graph.nodes(data=True) if d.get('type', 'unknown') == node_type]
            if nodes:
                nx.draw_networkx_nodes(kg.graph, pos, nodelist=nodes, 
                                        node_color=color, node_size=800, alpha=0.8, ax=ax)
        
        # Draw edges
        nx.draw_networkx_edges(kg.graph, pos, alpha=0.3, width=1, edge_color='gray', ax=ax)
        
        # Draw labels (use smaller font for readability in dense graphs)
        nx.draw_networkx_labels(kg.graph, pos, font_size=8, ax=ax)
        
        ax.set_title("Agricultural Knowledge Graph", fontsize=16, pad=20)
        ax.axis('off')
        
        # Legend (ensuring only relevant types are shown)
        legend_elements = []
        for node_type, color in colors.items():
            nodes_count = len([n for n, d in kg.graph.nodes(data=True) if d.get('type', 'unknown') == node_type])
            if nodes_count > 0:
                # Custom artist for the legend
                from matplotlib.lines import Line2D
                legend_elements.append(Line2D([0], [0], marker='o', color='w', 
                                                markerfacecolor=color, markersize=10, 
                                                label=f"{node_type.title()} ({nodes_count})"))
        
        if legend_elements:
            ax.legend(handles=legend_elements, loc='best', fontsize=10)
        
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Error loading knowledge graph: {e}")

elif page == "📋 Graph Data":
    st.title("📋 Knowledge Graph Data Details")
    
    try:
        kg = AgriKnowledgeGraph()
        
        # Statistics
        st.subheader("Data Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Nodes", kg.graph.number_of_nodes())
        with col2:
            st.metric("Total Edges", kg.graph.number_of_edges())
        with col3:
            node_types = len(set(d.get('type', 'unknown') for _, d in kg.graph.nodes(data=True)))
            st.metric("Distinct Node Types", node_types)
            
        st.markdown("---")
        
        # Nodes by type (More detail using expanders)
        st.subheader("Nodes Details")
        node_types_list = sorted(list(set(d.get('type', 'unknown') for _, d in kg.graph.nodes(data=True))))
        
        for node_type in node_types_list:
            nodes = [n for n, d in kg.graph.nodes(data=True) if d.get('type', 'unknown') == node_type]
            if nodes:
                with st.expander(f"**{node_type.title()}s** ({len(nodes)})"):
                    st.code(", ".join(nodes))
        
        st.markdown("---")
        
        # Sample relationships (using a data frame or table for better structure)
        st.subheader("Sample Relationships (First 20)")
        relationships = []
        for source, target, data in list(kg.graph.edges(data=True))[:20]:
            relation = data.get('relation', 'related_to')
            relationships.append({
                "Source Node": source,
                "Relationship": relation,
                "Target Node": target
            })
            
        if relationships:
            # Use st.dataframe for a cleaner look
            st.dataframe(relationships, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error loading graph data: {e}")