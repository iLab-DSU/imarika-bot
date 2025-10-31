import os
import json
import requests
import pandas as pd
from typing import Dict, List, Any, TypedDict
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langgraph.graph import StateGraph, END
import chromadb
try:
    from knowledge_graph import AgriKnowledgeGraph
except ImportError:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from core.knowledge_graph import AgriKnowledgeGraph

# State definition
class AgentState(TypedDict):
    query: str
    plan: str
    tools_needed: List[str]
    weather_data: Dict[str, Any]
    knowledge_data: List[str]
    final_response: str
    step: str

# Initialize models
llm = OllamaLLM(model="llama3", temperature=0.1)
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

class WeatherTool:
    def __init__(self):
        self.name = "weather_api"
        self.description = "Get current weather data for agricultural advice"
    
    def run(self, location: str) -> Dict[str, Any]:
        api_key = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")
        
        # Current weather
        current_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        # 5-day forecast
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
        
        try:
            # Get current weather
            current_response = requests.get(current_url, timeout=10)
            forecast_response = requests.get(forecast_url, timeout=10)
            
            result = {"location": location}
            
            if current_response.status_code == 200:
                current_data = current_response.json()
                result.update({
                    "temperature": current_data["main"]["temp"],
                    "humidity": current_data["main"]["humidity"],
                    "description": current_data["weather"][0]["description"],
                    "wind_speed": current_data["wind"]["speed"],
                    "pressure": current_data["main"]["pressure"]
                })
            
            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()
                # Get next 3 days forecast
                forecasts = []
                for i in range(0, min(24, len(forecast_data["list"])), 8):  # Every 24 hours
                    item = forecast_data["list"][i]
                    forecasts.append({
                        "date": item["dt_txt"][:10],
                        "temp": item["main"]["temp"],
                        "description": item["weather"][0]["description"]
                    })
                result["forecast"] = forecasts[:3]
            
            return result
        except:
            pass
        return {"error": "Weather data unavailable"}

class KnowledgeGraphTool:
    def __init__(self):
        self.name = "knowledge_graph"
        self.description = "Query agricultural knowledge graph for crop relationships"
        self.kg = AgriKnowledgeGraph()
    
    def run(self, query: str) -> List[str]:
        return self.kg.query(query)

# Initialize tools
weather_tool = WeatherTool()
knowledge_tool = KnowledgeGraphTool()

# Agent functions
def planner_agent(state: AgentState) -> AgentState:
    """Analyzes query and creates execution plan"""
    query = state["query"]
    
    prompt = f"""As Imarika, an agricultural assistant, analyze this query and determine what tools are needed:
Query: {query}

Available tools:
- weather_api: For weather-related questions
- knowledge_graph: For crop information from our database

Respond with:
1. PLAN: Brief execution strategy
2. TOOLS: List tools needed (weather_api, knowledge_graph, or both)

Focus only on: Beans, Cassava, Finger Millet, Maize, Sorghum, Sweet Potatoes."""
    
    response = llm.invoke(prompt)
    
    # Parse response - always use knowledge graph for agricultural queries
    tools_needed = ["knowledge_graph"]
    
    # Add weather tool if weather-related
    weather_keywords = ["weather", "hali ya hewa", "temperature", "joto", "rain", "mvua", "climate", "tabianchi"]
    if any(keyword in query.lower() for keyword in weather_keywords):
        tools_needed.append("weather_api")
    
    return {
        **state,
        "plan": response,
        "tools_needed": tools_needed,
        "step": "executor"
    }

def executor(state: AgentState) -> AgentState:
    """Executes tools based on plan"""
    query = state["query"]
    tools_needed = state["tools_needed"]
    
    weather_data = {}
    knowledge_data = []
    
    # Execute weather tool
    if "weather_api" in tools_needed:
        # Use user's location from session state or extract from query
        location = "Nairobi"  # Default fallback
        
        # Try to get location from session state (if available)
        try:
            import streamlit as st
            if hasattr(st, 'session_state') and hasattr(st.session_state, 'user_location') and st.session_state.user_location:
                location = st.session_state.user_location
        except:
            pass
        
        # Extract location from query if mentioned
        for word in query.split():
            if word.lower() in ["nairobi", "kampala", "dar", "kigali", "dodoma", "mombasa", "kisumu", "nakuru"]:
                location = word
                break
        
        weather_data = weather_tool.run(location)
    
    # Execute knowledge tool
    if "knowledge_graph" in tools_needed:
        knowledge_data = knowledge_tool.run(query)
    
    return {
        **state,
        "weather_data": weather_data,
        "knowledge_data": knowledge_data,
        "step": "synthesizer"
    }

def synthesizer(state: AgentState) -> AgentState:
    """Combines tool results and generates response using enhanced context"""
    query = state["query"]
    weather_data = state.get("weather_data", {})
    knowledge_data = state.get("knowledge_data", [])
    
    # Try to use enhanced synthesizer with fine-tuned context
    try:
        import sys
        import os
        fine_tuning_path = os.path.join(os.path.dirname(__file__), '..', 'fine_tuning')
        sys.path.append(fine_tuning_path)
        from ollama_integration import OllamaFineTuned
        
        enhanced_model = OllamaFineTuned()
        
        # Prepare context
        context_parts = []
        if knowledge_data:
            context_parts.append(f"Agricultural Knowledge: {'; '.join(knowledge_data[:3])}")
        if weather_data and "error" not in weather_data:
            weather_info = f"Weather in {weather_data.get('location', 'Unknown')}: {weather_data.get('temperature', 'N/A')}°C, {weather_data.get('description', 'N/A')}"
            context_parts.append(weather_info)
        
        context = " | ".join(context_parts)
        
        # Use enhanced model for agricultural queries
        response = enhanced_model.generate_response(query, context)
        
        # Add greeting for capability queries without redundant name
        if any(word in query.lower() for word in ['what can you do', 'capabilities', 'help', 'about']):
            response = "🌾 Habari! " + response
        
        return {
            **state,
            "final_response": response,
            "step": "end"
        }
        
    except Exception as e:
        print(f"Enhanced model unavailable, using fallback: {e}")
        # Continue with original logic below
    
    # Handle general questions about capabilities
    if any(phrase in query.lower() for phrase in ["what can you do", "what do you do", "who are you", "help", "capabilities"]):
        return {
            **state,
            "final_response": "🌾 Habari! Ninaweza kukusaidia na:\n\n• 🌱 Mazao 6: Mahindi, Maharage, Mihogo, Ulezi, Mtama, Viazi vitamu\n• 🌤️ Hali ya hewa: Ushauri kulingana na mazingira ya sasa\n• 📊 Uhusiano wa mazao: Mbolea, wadudu, magonjwa\n• 🔄 Mipango ya kilimo: Kupanda, kulima, kuvuna\n• 💡 Ushauri wa kisasa: Kutumia teknolojia ya Knowledge Graph\n\nMfano wa maswali:\n- Mahindi yanahitaji mbolea gani?\n- Hali ya hewa inaathirije mihogo?\n- Wadudu gani wanashambulia maharage?\n- Ni wakati gani bora wa kupanda mtama?\n\nUliza swali lolote kuhusu mazao haya! 🚀",
            "step": "end"
        }
    
    # Check if query is related to our crops (more comprehensive matching)
    crop_keywords = [
        "beans", "maharage", "bean", "cassava", "mihogo", "finger millet", "ulezi", "millet",
        "maize", "mahindi", "corn", "sorghum", "mtama", "sweet potatoes", "viazi vitamu", "potato",
        "pest", "pests", "wadudu", "disease", "magonjwa", "nutrient", "nutrients", "mbolea",
        "plant", "planting", "kupanda", "farming", "kilimo", "grow", "growing", "kukuza",
        "harvest", "harvesting", "kuvuna", "cultivation", "kulima"
    ]
    
    is_crop_related = any(keyword in query.lower() for keyword in crop_keywords) or knowledge_data or weather_data
    
    if not is_crop_related:
        return {
            **state,
            "final_response": "Samahani, mimi ni Imarika, mshauri wa kilimo. Ninajua tu kuhusu mahindi, maharage, mihogo, ulezi, mtama, na viazi vitamu. Je, una swali kuhusu mazao haya?",
            "step": "end"
        }
    
    # Build context
    context = ""
    if knowledge_data:
        context += f"Agricultural Knowledge:\n{chr(10).join(knowledge_data[:3])}\n\n"
    
    if weather_data and "error" not in weather_data:
        context += f"Current Weather in {weather_data.get('location', 'Unknown')}:\n"
        context += f"Temperature: {weather_data.get('temperature', 'N/A')}°C\n"
        context += f"Humidity: {weather_data.get('humidity', 'N/A')}%\n"
        context += f"Conditions: {weather_data.get('description', 'N/A')}\n"
        context += f"Wind Speed: {weather_data.get('wind_speed', 'N/A')} m/s\n"
        
        # Add forecast if available
        if 'forecast' in weather_data:
            context += "\n3-Day Forecast:\n"
            for day in weather_data['forecast']:
                context += f"- {day['date']}: {day['temp']}°C, {day['description']}\n"
        context += "\n"
    
    prompt = f"""You are an agricultural assistant specializing in 6 crops: Beans, Cassava, Finger Millet, Maize, Sorghum, and Sweet Potatoes.

Context:
{context}

User Question: {query}

Provide a helpful response in English or Swahili as appropriate. Be practical and specific. If weather data is available, include relevant agricultural advice based on current conditions. Do not mention your name in responses."""
    
    try:
        response = llm.invoke(prompt)
    except Exception as e:
        # Fallback to subprocess ollama
        import subprocess
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3", prompt],
                capture_output=True,
                text=True,
                timeout=15
            )
            response = result.stdout.strip()
        except Exception as e2:
            response = f"Technical error occurred: {str(e2)}"
    
    return {
        **state,
        "final_response": response,
        "step": "end"
    }

def should_continue(state: AgentState) -> str:
    """Router function for conditional logic"""
    step = state.get("step", "planner")
    
    if step == "executor":
        return "executor"
    elif step == "synthesizer":
        return "synthesizer"
    else:
        return "end"

# Build the graph
def create_graph():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("planner", planner_agent)
    workflow.add_node("executor", executor)
    workflow.add_node("synthesizer", synthesizer)
    
    # Add edges
    workflow.set_entry_point("planner")
    workflow.add_conditional_edges(
        "planner",
        should_continue,
        {
            "executor": "executor",
            "end": END
        }
    )
    workflow.add_conditional_edges(
        "executor",
        should_continue,
        {
            "synthesizer": "synthesizer",
            "end": END
        }
    )
    workflow.add_edge("synthesizer", END)
    
    return workflow.compile()

# Main function
def run_imarika_agent(query: str) -> str:
    """Main function to run the LangGraph agent"""
    app = create_graph()
    
    initial_state = {
        "query": query,
        "plan": "",
        "tools_needed": [],
        "weather_data": {},
        "knowledge_data": [],
        "final_response": "",
        "step": "planner"
    }
    
    result = app.invoke(initial_state)
    return result["final_response"]

if __name__ == "__main__":
    # Test the system
    test_queries = [
        "What are the best practices for growing maize?",
        "How does weather affect cassava farming?",
        "Tell me about beans cultivation in Nairobi",
        "What is quantum physics?",  # Should be rejected
    ]
    
    print("🌾 Imarika LangGraph Agent Testing 🌾\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"Test {i}: {query}")
        print("-" * 50)
        response = run_imarika_agent(query)
        print(f"Response: {response}\n")