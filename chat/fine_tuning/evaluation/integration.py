import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import ollama

class FineTunedImarika:
    def __init__(self, adapter_path: str = "fine_tuning/imarika-llama3"):
        self.adapter_path = adapter_path
        self.use_fine_tuned = self._check_adapter_exists()
        
    def _check_adapter_exists(self) -> bool:
        """Check if fine-tuned adapter exists"""
        from pathlib import Path
        return Path(self.adapter_path).exists()
    
    def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate response using fine-tuned model or fallback to Ollama"""
        
        if self.use_fine_tuned:
            return self._generate_with_adapter(prompt, context)
        else:
            # Fallback to existing Ollama setup
            return self._generate_with_ollama(prompt, context)
    
    def _generate_with_adapter(self, prompt: str, context: str) -> str:
        """Generate using fine-tuned LoRA adapter"""
        try:
            # Load model with adapter
            base_model = AutoModelForCausalLM.from_pretrained(
                "meta-llama/Llama-2-7b-chat-hf",
                torch_dtype=torch.float16,
                device_map="auto"
            )
            model = PeftModel.from_pretrained(base_model, self.adapter_path)
            tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
            
            # Format prompt
            full_prompt = f"Context: {context}\n\nQuestion: {prompt}\n\nAnswer:"
            inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=256,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response[len(full_prompt):].strip()
            
        except Exception as e:
            print(f"Fine-tuned model error: {e}")
            return self._generate_with_ollama(prompt, context)
    
    def _generate_with_ollama(self, prompt: str, context: str) -> str:
        """Fallback to existing Ollama implementation"""
        system_prompt = """You are Imarika, an agricultural expert for East African crops: 
        beans, cassava, finger millet, maize, sorghum, and sweet potatoes."""
        
        full_prompt = f"{system_prompt}\n\nContext: {context}\n\nQuestion: {prompt}"
        
        response = ollama.generate(
            model="llama3",
            prompt=full_prompt,
            options={"temperature": 0.7}
        )
        
        return response['response']

# Integration with existing LangGraph system
def create_enhanced_synthesizer():
    """Create synthesizer that uses fine-tuned model"""
    fine_tuned_model = FineTunedImarika()
    
    def synthesizer_agent(state):
        query = state.get("query", "")
        weather_data = state.get("weather_data", {})
        kg_data = state.get("kg_data", {})
        
        # Prepare context from tools
        context_parts = []
        if weather_data:
            context_parts.append(f"Weather: {weather_data}")
        if kg_data:
            context_parts.append(f"Knowledge: {kg_data}")
        
        context = " | ".join(context_parts)
        
        # Generate response with fine-tuned model
        response = fine_tuned_model.generate_response(query, context)
        
        return {"response": response}
    
    return synthesizer_agent