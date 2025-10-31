# Agentic Imarika Architecture with LangGraph
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, List, Optional
import json

class AgentState(TypedDict):
    messages: List[HumanMessage | AIMessage]
    user_location: str
    selected_crops: List[str]
    weather_data: Optional[dict]
    knowledge_context: Optional[str]
    plan: Optional[List[str]]
    current_step: int

class AgenticImarika:
    def __init__(self, llm, weather_tool, knowledge_tool):
        self.llm = llm
        self.weather_tool = weather_tool
        self.knowledge_tool = knowledge_tool
        self.graph = self._build_graph()
    
    def _build_graph(self):
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("planner", self.planner_agent)
        workflow.add_node("weather_tool", self.weather_executor)
        workflow.add_node("knowledge_tool", self.knowledge_executor)
        workflow.add_node("synthesizer", self.synthesizer_agent)
        workflow.add_node("response_gen", self.response_generator)
        
        # Add edges with conditional logic
        workflow.set_entry_point("planner")
        workflow.add_conditional_edges(
            "planner",
            self.route_next_step,
            {
                "weather": "weather_tool",
                "knowledge": "knowledge_tool",
                "synthesize": "synthesizer",
                "end": END
            }
        )
        workflow.add_edge("weather_tool", "planner")
        workflow.add_edge("knowledge_tool", "planner")
        workflow.add_edge("synthesizer", "response_gen")
        workflow.add_edge("response_gen", END)
        
        return workflow.compile()
    
    def planner_agent(self, state: AgentState) -> AgentState:
        """LLM-based planner that creates execution plan"""
        query = state["messages"][-1].content
        
        plan_prompt = f"""
        Analyze this agricultural query: "{query}"
        User location: {state.get('user_location', 'Unknown')}
        User crops: {state.get('selected_crops', [])}
        
        Create a step-by-step plan. Choose from:
        - weather: Get current weather data
        - knowledge: Search agricultural documents
        - synthesize: Combine information and reason
        
        Return JSON: {{"steps": ["step1", "step2", ...]}}
        """
        
        response = self.llm.invoke(plan_prompt)
        try:
            plan_data = json.loads(response.content)
            state["plan"] = plan_data["steps"]
            state["current_step"] = 0
        except:
            state["plan"] = ["knowledge", "synthesize"]
            state["current_step"] = 0
        
        return state
    
    def route_next_step(self, state: AgentState) -> str:
        """Dynamic router based on current plan"""
        if not state.get("plan") or state["current_step"] >= len(state["plan"]):
            return "end"
        
        next_step = state["plan"][state["current_step"]]
        state["current_step"] += 1
        
        return next_step
    
    def weather_executor(self, state: AgentState) -> AgentState:
        """Execute weather tool"""
        weather_data = self.weather_tool.invoke(state["user_location"])
        state["weather_data"] = weather_data
        return state
    
    def knowledge_executor(self, state: AgentState) -> AgentState:
        """Execute knowledge search"""
        query = state["messages"][-1].content
        context = self.knowledge_tool.invoke(query)
        state["knowledge_context"] = context
        return state
    
    def synthesizer_agent(self, state: AgentState) -> AgentState:
        """Reasoning agent that combines information"""
        synthesis_prompt = f"""
        Synthesize information for agricultural advice:
        
        Query: {state["messages"][-1].content}
        Weather: {state.get("weather_data", "Not available")}
        Knowledge: {state.get("knowledge_context", "Not available")}
        User crops: {state.get("selected_crops", [])}
        
        Provide reasoned agricultural guidance.
        """
        
        response = self.llm.invoke(synthesis_prompt)
        state["synthesis"] = response.content
        return state
    
    def response_generator(self, state: AgentState) -> AgentState:
        """Final response generation"""
        final_response = f"""
        🌾 **Imarika's Agricultural Guidance**
        
        {state.get("synthesis", "No guidance available")}
        
        📍 Location: {state["user_location"]}
        🌱 Your crops: {", ".join(state["selected_crops"])}
        """
        
        state["messages"].append(AIMessage(content=final_response))
        return state

# Usage Example:
def create_agentic_imarika(llm, weather_tool, knowledge_tool):
    return AgenticImarika(llm, weather_tool, knowledge_tool)