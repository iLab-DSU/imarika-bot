import json
import re
from typing import List, Dict
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

class AgriEvaluator:
    def __init__(self, base_model_path: str, adapter_path: str = None):
        self.base_model_path = base_model_path
        self.adapter_path = adapter_path
        self.load_models()
        
    def load_models(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.base_model_path)
        self.base_model = AutoModelForCausalLM.from_pretrained(
            self.base_model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        if self.adapter_path:
            self.fine_tuned_model = PeftModel.from_pretrained(
                self.base_model, 
                self.adapter_path
            )
        
    def generate_response(self, prompt: str, use_fine_tuned: bool = True) -> str:
        model = self.fine_tuned_model if use_fine_tuned and self.adapter_path else self.base_model
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=256,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response[len(prompt):].strip()
    
    def keyword_evaluation(self, response: str, expected_keywords: List[str]) -> float:
        """Check if response contains expected agricultural keywords"""
        found_keywords = 0
        for keyword in expected_keywords:
            if re.search(keyword.lower(), response.lower()):
                found_keywords += 1
        return found_keywords / len(expected_keywords) if expected_keywords else 0
    
    def crop_accuracy_test(self) -> Dict:
        """Test crop-specific knowledge accuracy"""
        test_cases = [
            {
                "prompt": "What nutrients does maize need?",
                "keywords": ["nitrogen", "phosphorus", "potassium", "NPK"]
            },
            {
                "prompt": "How do I manage pests in beans?",
                "keywords": ["pesticide", "rotation", "organic", "weevil"]
            },
            {
                "prompt": "What weather is good for cassava?",
                "keywords": ["humid", "warm", "rainfall", "drought"]
            }
        ]
        
        results = {"base_model": [], "fine_tuned": []}
        
        for test in test_cases:
            # Test base model
            base_response = self.generate_response(test["prompt"], use_fine_tuned=False)
            base_score = self.keyword_evaluation(base_response, test["keywords"])
            results["base_model"].append(base_score)
            
            # Test fine-tuned model
            if self.adapter_path:
                ft_response = self.generate_response(test["prompt"], use_fine_tuned=True)
                ft_score = self.keyword_evaluation(ft_response, test["keywords"])
                results["fine_tuned"].append(ft_score)
        
        return {
            "base_avg": sum(results["base_model"]) / len(results["base_model"]),
            "fine_tuned_avg": sum(results["fine_tuned"]) / len(results["fine_tuned"]) if results["fine_tuned"] else 0,
            "improvement": (sum(results["fine_tuned"]) / len(results["fine_tuned"]) - sum(results["base_model"]) / len(results["base_model"])) if results["fine_tuned"] else 0
        }
    
    def run_evaluation(self) -> Dict:
        """Run comprehensive evaluation"""
        crop_results = self.crop_accuracy_test()
        
        return {
            "crop_accuracy": crop_results,
            "summary": f"Fine-tuning improved accuracy by {crop_results['improvement']:.2%}"
        }

if __name__ == "__main__":
    evaluator = AgriEvaluator(
        base_model_path="meta-llama/Llama-2-7b-chat-hf",
        adapter_path="fine_tuning/imarika-llama3"
    )
    results = evaluator.run_evaluation()
    print(json.dumps(results, indent=2))