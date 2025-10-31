import subprocess
import os
from pathlib import Path

class QLoRAOllamaIntegration:
    def __init__(self, model_name: str = "imarika-agri"):
        self.model_name = model_name
        self.fallback_model = "llama3"
        
    def _check_model_exists(self) -> bool:
        """Check if fine-tuned model exists in Ollama"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return self.model_name in result.stdout
        except:
            return False
    
    def generate_response(self, query: str, context: str = "") -> str:
        """Generate response using fine-tuned model or fallback"""
        
        # Build prompt
        system_prompt = "You are Imarika, an agricultural expert for East African crops: beans, cassava, finger millet, maize, sorghum, and sweet potatoes."
        
        if context:
            full_prompt = f"{system_prompt}\n\nContext: {context}\n\nUser: {query}\nImarika:"
        else:
            full_prompt = f"{system_prompt}\n\nUser: {query}\nImarika:"
        
        # Try fine-tuned model first
        if self._check_model_exists():
            try:
                result = subprocess.run(
                    ["ollama", "run", self.model_name, full_prompt],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0 and result.stdout.strip():
                    return f"🌾 {result.stdout.strip()}"
            except:
                pass
        
        # Fallback to base model
        try:
            result = subprocess.run(
                ["ollama", "run", self.fallback_model, full_prompt],
                capture_output=True,
                text=True,
                timeout=8
            )
            
            if result.returncode == 0 and result.stdout.strip():
                return f"🌾 {result.stdout.strip()}"
        except:
            pass
        
        # Final fallback to hardcoded responses
        return self._fallback_response(query)
    
    def _fallback_response(self, query: str) -> str:
        """Provide fallback response when all models fail"""
        crop_info = {
            "maize": "Maize needs Nitrogen (120-150kg/ha), Phosphorus (60-80kg/ha), Potassium (40-60kg/ha), and organic manure for optimal growth.",
            "beans": "Beans fix nitrogen naturally but need Phosphorus (40-60kg/ha), Potassium (30-40kg/ha), and organic compost.",
            "cassava": "Cassava needs minimal fertilizer but benefits from NPK (15:15:15) and organic manure for better yields."
        }
        
        query_lower = query.lower()
        for crop, info in crop_info.items():
            if crop in query_lower:
                return f"🌾 {info}"
        
        return "🌾 I specialize in beans, cassava, finger millet, maize, sorghum, and sweet potatoes. Please ask about these crops."

def create_enhanced_synthesizer():
    """Create synthesizer that uses QLoRA fine-tuned model"""
    qlora_model = QLoRAOllamaIntegration()
    
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
        response = qlora_model.generate_response(query, context)
        
        return {"response": response}
    
    return synthesizer_agent

if __name__ == "__main__":
    # Test the QLoRA integration
    model = QLoRAOllamaIntegration()
    
    print(f"🔍 Checking for fine-tuned model '{model.model_name}'...")
    if model._check_model_exists():
        print("✅ Fine-tuned model found!")
    else:
        print("❌ Fine-tuned model not found. Using fallback.")
    
    test_queries = [
        "What nutrients does maize need?",
        "How do I manage pests in beans?",
        "What weather is good for cassava?"
    ]
    
    print("\n🧠 Testing QLoRA Model Integration:")
    for query in test_queries:
        print(f"\nQuery: {query}")
        response = model.generate_response(query)
        print(f"Response: {response}")