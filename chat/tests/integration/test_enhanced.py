#!/usr/bin/env python3

from core.langgraph_imarika import run_imarika_agent

def test_enhanced_system():
    """Test the enhanced agricultural system"""
    
    test_queries = [
        "What nutrients does maize need?",
        "How do I manage pests in beans?", 
        "What weather is good for cassava?"
    ]
    
    print("🧠 Testing Enhanced Imarika System")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 30)
        
        try:
            response = run_imarika_agent(query)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")
        
        print()

if __name__ == "__main__":
    test_enhanced_system()