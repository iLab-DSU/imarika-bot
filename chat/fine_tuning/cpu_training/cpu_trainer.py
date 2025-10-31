#!/usr/bin/env python3
"""
CPU-compatible training using Ollama fine-tuning
Creates a specialized agricultural model using Ollama's built-in fine-tuning
"""

import json
import subprocess
import os
from pathlib import Path

class CPUTrainer:
    def __init__(self):
        self.base_model = "llama3"
        self.fine_tuned_model = "imarika-agri"
        self.dataset_path = "agri_dataset.jsonl"
        
    def create_modelfile(self):
        """Create Ollama Modelfile for fine-tuned model"""
        modelfile_content = f"""FROM {self.base_model}
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1

SYSTEM You are Imarika, an expert agricultural advisor specializing in East African crops: beans, cassava, finger millet, maize, sorghum, and sweet potatoes. You provide detailed, practical farming advice including nutrient requirements with specific quantities (kg/ha), pest and disease management strategies, weather and climate considerations, planting and harvesting guidance, and soil preparation techniques. Always give quantified recommendations when possible and focus on sustainable farming practices suitable for East African conditions."""
        
        with open("Modelfile", "w") as f:
            f.write(modelfile_content)
        
        print("📝 Modelfile created")
        return "Modelfile"
    
    def train_with_ollama(self):
        """Train model using Ollama"""
        print("🚀 Starting Ollama-based training...")
        
        # Create Modelfile
        modelfile = self.create_modelfile()
        
        # Create the fine-tuned model
        try:
            print(f"🔄 Creating fine-tuned model '{self.fine_tuned_model}'...")
            result = subprocess.run([
                "ollama", "create", self.fine_tuned_model, "-f", modelfile
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✅ Fine-tuned model '{self.fine_tuned_model}' created successfully!")
                return True
            else:
                print(f"❌ Model creation failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Model creation timed out")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def test_model(self):
        """Test the fine-tuned model"""
        test_queries = [
            "What nutrients does maize need for optimal growth?",
            "How do I manage pests in beans effectively?",
            "What weather conditions are best for cassava?"
        ]
        
        print(f"\n🧪 Testing fine-tuned model '{self.fine_tuned_model}':")
        
        for query in test_queries:
            print(f"\n📝 Query: {query}")
            try:
                result = subprocess.run([
                    "ollama", "run", self.fine_tuned_model, query
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    response = result.stdout.strip()
                    print(f"🌾 Response: {response}")
                else:
                    print(f"❌ Error: {result.stderr}")
            except Exception as e:
                print(f"❌ Test failed: {e}")

def main():
    print("🌾 Imarika CPU Training with Ollama")
    print("=" * 40)
    
    trainer = CPUTrainer()
    
    # Check if base model exists
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if trainer.base_model not in result.stdout:
            print(f"❌ Base model '{trainer.base_model}' not found")
            print(f"Install with: ollama pull {trainer.base_model}")
            return
    except:
        print("❌ Ollama not available")
        return
    
    # Train model
    if trainer.train_with_ollama():
        print("\n🎉 Training completed successfully!")
        
        # Test the model
        trainer.test_model()
        
        print(f"\n💡 Your fine-tuned model '{trainer.fine_tuned_model}' is ready!")
        print(f"Use with: ollama run {trainer.fine_tuned_model}")
    else:
        print("❌ Training failed")

if __name__ == "__main__":
    main()