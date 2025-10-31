#!/usr/bin/env python3

import time
from ollama_integration import OllamaFineTuned

def test_enhanced_model():
    """Quick test of enhanced model functionality"""
    
    model = OllamaFineTuned()
    
    test_cases = [
        ("What nutrients does maize need?", ["nitrogen", "phosphorus", "potassium"]),
        ("How do I manage pests in beans?", ["pest", "management", "beans"]),
        ("What weather is good for cassava?", ["weather", "cassava", "tropical"])
    ]
    
    print("🧪 Quick Enhanced Model Test")
    print("=" * 40)
    
    total_score = 0
    for query, expected_keywords in test_cases:
        print(f"\n📝 Query: {query}")
        
        start_time = time.time()
        response = model.generate_response(query)
        response_time = time.time() - start_time
        
        # Calculate keyword score
        found_keywords = sum(1 for keyword in expected_keywords if keyword.lower() in response.lower())
        score = found_keywords / len(expected_keywords)
        total_score += score
        
        print(f"⏱️  Time: {response_time:.2f}s")
        print(f"📊 Score: {score:.2f} ({found_keywords}/{len(expected_keywords)} keywords)")
        print(f"💬 Response: {response}")
        
        if score > 0.5:
            print("✅ PASS")
        else:
            print("❌ NEEDS IMPROVEMENT")
    
    avg_score = total_score / len(test_cases)
    print(f"\n📈 Average Score: {avg_score:.2f}")
    
    if avg_score > 0.6:
        print("🎉 Enhanced model is working well!")
    else:
        print("⚠️  Enhanced model needs optimization")

if __name__ == "__main__":
    test_enhanced_model()