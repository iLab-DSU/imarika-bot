#!/usr/bin/env python3

import subprocess
import json

def simple_ollama_test():
    """Simple test using ollama directly"""
    
    queries = [
        "What nutrients does maize need for good growth?",
        "How to manage bean pests?",
        "Best weather for cassava?"
    ]
    
    print("🌾 Simple Ollama Test")
    print("=" * 30)
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. {query}")
        print("-" * 20)
        
        prompt = f"You are Imarika, agricultural expert for East African crops. Answer briefly: {query}"
        
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3", prompt],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"✅ {result.stdout.strip()}")
            else:
                print(f"❌ Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("⏰ Timeout - ollama taking too long")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    simple_ollama_test()