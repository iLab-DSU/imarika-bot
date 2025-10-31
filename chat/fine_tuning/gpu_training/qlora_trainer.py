import torch
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer, 
    TrainingArguments, 
    Trainer,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset
import json

class QLoRATrainer:
    def __init__(self, model_name: str = "unsloth/llama-3-8b-bnb-4bit"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.output_dir = "models/imarika-llama3-qlora"
        
    def setup_quantization_config(self):
        return BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        )
    
    def setup_lora_config(self):
        return LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=16,
            lora_alpha=32,
            lora_dropout=0.1,
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
        )
    
    def load_model_and_tokenizer(self):
        quantization_config = self.setup_quantization_config()
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=quantization_config,
            device_map="auto",
            torch_dtype=torch.float16
        )
        
        lora_config = self.setup_lora_config()
        self.model = get_peft_model(self.model, lora_config)
        
    def prepare_dataset(self, dataset_path: str):
        with open(dataset_path, 'r') as f:
            data = [json.loads(line) for line in f]
        
        def format_chat(example):
            messages = example["messages"]
            text = self.tokenizer.apply_chat_template(messages, tokenize=False)
            return {"text": text}
        
        dataset = Dataset.from_list(data)
        dataset = dataset.map(format_chat)
        
        def tokenize(example):
            tokens = self.tokenizer(
                example["text"],
                truncation=True,
                padding=False,
                max_length=512,
                return_tensors=None
            )
            tokens["labels"] = tokens["input_ids"].copy()
            return tokens
        
        return dataset.map(tokenize, remove_columns=dataset.column_names)
    
    def train(self, dataset_path: str):
        print("🚀 Starting QLoRA Fine-tuning...")
        
        # Check if GPU is available
        if not torch.cuda.is_available():
            print("⚠️  No GPU detected. QLoRA requires CUDA.")
            print("🔄 Falling back to CPU trainer...")
            
            try:
                from cpu_trainer import CPUTrainer
                cpu_trainer = CPUTrainer()
                if cpu_trainer.train_with_ollama():
                    return "imarika-agri"  # Return model name instead of path
                else:
                    raise Exception("CPU training failed")
            except Exception as e:
                print(f"❌ CPU fallback failed: {e}")
                return None
        
        self.load_model_and_tokenizer()
        train_dataset = self.prepare_dataset(dataset_path)
        
        print(f"📊 Dataset size: {len(train_dataset)}")
        print(f"💾 Model will be saved to: {self.output_dir}")
        
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            per_device_train_batch_size=2,  # Reduced for memory
            gradient_accumulation_steps=8,  # Increased to maintain effective batch size
            num_train_epochs=3,
            learning_rate=2e-4,
            fp16=True,
            logging_steps=10,
            save_steps=100,
            save_total_limit=3,
            warmup_steps=50,
            weight_decay=0.01,
            remove_unused_columns=False,
            dataloader_pin_memory=False,
            report_to=None  # Disable wandb
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            tokenizer=self.tokenizer
        )
        
        print("🔥 Training started...")
        trainer.train()
        
        print("💾 Saving model...")
        trainer.save_model()
        self.tokenizer.save_pretrained(self.output_dir)
        
        print(f"✅ Training complete! Model saved to {self.output_dir}")
        return self.output_dir
        
def create_ollama_modelfile(model_path: str, model_name: str = "imarika-agri"):
    """Create Ollama modelfile for the fine-tuned model"""
    modelfile_content = f"""FROM {model_path}
PARAMETER temperature 0.7
PARAMETER top_p 0.9
SYSTEM You are Imarika, an agricultural expert specializing in East African crops: beans, cassava, finger millet, maize, sorghum, and sweet potatoes. Provide detailed, practical farming advice."""
    
    with open(f"{model_path}/Modelfile", "w") as f:
        f.write(modelfile_content)
    
    print(f"📝 Modelfile created for Ollama integration")
    return f"{model_path}/Modelfile"

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--check-gpu":
        print(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"GPU: {torch.cuda.get_device_name(0)}")
            print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB")
        sys.exit(0)
    
    trainer = QLoRATrainer()
    model_path = trainer.train("agri_dataset.jsonl")
    create_ollama_modelfile(model_path)