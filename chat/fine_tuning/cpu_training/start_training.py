#!/usr/bin/env python3
"""
Quick start script for QLoRA fine-tuning
"""

import torch
import subprocess
import sys

def check_gpu():
    """Check GPU availability"""
    if not torch.cuda.is_available():
        print("❌ No CUDA GPU detected!")
        print("QLoRA fine-tuning requires a GPU with at least 8GB VRAM")
        return False
    
    gpu_name = torch.cuda.get_device_name(0)
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
    
    print(f"✅ GPU: {gpu_name}")
    print(f"📊 Memory: {gpu_memory:.1f}GB")
    
    if gpu_memory < 8:
        print("⚠️  Warning: Less than 8GB VRAM. Training may fail.")
        response = input("Continue anyway? (y/N): ")
        return response.lower() == 'y'
    
    return True

def install_dependencies():
    """Install required packages"""
    packages = [
        "torch",
        "transformers>=4.36.0", 
        "peft>=0.7.0",
        "datasets>=2.14.0",
        "accelerate>=0.24.0",
        "bitsandbytes>=0.41.0"
    ]
    
    print("📦 Installing dependencies...")
    for package in packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✅ {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    return True

def main():
    print("🌾 Imarika QLoRA Fine-Tuning Setup")
    print("=" * 40)
    
    # Check GPU
    if not check_gpu():
        return
    
    # Install dependencies
    print("\n📦 Checking dependencies...")
    try:
        import transformers, peft, datasets, accelerate, bitsandbytes
        print("✅ All dependencies installed")
    except ImportError:
        if not install_dependencies():
            print("❌ Failed to install dependencies")
            return
    
    # Generate dataset
    print("\n📊 Generating training dataset...")
    try:
        from dataset_generator import AgriDatasetGenerator
        generator = AgriDatasetGenerator()
        generator.generate_dataset(num_samples=1000)
        print("✅ Dataset generated")
    except Exception as e:
        print(f"❌ Dataset generation failed: {e}")
        return
    
    # Start training
    print("\n🚀 Starting QLoRA training...")
    print("This will take 2-4 hours depending on your GPU...")
    
    try:
        from qlora_trainer import QLoRATrainer
        trainer = QLoRATrainer()
        model_path = trainer.train("agri_dataset.jsonl")
        
        print(f"\n✅ Training completed!")
        print(f"📁 Model saved to: {model_path}")
        
        # Convert to Ollama
        print("\n🔄 Converting to Ollama...")
        from finetuned_model import convert_to_ollama
        ollama_name = convert_to_ollama(model_path)
        
        if ollama_name:
            print(f"✅ Ollama model '{ollama_name}' ready!")
            print("\n💡 Test with: ollama run imarika-agri")
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("- Ensure GPU has enough memory")
        print("- Try reducing batch size in qlora_trainer.py")
        print("- Check CUDA installation")

if __name__ == "__main__":
    main()