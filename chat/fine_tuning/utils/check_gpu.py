#!/usr/bin/env python3

import torch

def check_gpu():
    print("🔍 GPU Check for QLoRA Fine-tuning")
    print("=" * 40)
    
    if torch.cuda.is_available():
        print("✅ CUDA is available")
        print(f"📊 GPU Count: {torch.cuda.device_count()}")
        
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            memory_gb = props.total_memory / 1e9
            print(f"🎯 GPU {i}: {props.name}")
            print(f"💾 Memory: {memory_gb:.1f}GB")
            
            if memory_gb >= 8:
                print("✅ Sufficient memory for QLoRA training")
            else:
                print("⚠️  May need memory optimization")
    else:
        print("❌ CUDA not available")
        print("QLoRA fine-tuning requires a CUDA GPU")
        return False
    
    return True

if __name__ == "__main__":
    check_gpu()