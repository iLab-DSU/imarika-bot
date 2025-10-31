import subprocess
from pathlib import Path

class OllamaFineTuned:
    def __init__(self, model_name: str = "imarika-agri"):
        self.model_name = model_name
        self.fallback_model = "llama3"
        self.use_finetuned = self._check_finetuned_model()
        
    def _check_finetuned_model(self) -> bool:
        """Check if fine-tuned model exists"""
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
        
        # Build prompt with context
        if context:
            full_prompt = f"Context: {context}\n\nUser: {query}"
        else:
            full_prompt = query
        
        # Try fine-tuned model first
        if self.use_finetuned:
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
        
        # Fallback to base model with system prompt
        system_prompt = f"You are Imarika, agricultural expert for East African crops: beans, cassava, finger millet, maize, sorghum, sweet potatoes.\n\n{full_prompt}"
        
        try:
            result = subprocess.run(
                ["ollama", "run", self.fallback_model, system_prompt],
                capture_output=True,
                text=True,
                timeout=8
            )
            
            if result.returncode == 0 and result.stdout.strip():
                return f"🌾 {result.stdout.strip()}"
        except:
            pass
        
        # Final fallback
        return self._fallback_response(query)
    
    def _fallback_response(self, query: str) -> str:
        """Provide comprehensive fallback response when Ollama fails"""
        
        # Enhanced responses with more agricultural detail
        crop_info = {
            "maize": {
                "nutrients": "Maize needs Nitrogen (120-150kg/ha), Phosphorus (60-80kg/ha), Potassium (40-60kg/ha), and organic manure for optimal growth.",
                "pests": "Common maize pests include stem borers, armyworms, and weevils. Use integrated pest management with crop rotation and organic pesticides.",
                "weather": "Maize grows best in temperatures 20-30°C with 500-800mm annual rainfall distributed throughout the growing season.",
                "planting": "Plant maize at the start of rainy season, spacing 75cm between rows and 25cm between plants.",
                "harvest": "Harvest maize when kernels are hard and moisture content is below 20%, typically 4-6 months after planting."
            },
            "beans": {
                "nutrients": "Beans fix nitrogen naturally but need Phosphorus (40-60kg/ha), Potassium (30-40kg/ha), and organic compost.",
                "pests": "Manage bean pests like weevils, aphids, and bean flies using crop rotation, neem oil, and resistant varieties.",
                "weather": "Beans prefer moderate temperatures 18-24°C with well-distributed rainfall of 300-400mm during growing season.",
                "planting": "Plant beans 2-3cm deep with 30cm spacing between rows and 10cm between plants.",
                "harvest": "Harvest beans when pods are dry and rattle, typically 2-3 months after planting."
            },
            "cassava": {
                "nutrients": "Cassava needs minimal fertilizer but benefits from NPK (15:15:15) and organic manure for better yields.",
                "pests": "Control cassava pests like mealybugs, green mites, and cassava mosaic virus through clean planting material.",
                "weather": "Cassava thrives in tropical conditions with 1000-1500mm annual rainfall and temperatures 25-35°C.",
                "planting": "Plant cassava stems 15-20cm long at 45-degree angle with 1m spacing between plants.",
                "harvest": "Harvest cassava tubers 8-12 months after planting when leaves start yellowing."
            }
        }
        
        # Detect query type and crop
        query_lower = query.lower()
        
        # Find relevant crop
        detected_crop = None
        for crop in crop_info.keys():
            if crop in query_lower or crop.replace(" ", "") in query_lower:
                detected_crop = crop
                break
        
        if detected_crop:
            # Detect query type
            if any(word in query_lower for word in ["nutrient", "fertilizer", "manure", "npk"]):
                return f"🌾 {crop_info[detected_crop]['nutrients']}"
            elif any(word in query_lower for word in ["pest", "insect", "disease", "control"]):
                return f"🌾 {crop_info[detected_crop]['pests']}"
            elif any(word in query_lower for word in ["weather", "climate", "rain", "temperature"]):
                return f"🌾 {crop_info[detected_crop]['weather']}"
            elif any(word in query_lower for word in ["plant", "sow", "seed"]):
                return f"🌾 {crop_info[detected_crop]['planting']}"
            elif any(word in query_lower for word in ["harvest", "mature", "ready"]):
                return f"🌾 {crop_info[detected_crop]['harvest']}"
            else:
                # General crop info
                return f"🌾 {crop_info[detected_crop]['nutrients']}"
        
        return "🌾 I specialize in beans, cassava, finger millet, maize, sorghum, and sweet potatoes. Ask about nutrients, pests, weather, planting, or harvesting for these crops."

def create_enhanced_synthesizer():
    """Create synthesizer that uses fine-tuned context"""
    fine_tuned_model = OllamaFineTuned()
    
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
        
        # Generate response with enhanced context
        response = fine_tuned_model.generate_response(query, context)
        
        return {"response": response}
    
    return synthesizer_agent

if __name__ == "__main__":
    # Test the enhanced model
    model = OllamaFineTuned()
    
    print(f"🔍 Fine-tuned model '{model.model_name}' available: {model.use_finetuned}")
    
    test_queries = [
        "What nutrients does maize need?",
        "How do I manage pests in beans?",
        "What weather is good for cassava?"
    ]
    
    print("🧠 Testing Enhanced Ollama with Fine-tuned Model:")
    for query in test_queries:
        print(f"\nQuery: {query}")
        response = model.generate_response(query)
        print(f"Response: {response}")