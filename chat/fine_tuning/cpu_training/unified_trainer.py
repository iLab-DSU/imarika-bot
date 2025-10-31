#!/usr/bin/env python3
"""
Unified training script that tries QLoRA first, then falls back to CPU training
"""

import torch
import subprocess
from pathlib import Path

class UnifiedTrainer:
    def __init__(self):
        self.dataset_path = "agri_dataset.jsonl"
        self.model_name = "imarika-agri"
        
    def check_requirements(self):
        """Check system capabilities"""
        print("🔍 Checking system capabilities...")
        
        # Check dataset
        if not Path(self.dataset_path).exists():
            print("❌ Dataset not found. Generate first with: python train.py --stage generate")
            return False
        
        # Check GPU
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"✅ GPU: {gpu_name} ({gpu_memory:.1f}GB)")
            
            if gpu_memory >= 8:
                print("🎯 GPU suitable for QLoRA training")
                return "gpu"
            else:
                print("⚠️  GPU memory <8GB, using CPU method")
                return "cpu"
        else:
            print("💻 No GPU detected, using CPU method")
            return "cpu"
    
    def train_qlora(self):
        """Attempt QLoRA training"""
        print("\n🧠 Attempting QLoRA Training...")
        
        try:
            # Check dependencies
            import transformers, peft, datasets
            print("✅ QLoRA dependencies available")
            
            from qlora_trainer import QLoRATrainer
            trainer = QLoRATrainer()
            model_path = trainer.train(self.dataset_path)
            
            if model_path:
                print("✅ QLoRA training successful!")
                return model_path
            else:
                print("❌ QLoRA training failed")
                return None
                
        except ImportError as e:
            print(f"❌ Missing QLoRA dependencies: {e}")
            return None
        except Exception as e:
            print(f"❌ QLoRA training error: {e}")
            return None
    
    def train_cpu(self):
        """CPU-based training using Ollama"""
        print("\n💻 Starting CPU Training with Ollama...")
        
        try:
            from cpu_trainer import CPUTrainer
            trainer = CPUTrainer()
            
            if trainer.train_with_ollama():
                print("✅ CPU training successful!")
                return self.model_name
            else:
                print("❌ CPU training failed")
                return None
                
        except Exception as e:
            print(f"❌ CPU training error: {e}")
            return None
    
    def test_model(self, model_name):
        """Test the trained model"""
        print(f"\n🧪 Testing model: {model_name}")
        
        test_queries = [
            "What nutrients does maize need?",
            "How do I manage pests in beans?",
            "What weather is good for cassava?"
        ]
        
        for query in test_queries:
            print(f"\n📝 Query: {query}")
            try:
                result = subprocess.run([
                    "ollama", "run", model_name, query
                ], capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0:
                    response = result.stdout.strip()
                    print(f"🌾 Response: {response[:100]}...")
                else:
                    print(f"❌ Error: {result.stderr}")
            except Exception as e:
                print(f"❌ Test failed: {e}")
    
    def run_training(self):
        """Main training orchestration"""
        print("🌾 Unified Imarika Training Pipeline")
        print("=" * 50)
        
        # Check requirements
        capability = self.check_requirements()
        if not capability:
            return
        
        model_result = None
        
        # Try QLoRA first if GPU available
        if capability == "gpu":
            model_result = self.train_qlora()
        
        # Fallback to CPU training
        if not model_result:
            print("\n🔄 Falling back to CPU training...")
            model_result = self.train_cpu()
        
        # Test the model
        if model_result:
            print(f"\n🎉 Training completed successfully!")
            print(f"📁 Model: {model_result}")
            
            # Test if it's an Ollama model
            if isinstance(model_result, str) and not model_result.startswith("/"):
                self.test_model(model_result)
            
            print(f"\n💡 Usage:")
            print(f"  - Test: ollama run {self.model_name}")
            print(f"  - Integration: Model automatically used by system")
        else:
            print("\n❌ All training methods failed!")

if __name__ == "__main__":
    trainer = UnifiedTrainer()
    trainer.run_training()