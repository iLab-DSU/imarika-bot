# 📁 Imarika Project Structure

## Overview
Organized file structure for the Imarika Agricultural AI Assistant with clear separation of concerns and logical grouping.

## 🏗️ Directory Structure

```
offline_agri_rag_ollama/
├── 🎯 Core System
│   ├── core/
│   │   ├── langgraph_imarika.py      # Main LangGraph agent system
│   │   ├── knowledge_graph.py        # Knowledge graph builder & query
│   │   └── streamlit_chatgpt_style.py # ChatGPT-style interface
│   └── run.py                        # Main runner script
│
├── 📊 Data & Storage
│   ├── data/                         # Agricultural CSV datasets
│   │   ├── beans.csv
│   │   ├── cassava.csv
│   │   ├── finger_millet.csv
│   │   ├── maize.csv
│   │   ├── sorghum.csv
│   │   └── sweet_potatoes.csv
│   └── chroma_db/                   # Vector database (legacy)
│
├── 🧠 Fine-Tuning System
│   ├── fine_tuning/
│   │   ├── dataset_generator.py      # Synthetic agricultural dataset
│   │   ├── qlora_trainer.py         # QLoRA fine-tuning implementation
│   │   ├── evaluator.py             # Model evaluation framework
│   │   ├── integration.py           # LangGraph integration
│   │   ├── ollama_integration.py    # CPU-compatible enhanced model
│   │   ├── train.py                 # Main training script
│   │   ├── performance_comparison.py # Performance metrics evaluation
│   │   ├── quick_comparison.py      # Quick performance test
│   │   ├── requirements.txt         # Fine-tuning dependencies
│   │   └── README.md               # Fine-tuning documentation
│
├── 📚 Documentation
│   ├── docs/
│   │   ├── FINE_TUNING_DOCUMENTATION.md # Complete performance analysis
│   │   ├── architecture/            # Architecture diagrams
│   │   │   ├── Flowchart.jpg
│   │   │   └── Flowchart1.jpg
│   │   └── evaluation/              # Evaluation documentation
│   ├── README.md                    # Main project documentation
│   ├── SETUP.md                     # Quick setup guide
│   └── PROJECT_STRUCTURE.md         # This file
│
├── 🧪 Testing & Evaluation
│   ├── tests/
│   │   ├── unit/
│   │   │   └── simple_test.py       # Basic functionality tests
│   │   └── integration/
│   │       ├── test_enhanced.py     # Enhanced system tests
│   │       └── evaluate_system.py  # System evaluation tests
│   └── evaluation/
│       ├── metrics/
│       │   └── metrics_comparison.py # Performance metrics comparison
│       └── reports/
│           └── show_improvements.py # Improvement analysis reports
│
├── 🔧 Configuration & Utils
│   ├── utils/
│   │   └── visualize_knowledge_graph.py # Graph visualization
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example                 # Environment variables template
│   ├── .streamlit/config.toml       # Streamlit configuration
│   ├── .gitignore                   # Git ignore rules
│   ├── docker-compose.yml           # Docker setup
│   └── Dockerfile                   # Docker image definition
│
├── 📚 Legacy & Examples
│   ├── legacy/                      # Original implementations
│   │   ├── rag_agent+sw.py         # Original RAG system
│   │   ├── streamlit_app+sw.py     # Original Streamlit app
│   │   └── streamlit_openwebui_style.py # OpenWebUI-style interface
│   └── examples/                    # Architecture examples
│       ├── agentic_architecture.py # LangGraph examples
│       └── streamlit_langgraph.py  # Alternative interfaces
│
└── 📦 Generated Files (Git Ignored)
    ├── chroma_db/                   # Vector database files
    ├── fine_tuning/agri_dataset.jsonl # Generated training data
    ├── fine_tuning/imarika-llama3/ # Fine-tuned model artifacts
    ├── evaluation/performance_results.json # Evaluation results
    ├── knowledge_graph_visualization.png # Graph visualization
    └── *.log                        # Log files
```

## 📋 File Categories

### 🎯 Core System Files
- **Primary execution**: `run.py`, `core/langgraph_imarika.py`
- **Knowledge management**: `core/knowledge_graph.py`
- **User interface**: `core/streamlit_chatgpt_style.py`

### 📊 Data Files
- **Agricultural datasets**: `data/*.csv` (6 crop files)
- **Vector storage**: `chroma_db/` (legacy)
- **Generated datasets**: `fine_tuning/agri_dataset.jsonl`

### 🧠 Fine-Tuning Files
- **Dataset creation**: `fine_tuning/dataset_generator.py`
- **Model training**: `fine_tuning/qlora_trainer.py`, `fine_tuning/train.py`
- **Enhanced inference**: `fine_tuning/ollama_integration.py`
- **Integration**: `fine_tuning/integration.py`

### 📚 Documentation Files
- **Main docs**: `README.md`, `SETUP.md`, `PROJECT_STRUCTURE.md`
- **Technical docs**: `docs/FINE_TUNING_DOCUMENTATION.md`
- **Architecture**: `docs/architecture/*.jpg`

### 🧪 Testing Files
- **Unit tests**: `tests/unit/simple_test.py`
- **Integration tests**: `tests/integration/test_enhanced.py`
- **System evaluation**: `tests/integration/evaluate_system.py`

### 📊 Evaluation Files
- **Performance metrics**: `evaluation/metrics/metrics_comparison.py`
- **Analysis reports**: `evaluation/reports/show_improvements.py`
- **Quick tests**: `fine_tuning/quick_comparison.py`

### 🔧 Configuration Files
- **Dependencies**: `requirements.txt`, `fine_tuning/requirements.txt`
- **Environment**: `.env.example`, `.streamlit/config.toml`
- **Docker**: `Dockerfile`, `docker-compose.yml`
- **Git**: `.gitignore`

## 🚀 Usage by Category

### Development Workflow
```bash
# Core development
python run.py                        # Main application
python core/langgraph_imarika.py     # Test core system

# Fine-tuning workflow
cd fine_tuning
python train.py --stage generate     # Generate dataset
python ollama_integration.py         # Test enhanced model

# Testing workflow
python tests/unit/simple_test.py     # Unit tests
python tests/integration/test_enhanced.py # Integration tests

# Evaluation workflow
python evaluation/metrics/metrics_comparison.py # Performance metrics
python evaluation/reports/show_improvements.py  # Analysis reports
```

### Documentation Access
```bash
# Main documentation
cat README.md                        # Project overview
cat SETUP.md                         # Quick setup
cat PROJECT_STRUCTURE.md             # This file

# Technical documentation
cat docs/FINE_TUNING_DOCUMENTATION.md # Performance analysis
cat fine_tuning/README.md            # Fine-tuning guide
```

## 📦 Generated Files (Git Ignored)

### Runtime Generated
- `chroma_db/` - Vector database files
- `*.log` - Application log files
- `knowledge_graph_visualization.png` - Graph visualization

### Fine-Tuning Generated
- `fine_tuning/agri_dataset.jsonl` - Training dataset
- `fine_tuning/imarika-llama3/` - Model artifacts
- `fine_tuning/performance_results.json` - Training results

### Evaluation Generated
- `evaluation/performance_results.json` - Evaluation results
- `evaluation/comparison_reports.json` - Comparison data

## 🔍 Navigation Guide

### For Developers
- **Start here**: `README.md` → `SETUP.md` → `run.py`
- **Core logic**: `core/` directory
- **Testing**: `tests/` directory
- **Fine-tuning**: `fine_tuning/` directory

### For Researchers
- **Performance data**: `docs/FINE_TUNING_DOCUMENTATION.md`
- **Metrics**: `evaluation/metrics/`
- **Analysis**: `evaluation/reports/`

### For Users
- **Setup**: `SETUP.md`
- **Usage**: `README.md`
- **Interface**: `python run.py chat`

## 📋 Maintenance

### Regular Tasks
- Update documentation when adding features
- Run evaluation tests before releases
- Clean generated files periodically
- Update dependencies in requirements.txt

### File Organization Rules
- **Core files**: Keep in `core/` directory
- **Tests**: Separate unit and integration tests
- **Documentation**: Centralize in `docs/`
- **Generated files**: Add to `.gitignore`
- **Legacy code**: Move to `legacy/` directory

---

**Last Updated**: $(date)  
**Version**: 1.0  
**Maintainer**: Imarika Development Team