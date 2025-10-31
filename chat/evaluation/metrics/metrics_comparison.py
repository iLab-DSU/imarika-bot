#!/usr/bin/env python3

import re
import json
from pathlib import Path

class AgriMetrics:
    def __init__(self):
        self.agricultural_keywords = {
            "nutrients": ["nitrogen", "phosphorus", "potassium", "NPK", "manure", "compost", "fertilizer"],
            "pests": ["weevil", "borer", "aphids", "pesticide", "insecticide", "organic", "rotation"],
            "weather": ["temperature", "humidity", "rainfall", "drought", "season", "climate"],
            "practices": ["planting", "harvesting", "irrigation", "cultivation", "spacing", "timing"],
            "crops": ["maize", "beans", "cassava", "sorghum", "millet", "sweet potatoes"]
        }
        
        self.test_queries = [
            "What nutrients does maize need?",
            "How do I manage bean pests?", 
            "What weather is good for cassava?",
            "When should I plant sorghum?",
            "How to harvest sweet potatoes?"
        ]
    
    def calculate_keyword_density(self, response: str) -> float:
        """Calculate agricultural keyword density in response"""
        if not response:
            return 0.0
        
        words = response.lower().split()
        total_keywords = sum(len(keywords) for keywords in self.agricultural_keywords.values())
        found_keywords = 0
        
        for category, keywords in self.agricultural_keywords.items():
            for keyword in keywords:
                if keyword in response.lower():
                    found_keywords += 1
        
        return found_keywords / total_keywords if total_keywords > 0 else 0.0
    
    def calculate_specificity_score(self, response: str, query: str) -> float:
        """Calculate how specific the response is to the query"""
        query_words = set(query.lower().split())
        response_words = set(response.lower().split())
        
        # Remove common words
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        query_words -= common_words
        response_words -= common_words
        
        if not query_words:
            return 0.0
        
        overlap = len(query_words.intersection(response_words))
        return overlap / len(query_words)
    
    def calculate_completeness_score(self, response: str) -> float:
        """Calculate response completeness based on length and structure"""
        if not response:
            return 0.0
        
        # Basic completeness indicators
        has_greeting = any(word in response.lower() for word in ["habari", "hello", "hi"])
        has_explanation = len(response.split()) > 20
        has_specific_advice = any(word in response.lower() for word in ["apply", "use", "during", "stage"])
        has_context = any(word in response.lower() for word in ["east africa", "climate", "soil"])
        
        indicators = [has_greeting, has_explanation, has_specific_advice, has_context]
        return sum(indicators) / len(indicators)
    
    def calculate_accuracy_score(self, response: str, query: str) -> float:
        """Calculate accuracy based on expected content for query type"""
        query_lower = query.lower()
        response_lower = response.lower()
        
        # Define expected content for different query types
        if "nutrient" in query_lower or "fertilizer" in query_lower:
            expected = ["nitrogen", "phosphorus", "potassium", "npk", "manure"]
        elif "pest" in query_lower or "disease" in query_lower:
            expected = ["pesticide", "organic", "rotation", "spray", "control"]
        elif "weather" in query_lower or "climate" in query_lower:
            expected = ["temperature", "humidity", "rainfall", "season", "climate"]
        elif "plant" in query_lower or "grow" in query_lower:
            expected = ["season", "spacing", "depth", "timing", "preparation"]
        elif "harvest" in query_lower:
            expected = ["maturity", "months", "storage", "timing", "signs"]
        else:
            expected = []
        
        if not expected:
            return 0.5  # Neutral score for unclear queries
        
        found = sum(1 for word in expected if word in response_lower)
        return found / len(expected)
    
    def calculate_composite_score(self, response: str, query: str) -> dict:
        """Calculate all metrics and return composite score"""
        
        metrics = {
            "keyword_density": self.calculate_keyword_density(response),
            "specificity": self.calculate_specificity_score(response, query),
            "completeness": self.calculate_completeness_score(response),
            "accuracy": self.calculate_accuracy_score(response, query)
        }
        
        # Weighted composite score
        weights = {
            "keyword_density": 0.25,
            "specificity": 0.25, 
            "completeness": 0.25,
            "accuracy": 0.25
        }
        
        composite = sum(metrics[metric] * weights[metric] for metric in metrics)
        metrics["composite_score"] = composite
        
        return metrics

def compare_systems():
    """Compare base vs enhanced system using metrics"""
    
    metrics = AgriMetrics()
    
    # Sample responses for comparison
    test_cases = [
        {
            "query": "What nutrients does maize need?",
            "base_response": "Maize needs nitrogen, phosphorus, and potassium.",
            "enhanced_response": "Maize needs Nitrogen, Phosphorus, Potassium, Manure, and Compost. For optimal growth in East African conditions, apply NPK fertilizer during planting at 2-3 inches depth. Top-dress with nitrogen during the vegetative stage around 4-6 weeks after planting. Consider DAP for phosphorus-deficient soils common in the region."
        },
        {
            "query": "How do I manage bean pests?",
            "base_response": "Use pesticides to control bean pests.",
            "enhanced_response": "To manage pests in beans: use organic pesticides and crop rotation. Apply neem oil or insecticidal soap during early morning or evening. Practice intercropping with pest-repellent crops like sweet potatoes. Monitor regularly for weevil damage and remove affected plants immediately. Maintain proper spacing for air circulation."
        }
    ]
    
    print("📊 AGRICULTURAL METRICS COMPARISON")
    print("=" * 60)
    
    total_base_score = 0
    total_enhanced_score = 0
    
    for i, case in enumerate(test_cases, 1):
        query = case["query"]
        base_response = case["base_response"]
        enhanced_response = case["enhanced_response"]
        
        print(f"\n{i}. Query: {query}")
        print("-" * 40)
        
        # Calculate metrics for base response
        base_metrics = metrics.calculate_composite_score(base_response, query)
        print(f"Base Response Metrics:")
        for metric, score in base_metrics.items():
            print(f"   {metric.replace('_', ' ').title()}: {score:.3f}")
        
        # Calculate metrics for enhanced response  
        enhanced_metrics = metrics.calculate_composite_score(enhanced_response, query)
        print(f"\nEnhanced Response Metrics:")
        for metric, score in enhanced_metrics.items():
            print(f"   {metric.replace('_', ' ').title()}: {score:.3f}")
        
        # Show improvement
        improvement = enhanced_metrics["composite_score"] - base_metrics["composite_score"]
        print(f"\n📈 Improvement: {improvement:+.3f} ({improvement/base_metrics['composite_score']*100:+.1f}%)")
        
        total_base_score += base_metrics["composite_score"]
        total_enhanced_score += enhanced_metrics["composite_score"]
    
    # Overall comparison
    avg_base = total_base_score / len(test_cases)
    avg_enhanced = total_enhanced_score / len(test_cases)
    overall_improvement = avg_enhanced - avg_base
    
    print(f"\n" + "=" * 60)
    print("🎯 OVERALL PERFORMANCE COMPARISON")
    print("=" * 60)
    print(f"Base System Average Score:     {avg_base:.3f}")
    print(f"Enhanced System Average Score: {avg_enhanced:.3f}")
    print(f"Overall Improvement:           {overall_improvement:+.3f} ({overall_improvement/avg_base*100:+.1f}%)")
    
    # Performance rating
    if overall_improvement > 0.3:
        rating = "🌟 Excellent Improvement"
    elif overall_improvement > 0.2:
        rating = "✅ Good Improvement"
    elif overall_improvement > 0.1:
        rating = "⚠️ Moderate Improvement"
    else:
        rating = "❌ Minimal Improvement"
    
    print(f"Performance Rating:            {rating}")
    
    return {
        "base_avg": avg_base,
        "enhanced_avg": avg_enhanced,
        "improvement": overall_improvement,
        "improvement_percentage": (overall_improvement/avg_base*100)
    }

if __name__ == "__main__":
    results = compare_systems()
    
    print(f"\n💡 Key Metrics Used:")
    print(f"   • Keyword Density: Agricultural term coverage")
    print(f"   • Specificity: Query-response relevance")
    print(f"   • Completeness: Response depth and structure")
    print(f"   • Accuracy: Expected content presence")
    print(f"   • Composite Score: Weighted average of all metrics")