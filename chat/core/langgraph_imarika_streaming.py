import os
import json
import requests
import asyncio
from typing import Dict, List, Any, TypedDict, Iterator
from langchain_ollama import OllamaLLM
from langgraph.graph import StateGraph, END
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from knowledge_graph import AgriKnowledgeGraph
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from core.knowledge_graph import AgriKnowledgeGraph

# Optimized State definition
class AgentState(TypedDict):
    query: str
    tools_needed: List[str]
    weather_data: Dict[str, Any]
    knowledge_data: List[str]
    final_response: str
    step: str

# Fast LLM with optimized settings
llm = OllamaLLM(
    model="llama3", 
    temperature=0.1,
    num_predict=512,  # Limit response length for speed
    top_k=10,         # Reduce sampling for faster generation
    top_p=0.9
)

class FastWeatherTool:
    def __init__(self):
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes
    
    def run(self, location: str) -> Dict[str, Any]:
        # Check cache first
        cache_key = location.lower()
        current_time = time.time()
        
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if current_time - timestamp < self.cache_timeout:
                return cached_data
        
        api_key = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(url, timeout=3)  # Reduced timeout
            if response.status_code == 200:
                data = response.json()
                result = {
                    "location": location,
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"]
                }
                # Cache the result
                self.cache[cache_key] = (result, current_time)
                return result
        except:
            pass
        
        return {"error": "Weather unavailable"}

class FastKnowledgeGraphTool:
    def __init__(self):
        self.kg = AgriKnowledgeGraph()
        self.cache = {}
    
    def run(self, query: str) -> List[str]:
        # Simple caching for repeated queries
        cache_key = query.lower()
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        result = self.kg.query(query)
        self.cache[cache_key] = result
        return result

# Initialize tools
weather_tool = FastWeatherTool()
knowledge_tool = FastKnowledgeGraphTool()

def fast_planner(state: AgentState) -> AgentState:
    """Quick analysis without LLM for speed"""
    query = state["query"].lower()
    
    # Fast keyword-based tool selection
    tools_needed = ["knowledge_graph"]  # Always use KG for agricultural queries
    
    # Add weather if weather-related keywords found
    weather_keywords = ["weather", "hali ya hewa", "temperature", "joto", "rain", "mvua", "climate"]
    if any(keyword in query for keyword in weather_keywords):
        tools_needed.append("weather_api")
    
    return {
        **state,
        "tools_needed": tools_needed,
        "step": "executor"
    }

def parallel_executor(state: AgentState) -> AgentState:
    """Execute tools in parallel for speed"""
    query = state["query"]
    tools_needed = state["tools_needed"]
    
    weather_data = {}
    knowledge_data = []
    
    # Use ThreadPoolExecutor for parallel execution
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {}
        
        # Submit weather task
        if "weather_api" in tools_needed:
            location = extract_location(query)
            futures["weather"] = executor.submit(weather_tool.run, location)
        
        # Submit knowledge task
        if "knowledge_graph" in tools_needed:
            futures["knowledge"] = executor.submit(knowledge_tool.run, query)
        
        # Collect results as they complete
        for future in as_completed(futures.values()):
            try:
                if futures.get("weather") == future:
                    weather_data = future.result()
                elif futures.get("knowledge") == future:
                    knowledge_data = future.result()
            except Exception as e:
                print(f"Tool execution error: {e}")
    
    return {
        **state,
        "weather_data": weather_data,
        "knowledge_data": knowledge_data,
        "step": "synthesizer"
    }

def extract_location(query: str) -> str:
    """Fast location extraction"""
    locations = ["nairobi", "kampala", "dar", "kigali", "dodoma", "mombasa", "kisumu", "nakuru"]
    for word in query.lower().split():
        if word in locations:
            return word.capitalize()
    return "Nairobi"  # Default

def streaming_synthesizer(state: AgentState) -> Iterator[str]:
    """Generate streaming response"""
    query = state["query"]
    weather_data = state.get("weather_data", {})
    knowledge_data = state.get("knowledge_data", [])
    
    # Handle capability queries quickly
    if any(phrase in query.lower() for phrase in ["what can you do", "capabilities", "help", "who are you"]):
        response = "🌾 Habari! Ninaweza kukusaidia na:\n\n• 🌱 Mazao 6: Mahindi, Maharage, Mihogo, Ulezi, Mtama, Viazi vitamu\n• 🌤️ Hali ya hewa: Ushauri kulingana na mazingira\n• 📊 Uhusiano wa mazao: Mbolea, wadudu, magonjwa\n• 🔄 Mipango ya kilimo: Kupanda, kulima, kuvuna\n\nUliza swali lolote kuhusu mazao haya! 🚀"
        
        # Stream the response word by word
        words = response.split()
        for i, word in enumerate(words):
            if i == 0:
                yield word
            else:
                yield " " + word
            time.sleep(0.05)  # Small delay for streaming effect
        return
    
    # Build context quickly
    context_parts = []
    if knowledge_data:
        context_parts.append(f"Knowledge: {'; '.join(knowledge_data[:2])}")
    if weather_data and "error" not in weather_data:
        context_parts.append(f"Weather: {weather_data.get('temperature')}°C, {weather_data.get('description')}")
    
    context = " | ".join(context_parts)
    
    # Use subprocess for streaming ollama response
    prompt = f"""You are an agricultural assistant for East African crops.
Context: {context}
Question: {query}
Provide a concise, practical response in English or Swahili. Do not mention your name."""
    
    try:
        # Stream from ollama directly
        process = subprocess.Popen(
            ["ollama", "run", "llama3"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Send prompt
        process.stdin.write(prompt + "\n")
        process.stdin.flush()
        process.stdin.close()
        
        # Stream output
        buffer = ""
        while True:
            char = process.stdout.read(1)
            if not char:
                break
            
            buffer += char
            
            # Yield complete words
            if char in [' ', '\n', '.', ',', '!', '?']:
                if buffer.strip():
                    yield buffer
                    buffer = ""
        
        # Yield any remaining content
        if buffer.strip():
            yield buffer
            
        process.wait()
        
    except Exception as e:
        # Fallback to non-streaming
        fallback_response = f"Samahani, kuna tatizo la kiufundi. Jaribu tena.\n\nContext: {context}"
        yield fallback_response

def fast_synthesizer(state: AgentState) -> AgentState:
    """Non-streaming version for compatibility"""
    query = state["query"]
    weather_data = state.get("weather_data", {})
    knowledge_data = state.get("knowledge_data", [])
    
    # Quick responses for common queries
    if any(phrase in query.lower() for phrase in ["what can you do", "capabilities", "help"]):
        return {
            **state,
            "final_response": "🌾 Habari! Ninaweza kukusaidia na:\n• 🌱 Mazao 6: Mahindi, Maharage, Mihogo, Ulezi, Mtama, Viazi vitamu\n• 🌤️ Hali ya hewa na ushauri wa mazingira\n• 📊 Uhusiano wa mazao: Mbolea, wadudu, magonjwa\n\nUliza swali lolote kuhusu mazao haya! 🚀",
            "step": "end"
        }
    
    # Build minimal context
    context = ""
    if knowledge_data:
        context += f"Knowledge: {'; '.join(knowledge_data[:2])}\n"
    if weather_data and "error" not in weather_data:
        context += f"Weather: {weather_data.get('temperature')}°C, {weather_data.get('description')}\n"
    
    # Optimized prompt for speed
    prompt = f"""Agricultural assistant for East African crops. Context: {context}
Q: {query}
A: """
    
    try:
        # Fast subprocess call with timeout
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True,
            timeout=10  # Reduced timeout
        )
        response = result.stdout.strip()
        
        if not response:
            response = "Samahani, hakuna jibu. Jaribu swali lingine kuhusu kilimo."
            
    except Exception as e:
        response = f"Kuna tatizo la kiufundi. Jaribu tena baadaye."
    
    return {
        **state,
        "final_response": response,
        "step": "end"
    }

def should_continue(state: AgentState) -> str:
    """Fast routing"""
    step = state.get("step", "planner")
    return step if step != "end" else "end"

# Optimized graph
def create_fast_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("planner", fast_planner)
    workflow.add_node("executor", parallel_executor)
    workflow.add_node("synthesizer", fast_synthesizer)
    
    workflow.set_entry_point("planner")
    workflow.add_conditional_edges(
        "planner",
        should_continue,
        {"executor": "executor", "end": END}
    )
    workflow.add_conditional_edges(
        "executor", 
        should_continue,
        {"synthesizer": "synthesizer", "end": END}
    )
    workflow.add_edge("synthesizer", END)
    
    return workflow.compile()

# Main functions
def run_imarika_agent_fast(query: str) -> str:
    """Fast non-streaming version"""
    app = create_fast_graph()
    
    initial_state = {
        "query": query,
        "tools_needed": [],
        "weather_data": {},
        "knowledge_data": [],
        "final_response": "",
        "step": "planner"
    }
    
    result = app.invoke(initial_state)
    return result["final_response"]

def run_imarika_agent_streaming(query: str) -> Iterator[str]:
    """Streaming version"""
    # Fast planning and execution
    state = {"query": query, "tools_needed": [], "weather_data": {}, "knowledge_data": [], "final_response": "", "step": "planner"}
    
    # Quick planning
    state = fast_planner(state)
    
    # Parallel execution
    state = parallel_executor(state)
    
    # Stream response
    yield from streaming_synthesizer(state)

# Compatibility function
def run_imarika_agent(query: str) -> str:
    """Main function - uses fast version"""
    return run_imarika_agent_fast(query)

if __name__ == "__main__":
    # Test both versions
    test_query = "What nutrients does maize need?"
    
    print("🚀 Fast Response:")
    start_time = time.time()
    response = run_imarika_agent_fast(test_query)
    print(f"Time: {time.time() - start_time:.2f}s")
    print(f"Response: {response}\n")
    
    print("📡 Streaming Response:")
    start_time = time.time()
    for chunk in run_imarika_agent_streaming(test_query):
        print(chunk, end='', flush=True)
    print(f"\nTime: {time.time() - start_time:.2f}s")