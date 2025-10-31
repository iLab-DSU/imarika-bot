#!/usr/bin/env python3
"""
Main training orchestration script for Imarika fine-tuning
"""

import argparse
import sys
import os
import torch
from pathlib import Path

def check_requirements():
    """Check system requirements for training"""
    print("🔍 Checking system requirements...")
    
    # Check GPU
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"✅ GPU: {gpu_name} ({gpu_memory:.1f}GB)")
        
        if gpu_memory < 8:
            print("⚠️  Warning: GPU has <8GB memory. Training may be slow.")
    else:
        print("❌ No GPU detected. Fine-tuning requires CUDA GPU.")
        return False
    
    # Check dependencies
    try:
        import transformers, peft, datasets
        print("✅ Required packages installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Install with: pip install transformers peft datasets torch")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Imarika Fine-tuning Pipeline")
    parser.add_argument("--stage", choices=["generate", "train", "evaluate", "convert", "all"], 
                       default="all", help="Training stage to run")
    parser.add_argument("--samples", type=int, default=1000, 
                       help="Number of samples to generate")
    parser.add_argument("--check-gpu", action="store_true", 
                       help="Check GPU availability and exit")
    
    args = parser.parse_args()
    
    if args.check_gpu:
        check_requirements()
        return
    
    print("🌾 Imarika QLoRA Fine-tuning Pipeline")
    print("=" * 50)
    
    if args.stage in ["generate", "all"]:
        print("\n📊 Stage 1: Dataset Generation")
        from dataset_generator import AgriDatasetGenerator
        generator = AgriDatasetGenerator()
        dataset = generator.generate_instruction_pairs(num_samples=args.samples)
        generator.save_dataset(dataset)
        print(f"✅ Generated {args.samples} training samples")
    
    if args.stage in ["train", "all"]:
        print("\n🧠 Stage 2: QLoRA Training")
        if not check_requirements():
            print("❌ Requirements not met. Skipping training.")
        else:
            try:
                from qlora_trainer import QLoRATrainer
                trainer = QLoRATrainer()
                model_path = trainer.train("agri_dataset.jsonl")
                print(f"✅ Model saved to: {model_path}")
            except Exception as e:
                print(f"❌ Training failed: {e}")
                return
    
    if args.stage in ["convert", "all"]:
        print("\n🔄 Stage 3: Ollama Conversion")
        try:
            from finetuned_model import convert_to_ollama
            model_name = convert_to_ollama("models/imarika-llama3-qlora")
            if model_name:
                print(f"✅ Ollama model '{model_name}' ready for use")
        except Exception as e:
            print(f"❌ Conversion failed: {e}")
    
    if args.stage in ["evaluate", "all"]:
        print("\n📈 Stage 4: Model Evaluation")
        try:
            from performance_comparison import PerformanceComparator
            comparator = PerformanceComparator()
            results = comparator.run_comparison()
            print("✅ Evaluation completed")
        except Exception as e:
            print(f"❌ Evaluation failed: {e}")
    
    print("\n🎉 Fine-tuning pipeline completed!")
    print("\n💡 Usage:")
    print("  - Test model: python finetuned_model.py")
    print("  - Use in system: Update ollama_integration.py to use 'imarika-agri' model")

if __name__ == "__main__":
    main()