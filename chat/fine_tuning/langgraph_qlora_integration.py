#!/usr/bin/env python3
"""
LangGraph Integration with QLoRA Fine-tuned Model
Integrates the fine-tuned model into the existing LangGraph system
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from typing import Dict, List, Any, TypedDict
from qlora_model_integration import IntegratedImarika
from core.knowledge_graph import AgriKnowledgeGraph
import requests
import time

# State definition (same as original)
class AgentState(TypedDict):
    query: str
    tools_needed: List[str]
    weather_data: Dict[str, Any]
    knowledge_data: List[str]
    final_response: str
    step: str

class QLoRAWeatherTool:
    def __init__(self):
        self.cache = {}
        self.cache_timeout = 300
    
    def run(self, location: str) -> Dict[str, Any]:
        cache_key = location.lower()
        current_time = time.time()
        
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if current_time - timestamp < self.cache_timeout:
                return cached_data
        
        api_key = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                data = response.json()
                result = {
                    "location": location,
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"]
                }
                self.cache[cache_key] = (result, current_time)
                return result
        except:
            pass
        
        return {"error": "Weather unavailable"}

class QLoRAKnowledgeGraphTool:
    def __init__(self):
        self.kg = AgriKnowledgeGraph()
        self.cache = {}
    
    def run(self, query: str) -> List[str]:
        cache_key = query.lower()
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        result = self.kg.query(query)
        self.cache[cache_key] = result
        return result

class QLoRALangGraphAgent:
    def __init__(self):
        self.imarika_model = IntegratedImarika()
        self.weather_tool = QLoRAWeatherTool()
        self.knowledge_tool = QLoRAKnowledgeGraphTool()
        
        print(f"🌾 QLoRA LangGraph Agent Initialized")
        print(f"   Model: {self.imarika_model.get_model_info()['model_type']}")
        print(f"   Device: {self.imarika_model.get_model_info().get('device', 'CPU')}")
    
    def fast_planner(self, state: AgentState) -> AgentState:
        """Quick planning without LLM"""
        query = state["query"].lower()
        
        tools_needed = ["knowledge_graph"]
        
        # Add weather if weather-related
        weather_keywords = ["weather", "hali ya hewa", "temperature", "joto", "rain", "mvua", "climate"]
        if any(keyword in query for keyword in weather_keywords):
            tools_needed.append("weather_api")
        
        return {
            **state,
            "tools_needed": tools_needed,
            "step": "executor"
        }
    
    def parallel_executor(self, state: AgentState) -> AgentState:
        """Execute tools in parallel"""
        query = state["query"]
        tools_needed = state["tools_needed"]
        
        weather_data = {}
        knowledge_data = []
        
        # Execute weather tool
        if "weather_api" in tools_needed:
            location = self.extract_location(query)
            weather_data = self.weather_tool.run(location)
        
        # Execute knowledge tool
        if "knowledge_graph" in tools_needed:
            knowledge_data = self.knowledge_tool.run(query)
        
        return {
            **state,
            "weather_data": weather_data,
            "knowledge_data": knowledge_data,
            "step": "synthesizer"
        }
    
    def extract_location(self, query: str) -> str:
        """Extract location from query"""
        locations = ["nairobi", "kampala", "dar", "kigali", "dodoma", "mombasa", "kisumu", "nakuru"]
        for word in query.lower().split():
            if word in locations:
                return word.capitalize()
        return "Nairobi"
    
    def qlora_synthesizer(self, state: AgentState) -> AgentState:
        """Generate response using QLoRA model"""
        query = state["query"]
        weather_data = state.get("weather_data", {})
        knowledge_data = state.get("knowledge_data", [])
        
        # Handle capability queries
        if any(phrase in query.lower() for phrase in ["what can you do", "capabilities", "help", "who are you"]):
            model_info = self.imarika_model.get_model_info()
            response = f"🌾 Habari! Ninaweza kukusaidia na:\n\n• 🌱 Mazao 6: Mahindi, Maharage, Mihogo, Ulezi, Mtama, Viazi vitamu\n• 🌤️ Hali ya hewa na ushauri wa mazingira\n• 📊 Uhusiano wa mazao: Mbolea, wadudu, magonjwa\n• 🧠 Enhanced AI: {model_info['model_type']}\n\nUliza swali lolote kuhusu mazao haya! 🚀"
            
            return {
                **state,
                "final_response": response,
                "step": "end"
            }
        
        # Build context for QLoRA model
        context_parts = []
        if knowledge_data:
            context_parts.append(f"Agricultural Knowledge: {'; '.join(knowledge_data[:3])}")
        if weather_data and "error" not in weather_data:
            context_parts.append(f"Weather in {weather_data.get('location')}: {weather_data.get('temperature')}°C, {weather_data.get('description')}")
        
        context = " | ".join(context_parts)
        
        # Generate response using QLoRA model
        try:
            response = self.imarika_model.generate_response(query, context)
            
            # Add model indicator for fine-tuned responses
            if self.imarika_model.use_qlora:
                response = f"{response}\n\n🧠 *Enhanced by QLoRA fine-tuning*"
            
        except Exception as e:
            response = f"Samahani, kuna tatizo la kiufundi. Jaribu tena baadaye.\n\nError: {str(e)[:100]}..."
        
        return {
            **state,
            "final_response": response,
            "step": "end"
        }
    
    def run_agent(self, query: str) -> str:
        """Main agent execution"""
        # Initialize state
        state = {
            "query": query,
            "tools_needed": [],
            "weather_data": {},
            "knowledge_data": [],
            "final_response": "",
            "step": "planner"
        }
        
        # Execute pipeline
        state = self.fast_planner(state)
        state = self.parallel_executor(state)
        state = self.qlora_synthesizer(state)
        
        return state["final_response"]

# Main function for compatibility
def run_qlora_imarika_agent(query: str) -> str:
    """Main function to run QLoRA-enhanced agent"""
    agent = QLoRALangGraphAgent()
    return agent.run_agent(query)

# Streaming version (placeholder for future implementation)
def run_qlora_imarika_agent_streaming(query: str):
    """Streaming version - future implementation"""
    agent = QLoRALangGraphAgent()
    response = agent.run_agent(query)
    
    # Simple word-by-word streaming simulation
    words = response.split()
    for i, word in enumerate(words):
        if i == 0:
            yield word
        else:
            yield " " + word
        time.sleep(0.05)

if __name__ == "__main__":
    # Test the QLoRA agent
    print("🧪 Testing QLoRA LangGraph Agent...")
    
    agent = QLoRALangGraphAgent()
    
    test_queries = [
        "What nutrients does maize need?",
        "How to control bean weevils?",
        "Best weather for cassava planting?",
        "What can you do?"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        print("=" * 50)
        
        start_time = time.time()
        response = agent.run_agent(query)
        end_time = time.time()
        
        print(f"Response: {response}")
        print(f"Time: {end_time - start_time:.2f}s")
        print(f"Model: {agent.imarika_model.get_model_info()['model_type']}")