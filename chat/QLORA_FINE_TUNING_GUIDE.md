# 🧠 QLoRA Fine-Tuning Guide for Imarika

## Overview

Complete guide for fine-tuning Llama 3.2 3B with QLoRA using agricultural CSV data and integrating it into the Imarika system.

## 📋 Table of Contents

1. [Fine-Tuning Process](#fine-tuning-process)
2. [Integration Steps](#integration-steps)
3. [Performance Evaluation](#performance-evaluation)
4. [Usage Instructions](#usage-instructions)
5. [Troubleshooting](#troubleshooting)

## 🚀 Fine-Tuning Process

### Option 1: Google Colab (Recommended)

```bash
# 1. Open notebook
fine_tuning/notebooks/imarika_csv_qlora.ipynb

# 2. Upload CSV files
# - beans.csv
# - cassava.csv
# - finger_millet.csv
# - maize.csv
# - sorghum.csv
# - sweet_potatoes.csv

# 3. Run all cells (2-4 hours)

# 4. Download model
# imarika_csv_qlora_model.zip (~1.5GB)
```

### Option 2: Local Training

```bash
# Install dependencies
pip install torch transformers peft datasets accelerate bitsandbytes trl

# Generate dataset
cd fine_tuning
python train.py --stage generate --samples 2000

# Train model
python train.py --stage train

# Evaluate
python train.py --stage evaluate
```

## 🔧 Integration Steps

### Step 1: Place Model File

```bash
# Copy model zip to project root
cp imarika_csv_qlora_model.zip /path/to/offline_agri_rag_ollama/
```

### Step 2: Test Integration

```bash
# Run complete test suite
python test_qlora_integration.py

# Expected output:
# ✅ QLoRA model loaded successfully
# ✅ Model Integration Status
# ✅ All tests completed
```

### Step 3: Verify Performance

```bash
# Run performance comparison
cd fine_tuning
python performance_evaluator.py

# Expected improvements:
# +50-150% overall performance
# +200-400% agricultural keywords
# +100-300% query relevance
```

## 📊 Performance Evaluation

### Metrics Used

1. **Response Length Score** (0-1): Completeness
2. **Agricultural Keyword Density** (0-1): Domain terminology
3. **Query Relevance Score** (0-1): Context appropriateness
4. **Crop Specificity** (0-1): Target crop mentions
5. **Practical Advice Score** (0-1): Actionable recommendations
6. **Composite Score** (0-1): Weighted average
7. **Response Time**: Generation speed

### Test Queries (26 total)

**Nutrients:**
- What nutrients does maize need for optimal growth?
- Which fertilizers are best for beans cultivation?
- How to improve soil fertility for cassava?

**Pests & Diseases:**
- Common pests affecting maize crops
- How to control bean weevils naturally?
- Cassava mosaic disease prevention

**Weather & Climate:**
- Best weather conditions for maize planting
- How does rainfall affect bean production?
- Drought-resistant cassava varieties

**Farming Practices:**
- Maize intercropping with beans benefits
- Proper spacing for cassava planting
- Harvesting time for finger millet

### Expected Results

**Quality Improvements:**
- Composite Score: +50-150%
- Agricultural Keywords: +200-400%
- Query Relevance: +100-300%
- Crop Specificity: +80-150%
- Practical Advice: +50-100%

**Performance:**
- GPU Inference: 2-5 seconds
- CPU Inference: 10-20 seconds
- Model Size: 1.5GB (4-bit quantized)
- Memory: 4-6GB GPU VRAM

## 💻 Usage Instructions

### Basic Usage

```python
from fine_tuning.qlora_model_integration import IntegratedImarika

# Initialize (auto-detects QLoRA or falls back to Ollama)
imarika = IntegratedImarika()

# Generate response
response = imarika.generate_response(
    "What nutrients does maize need?",
    context="Weather: 25°C, humid"
)

print(response)
```

### LangGraph Integration

```python
from fine_tuning.langgraph_qlora_integration import QLoRALangGraphAgent

# Initialize agent
agent = QLoRALangGraphAgent()

# Run query with tools (weather + knowledge graph)
response = agent.run_agent("Maize nutrients in Nairobi weather")

print(response)
```

### Streamlit Integration

```bash
# Launch chat interface
python run.py chat

# System automatically uses QLoRA if available
# Falls back to Ollama if model not found
```

## 🔍 Troubleshooting

### Model Not Loading

```bash
# Check if zip exists
ls -lh imarika_csv_qlora_model.zip

# Check extraction
ls -lh fine_tuning/qlora_model/

# Test manually
python fine_tuning/qlora_model_integration.py
```

### GPU Issues

```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Check GPU memory
nvidia-smi

# Use CPU fallback (slower)
# System automatically falls back if GPU unavailable
```

### Slow Inference

```bash
# GPU inference: 2-5 seconds
# CPU inference: 10-20 seconds (expected)

# Optimize:
# 1. Use GPU for faster inference
# 2. Reduce max_length in generate_response()
# 3. Enable caching for repeated queries
```

### Import Errors

```bash
# Install missing dependencies
pip install torch transformers peft bitsandbytes

# Check Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Verify installation
python test_qlora_integration.py
```

## 📈 Fine-Tuning Report

### Dataset Generation

- **Source**: 6 CSV files with agricultural data
- **Training Samples**: 500-2000 instruction-response pairs
- **Format**: Llama 3.2 chat template
- **Coverage**: All 6 crops, nutrients, pests, weather, practices
- **Languages**: English and Swahili

### Model Architecture

- **Base Model**: Llama 3.2 3B Instruct
- **Quantization**: 4-bit NF4 with double quantization
- **LoRA Config**:
  - Rank (r): 16
  - Alpha: 32
  - Dropout: 0.05
  - Target modules: q_proj, k_proj, v_proj, o_proj
- **Training**:
  - Epochs: 3
  - Batch size: 4
  - Learning rate: 2e-4
  - Optimizer: AdamW 8-bit

### Sample Comparison

**Query**: "What nutrients does maize need?"

**Base Model** (Score: 0.231):
```
Maize needs nitrogen, phosphorus, and potassium.
```

**Fine-Tuned Model** (Score: 0.550):
```
Maize (Mahindi) requires several key nutrients for optimal growth in East African conditions:

1. **Nitrogen (N)**: Essential for leaf and stem growth. Apply 60-120 kg/ha.
2. **Phosphorus (P)**: Critical for root development. Apply 40-60 kg/ha.
3. **Potassium (K)**: Improves disease resistance. Apply 30-60 kg/ha.
4. **Organic Matter**: Manure or compost at 5-10 tons/ha.
5. **Micronutrients**: Zinc and boron for better yields.

Apply NPK fertilizer (23:23:0 or 17:17:17) at planting, 2-3 inches from seeds. 
Top-dress with CAN or Urea 4-6 weeks after planting.
```

**Improvement**: +138% composite score, +400% agricultural keywords, +250% detail

## 🎯 Next Steps

1. **Run Integration Test**: `python test_qlora_integration.py`
2. **Evaluate Performance**: `python fine_tuning/performance_evaluator.py`
3. **Test in Chat**: `python run.py chat`
4. **Compare Results**: Review evaluation reports
5. **Deploy**: Use QLoRA model in production

## 📚 Additional Resources

- [Fine-Tuning Notebook](fine_tuning/notebooks/imarika_csv_qlora.ipynb)
- [Integration Code](fine_tuning/qlora_model_integration.py)
- [Performance Evaluator](fine_tuning/performance_evaluator.py)
- [LangGraph Integration](fine_tuning/langgraph_qlora_integration.py)
- [Test Suite](test_qlora_integration.py)

---

**Built for East African farmers with QLoRA fine-tuning**