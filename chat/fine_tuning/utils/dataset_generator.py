import json
import csv
import random
from pathlib import Path
from typing import List, Dict

class AgriDatasetGenerator:
    def __init__(self, data_dir: str = "../data"):
        self.data_dir = Path(data_dir)
        self.crops = ["beans", "cassava", "finger_millet", "maize", "sorghum", "sweet_potatoes"]
        
    def load_crop_data(self) -> Dict:
        crop_data = {}
        for crop in self.crops:
            file_path = self.data_dir / f"{crop}.csv"
            if file_path.exists():
                with open(file_path, 'r') as f:
                    reader = csv.DictReader(f)
                    crop_data[crop] = list(reader)
        return crop_data
    
    def generate_instruction_pairs(self, num_samples: int = 1000) -> List[Dict]:
        crop_data = self.load_crop_data()
        instructions = []
        
        templates = [
            {
                "instruction": "What crops are suitable for {weather} conditions?",
                "response": "For {weather} conditions, I recommend {crop} because it's {reason}."
            },
            {
                "instruction": "How do I manage pests in {crop}?",
                "response": "To manage pests in {crop}: use organic pesticides and crop rotation."
            },
            {
                "instruction": "What nutrients does {crop} need?",
                "response": "{crop} needs nitrogen, phosphorus, and potassium for optimal growth."
            }
        ]
        
        for _ in range(num_samples):
            template = random.choice(templates)
            crop = random.choice(self.crops)
            weather = random.choice(["dry", "wet", "humid"])
            
            instruction = template["instruction"].format(
                crop=crop.replace('_', ' '),
                weather=weather
            )
            
            response = template["response"].format(
                crop=crop.replace('_', ' '),
                weather=weather,
                reason="drought-resistant and suitable for East African climate"
            )
            
            instructions.append({
                "messages": [
                    {"role": "system", "content": "You are Imarika, an agricultural expert for East African crops."},
                    {"role": "user", "content": instruction},
                    {"role": "assistant", "content": response}
                ]
            })
            
        return instructions
    
    def save_dataset(self, instructions: List[Dict], filename: str = "agri_dataset.jsonl"):
        output_path = Path(filename)
        
        with open(output_path, 'w') as f:
            for item in instructions:
                f.write(json.dumps(item) + '\n')
        
        print(f"Dataset saved to {output_path} with {len(instructions)} samples")

if __name__ == "__main__":
    generator = AgriDatasetGenerator()
    dataset = generator.generate_instruction_pairs(2000)
    generator.save_dataset(dataset)