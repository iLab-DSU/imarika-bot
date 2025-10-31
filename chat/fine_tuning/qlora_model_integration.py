#!/usr/bin/env python3
"""
QLoRA Fine-tuned Model Integration for Imarika
Integrates the imarika_csv_qlora_model.zip into the system
"""

import os
import zipfile
import torch
import json
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
import subprocess
import time

class QLoRAImarika:
    def __init__(self, model_zip_path="imarika_csv_qlora_model.zip"):
        self.model_path = None
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.force_cpu = False
        
        # Extract and load model
        if os.path.exists(model_zip_path):
            self.extract_model(model_zip_path)
            self.load_model()
        else:
            print(f"Model zip not found: {model_zip_path}")
    
    def extract_model(self, zip_path):
        """Extract the model from zip file"""
        extract_dir = "fine_tuning/qlora_model"
        os.makedirs(extract_dir, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        self.model_path = extract_dir
        print(f"✅ Model extracted to: {extract_dir}")
    
    def load_model(self):
        """Load the fine-tuned model - try GPU first, fallback to CPU if needed"""
        # Try GPU first if available
        if torch.cuda.is_available() and not self.force_cpu:
            try:
                print(f"🚀 Attempting to load QLoRA model on GPU...")
                self._load_gpu_model()
                if self.model is not None:
                    print("✅ QLoRA model loaded successfully on GPU")
                    return
            except Exception as e:
                print(f"⚠️  GPU loading failed: {str(e)[:100]}...")
                print("   Trying CPU fallback...")
        
        # Try CPU fallback
        try:
            print(f"🔄 Attempting CPU inference (slower)...")
            self._load_cpu_model()
            if self.model is not None:
                print("✅ QLoRA model loaded on CPU (expect slower inference)")
                return
        except Exception as e:
            print(f"⚠️  CPU loading failed: {str(e)[:100]}...")
        
        print("❌ QLoRA model unavailable - will use Ollama fallback")
        self.model = None
    
    def _load_gpu_model(self):
        """Load model with GPU optimizations"""
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        
        base_model = "unsloth/Llama-3.2-3B-Instruct"
        
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        base_model_obj = AutoModelForCausalLM.from_pretrained(
            base_model,
            quantization_config=bnb_config,
            device_map="auto",
            torch_dtype=torch.bfloat16
        )
        
        self.model = PeftModel.from_pretrained(base_model_obj, self.model_path)
        self.model.eval()
        self.device = "cuda"
    
    def _load_cpu_model(self):
        """Load model for CPU inference"""
        base_model = "unsloth/Llama-3.2-3B-Instruct"
        
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Load without quantization for CPU
        base_model_obj = AutoModelForCausalLM.from_pretrained(
            base_model,
            torch_dtype=torch.float32,  # Use float32 for CPU
            device_map="cpu"
        )
        
        self.model = PeftModel.from_pretrained(base_model_obj, self.model_path)
        self.model.eval()
        self.device = "cpu"
    
    def generate_response(self, query, context="", max_length=256):
        """Generate response using fine-tuned model"""
        if not self.model or not self.tokenizer:
            return "Model not loaded"
        
        # Shorter prompt for better performance
        if context:
            full_prompt = f"Agricultural assistant for East African crops.\nContext: {context}\nQ: {query}\nA:"
        else:
            full_prompt = f"Agricultural assistant for East African crops.\nQ: {query}\nA:"
        
        try:
            # Tokenize with shorter length
            inputs = self.tokenizer(
                full_prompt,
                return_tensors="pt",
                truncation=True,
                max_length=512
            )
            
            # Move to device
            if self.device == "cuda":
                inputs = inputs.to(self.device)
            
            # Generate with optimized settings
            with torch.no_grad():
                # Reduce parameters for faster inference
                gen_kwargs = {
                    "max_new_tokens": max_length,
                    "temperature": 0.7,
                    "do_sample": True,
                    "pad_token_id": self.tokenizer.eos_token_id,
                    "eos_token_id": self.tokenizer.eos_token_id,
                    "repetition_penalty": 1.1
                }
                
                # CPU-specific optimizations
                if self.device == "cpu":
                    gen_kwargs.update({
                        "max_new_tokens": 128,  # Shorter for CPU
                        "num_beams": 1,  # No beam search
                        "do_sample": False  # Greedy decoding
                    })
                
                outputs = self.model.generate(**inputs, **gen_kwargs)
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract answer
            if "A:" in response:
                response = response.split("A:")[-1].strip()
            
            return response[:500]  # Limit response length
            
        except Exception as e:
            return f"Generation error: {str(e)[:100]}..."
    
    def is_available(self):
        """Check if model is loaded and ready"""
        return self.model is not None and self.tokenizer is not None

# Fallback to Ollama if QLoRA not available
class OllamaFallback:
    def generate_response(self, query, context=""):
        try:
            prompt = f"Agricultural assistant for East African crops.\nContext: {context}\nQ: {query}\nA:"
            
            result = subprocess.run(
                ["ollama", "run", "llama3", prompt],
                capture_output=True,
                text=True,
                timeout=15
            )
            return result.stdout.strip()
        except:
            return "Ollama unavailable"
    
    def is_available(self):
        return True

# Main integration class
class IntegratedImarika:
    def __init__(self):
        # Try to load QLoRA model first
        self.qlora_model = QLoRAImarika()
        self.ollama_model = OllamaFallback()
        
        # Determine which model to use
        self.use_qlora = self.qlora_model.is_available()
        
        print(f"🌾 Imarika Integration Status:")
        print(f"   QLoRA Model: {'✅ Available' if self.use_qlora else '❌ Not Available'}")
        print(f"   Ollama Fallback: ✅ Available")
        device_info = f" ({self.qlora_model.device})" if self.use_qlora else ""
        print(f"   Active Model: {'QLoRA Fine-tuned' + device_info if self.use_qlora else 'Ollama Base'}")
    
    def generate_response(self, query, context=""):
        """Generate response using best available model"""
        if self.use_qlora:
            try:
                response = self.qlora_model.generate_response(query, context)
                # If QLoRA fails, fallback to Ollama
                if "Generation error" in response or len(response.strip()) < 10:
                    print("⚠️  QLoRA generation failed, using Ollama fallback")
                    return self.ollama_model.generate_response(query, context)
                return response
            except Exception as e:
                print(f"⚠️  QLoRA error: {e}, using Ollama fallback")
                return self.ollama_model.generate_response(query, context)
        else:
            return self.ollama_model.generate_response(query, context)
    
    def get_model_info(self):
        """Get information about active model"""
        return {
            "model_type": "QLoRA Fine-tuned" if self.use_qlora else "Ollama Base",
            "qlora_available": self.use_qlora,
            "device": self.qlora_model.device if self.use_qlora else "CPU"
        }

if __name__ == "__main__":
    # Test the integration
    print("🧪 Testing QLoRA Integration...")
    
    imarika = IntegratedImarika()
    
    # Test queries
    test_queries = [
        "What nutrients does maize need?",
        "How to control pests in beans?",
        "Best planting time for cassava?",
        "Sorghum drought resistance tips"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        print("=" * 50)
        
        start_time = time.time()
        response = imarika.generate_response(query)
        end_time = time.time()
        
        print(f"Response: {response}")
        print(f"Time: {end_time - start_time:.2f}s")
        print(f"Model: {imarika.get_model_info()['model_type']}")