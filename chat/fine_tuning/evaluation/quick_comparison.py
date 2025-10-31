#!/usr/bin/env python3

import subprocess
import time

def quick_test():
    """Quick comparison test"""
    
    query = "What nutrients does maize need?"
    
    print("🔍 Quick Performance Test")
    print("=" * 40)
    print(f"Query: {query}\n")
    
    # Test 1: Base Ollama
    print("📊 Base Ollama Model:")
    print("-" * 20)
    
    base_prompt = f"You are an agricultural assistant. Answer briefly: {query}"
    
    start = time.time()
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", base_prompt],
            capture_output=True,
            text=True,
            timeout=15
        )
        base_time = time.time() - start
        
        if result.returncode == 0:
            base_response = result.stdout.strip()
            print(f"Response: {base_response}")
            print(f"Time: {base_time:.2f}s")
        else:
            print("❌ Error in base model")
            base_response = "Error"
            
    except subprocess.TimeoutExpired:
        print("⏰ Base model timeout")
        base_response = "Timeout"
        base_time = 15
    
    # Test 2: Enhanced Model
    print(f"\n🧠 Enhanced Model:")
    print("-" * 20)
    
    try:
        from ollama_integration import OllamaFineTuned
        enhanced_model = OllamaFineTuned()
        
        start = time.time()
        enhanced_response = enhanced_model.generate_response(query, "")
        enhanced_time = time.time() - start
        
        print(f"Response: {enhanced_response}")
        print(f"Time: {enhanced_time:.2f}s")
        
        # Simple comparison
        print(f"\n📈 Comparison:")
        print(f"Base length: {len(base_response)} chars")
        print(f"Enhanced length: {len(enhanced_response)} chars")
        print(f"Time difference: {enhanced_time - base_time:+.2f}s")
        
        # Check for agricultural keywords
        keywords = ["nitrogen", "phosphorus", "potassium", "NPK", "manure", "fertilizer"]
        base_keywords = sum(1 for k in keywords if k.lower() in base_response.lower())
        enhanced_keywords = sum(1 for k in keywords if k.lower() in enhanced_response.lower())
        
        print(f"Base keywords found: {base_keywords}/{len(keywords)}")
        print(f"Enhanced keywords found: {enhanced_keywords}/{len(keywords)}")
        print(f"Keyword improvement: {enhanced_keywords - base_keywords:+d}")
        
    except Exception as e:
        print(f"❌ Enhanced model error: {e}")

if __name__ == "__main__":
    quick_test()