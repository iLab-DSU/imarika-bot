#!/usr/bin/env python3

import json
import time
import subprocess
from pathlib import Path

class PerformanceComparator:
    def __init__(self):
        self.test_queries = [
            "What nutrients does maize need?",
            "How do I manage pests in beans?", 
            "What weather is good for cassava?",
            "When should I plant sorghum?",
            "How to harvest sweet potatoes?"
        ]
        
        self.expected_keywords = {
            "What nutrients does maize need?": ["nitrogen", "phosphorus", "potassium", "NPK", "manure"],
            "How do I manage pests in beans?": ["pesticide", "rotation", "organic", "weevil", "spray"],
            "What weather is good for cassava?": ["humid", "warm", "rainfall", "drought", "temperature"],
            "When should I plant sorghum?": ["season", "rain", "dry", "planting", "timing"],
            "How to harvest sweet potatoes?": ["months", "maturity", "harvest", "storage", "tubers"]
        }
    
    def test_base_model(self, query: str) -> dict:
        """Test original Ollama without enhancement"""
        prompt = f"You are an agricultural assistant. Answer briefly: {query}"
        
        start_time = time.time()
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3", prompt],
                capture_output=True,
                text=True,
                timeout=20
            )
            response_time = time.time() - start_time
            
            if result.returncode == 0:
                return {
                    "response": result.stdout.strip(),
                    "time": response_time,
                    "success": True
                }
            else:
                return {"response": "Error", "time": response_time, "success": False}
                
        except subprocess.TimeoutExpired:
            return {"response": "Timeout", "time": 20, "success": False}
        except Exception as e:
            return {"response": f"Error: {e}", "time": 0, "success": False}
    
    def test_enhanced_model(self, query: str) -> dict:
        """Test enhanced model with fine-tuned context"""
        try:
            from ollama_integration import OllamaFineTuned
            enhanced_model = OllamaFineTuned()
            
            start_time = time.time()
            response = enhanced_model.generate_response(query, "")
            response_time = time.time() - start_time
            
            return {
                "response": response,
                "time": response_time,
                "success": True
            }
        except Exception as e:
            return {"response": f"Error: {e}", "time": 0, "success": False}
    
    def calculate_keyword_score(self, response: str, expected_keywords: list) -> float:
        """Calculate how many expected keywords are in response"""
        if not expected_keywords:
            return 0.0
        
        found = 0
        for keyword in expected_keywords:
            if keyword.lower() in response.lower():
                found += 1
        
        return found / len(expected_keywords)
    
    def run_comparison(self) -> dict:
        """Run full performance comparison"""
        results = {
            "base_model": [],
            "enhanced_model": [],
            "summary": {}
        }
        
        print("🔍 Performance Comparison: Base vs Enhanced Model")
        print("=" * 60)
        
        for query in self.test_queries:
            print(f"\nTesting: {query}")
            print("-" * 40)
            
            # Test base model
            print("📊 Base Model...")
            base_result = self.test_base_model(query)
            base_score = self.calculate_keyword_score(
                base_result["response"], 
                self.expected_keywords.get(query, [])
            )
            base_result["keyword_score"] = base_score
            results["base_model"].append(base_result)
            
            print(f"   Response: {base_result['response'][:100]}...")
            print(f"   Time: {base_result['time']:.2f}s")
            print(f"   Keyword Score: {base_score:.2f}")
            
            # Test enhanced model
            print("🧠 Enhanced Model...")
            enhanced_result = self.test_enhanced_model(query)
            enhanced_score = self.calculate_keyword_score(
                enhanced_result["response"],
                self.expected_keywords.get(query, [])
            )
            enhanced_result["keyword_score"] = enhanced_score
            results["enhanced_model"].append(enhanced_result)
            
            print(f"   Response: {enhanced_result['response'][:100]}...")
            print(f"   Time: {enhanced_result['time']:.2f}s")
            print(f"   Keyword Score: {enhanced_score:.2f}")
            
            # Show improvement
            improvement = enhanced_score - base_score
            print(f"   📈 Improvement: {improvement:+.2f}")
        
        # Calculate summary statistics
        base_avg_score = sum(r["keyword_score"] for r in results["base_model"]) / len(results["base_model"])
        enhanced_avg_score = sum(r["keyword_score"] for r in results["enhanced_model"]) / len(results["enhanced_model"])
        
        base_avg_time = sum(r["time"] for r in results["base_model"] if r["success"]) / len([r for r in results["base_model"] if r["success"]])
        enhanced_avg_time = sum(r["time"] for r in results["enhanced_model"] if r["success"]) / len([r for r in results["enhanced_model"] if r["success"]])
        
        results["summary"] = {
            "base_avg_score": base_avg_score,
            "enhanced_avg_score": enhanced_avg_score,
            "score_improvement": enhanced_avg_score - base_avg_score,
            "base_avg_time": base_avg_time,
            "enhanced_avg_time": enhanced_avg_time,
            "time_difference": enhanced_avg_time - base_avg_time
        }
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 PERFORMANCE SUMMARY")
        print("=" * 60)
        print(f"Base Model Average Score:     {base_avg_score:.2f}")
        print(f"Enhanced Model Average Score: {enhanced_avg_score:.2f}")
        print(f"Score Improvement:           {results['summary']['score_improvement']:+.2f} ({results['summary']['score_improvement']/base_avg_score*100:+.1f}%)")
        print(f"Base Model Average Time:     {base_avg_time:.2f}s")
        print(f"Enhanced Model Average Time: {enhanced_avg_time:.2f}s")
        print(f"Time Difference:             {results['summary']['time_difference']:+.2f}s")
        
        # Save results
        with open("performance_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to performance_results.json")
        
        return results

if __name__ == "__main__":
    comparator = PerformanceComparator()
    comparator.run_comparison()