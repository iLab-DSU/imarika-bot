import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import subprocess
import os
from pathlib import Path

class FineTunedImarika:
    def __init__(self, model_path: str = "models/imarika-llama3-qlora"):
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_model(self):
        """Load the fine-tuned QLoRA model"""
        if not Path(self.model_path).exists():
            raise FileNotFoundError(f"Model not found at {self.model_path}. Run training first.")
        
        print(f"🔄 Loading fine-tuned model from {self.model_path}")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        
        # Load base model and adapter
        base_model = AutoModelForCausalLM.from_pretrained(
            "unsloth/llama-3-8b-bnb-4bit",
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        # Load LoRA adapter
        self.model = PeftModel.from_pretrained(base_model, self.model_path)
        self.model.eval()
        
        print("✅ Fine-tuned model loaded successfully")
    
    def generate_response(self, query: str, context: str = "") -> str:
        """Generate response using fine-tuned model"""
        if self.model is None:
            self.load_model()
        
        # Format prompt
        system_msg = "You are Imarika, an agricultural expert for East African crops: beans, cassava, finger millet, maize, sorghum, and sweet potatoes."
        
        if context:
            prompt = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n{system_msg}\n\nContext: {context}<|eot_id|><|start_header_id|>user<|end_header_id|>\n{query}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
        else:
            prompt = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n{system_msg}<|eot_id|><|start_header_id|>user<|end_header_id|>\n{query}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
        
        # Tokenize
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=256,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode response
        response = self.tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
        return response.strip()

def convert_to_ollama(model_path: str, ollama_model_name: str = "imarika-agri"):
    """Convert fine-tuned model to Ollama format"""
    print(f"🔄 Converting model to Ollama format: {ollama_model_name}")
    
    try:
        # Create Ollama model
        result = subprocess.run([
            "ollama", "create", ollama_model_name, 
            "-f", f"{model_path}/Modelfile"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Ollama model '{ollama_model_name}' created successfully")
            return ollama_model_name
        else:
            print(f"❌ Failed to create Ollama model: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ Error converting to Ollama: {e}")
        return None

if __name__ == "__main__":
    # Test fine-tuned model
    model = FineTunedImarika()
    
    test_queries = [
        "What nutrients does maize need?",
        "How do I manage pests in beans?",
        "What weather is good for cassava?"
    ]
    
    print("🧠 Testing Fine-Tuned Imarika Model:")
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            response = model.generate_response(query)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")