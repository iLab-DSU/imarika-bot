#!/usr/bin/env python3

from core.langgraph_imarika import run_imarika_agent
import time

def evaluate_responses():
    """Evaluate system responses for quality metrics"""
    
    test_cases = [
        {
            "query": "What nutrients does maize need?",
            "expected_keywords": ["nitrogen", "phosphorus", "potassium", "NPK", "manure"],
            "category": "Nutrients"
        },
        {
            "query": "How do I manage bean pests?", 
            "expected_keywords": ["pesticide", "rotation", "organic", "weevil"],
            "category": "Pest Management"
        },
        {
            "query": "What can you do?",
            "expected_keywords": ["Imarika", "crops", "agricultural", "assistant"],
            "category": "Capabilities"
        }
    ]
    
    print("🔍 System Evaluation Report")
    print("=" * 50)
    
    total_score = 0
    total_time = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test['query']}")
        print(f"   Category: {test['category']}")
        print("-" * 40)
        
        start_time = time.time()
        try:
            response = run_imarika_agent(test['query'])
            response_time = time.time() - start_time
            
            # Calculate keyword score
            keywords_found = 0
            for keyword in test['expected_keywords']:
                if keyword.lower() in response.lower():
                    keywords_found += 1
            
            score = keywords_found / len(test['expected_keywords'])
            total_score += score
            total_time += response_time
            
            print(f"   ✅ Response: {response[:100]}...")
            print(f"   ⏱️  Time: {response_time:.2f}s")
            print(f"   📊 Keywords Found: {keywords_found}/{len(test['expected_keywords'])}")
            print(f"   🎯 Score: {score:.2f} ({score*100:.0f}%)")
            
            # Check for enhanced features
            enhanced_indicators = ["Enhanced" in response, len(response) > 100, "Imarika" in response]
            enhancement_score = sum(enhanced_indicators) / len(enhanced_indicators)
            print(f"   🧠 Enhancement Score: {enhancement_score:.2f}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            total_time += 30  # Penalty for errors
    
    # Summary
    avg_score = total_score / len(test_cases)
    avg_time = total_time / len(test_cases)
    
    print("\n" + "=" * 50)
    print("📊 EVALUATION SUMMARY")
    print("=" * 50)
    print(f"Average Accuracy Score: {avg_score:.2f} ({avg_score*100:.0f}%)")
    print(f"Average Response Time:  {avg_time:.2f}s")
    print(f"Total Test Cases:       {len(test_cases)}")
    
    # Performance rating
    if avg_score >= 0.8:
        rating = "🌟 Excellent"
    elif avg_score >= 0.6:
        rating = "✅ Good" 
    elif avg_score >= 0.4:
        rating = "⚠️  Fair"
    else:
        rating = "❌ Needs Improvement"
    
    print(f"Overall Rating:         {rating}")
    
    return {
        "avg_score": avg_score,
        "avg_time": avg_time,
        "rating": rating
    }

if __name__ == "__main__":
    evaluate_responses()