# 🚀 Quick Setup Guide

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Ollama installed and running
- [ ] Git installed

## 1-Minute Setup

```bash
# 1. Clone repository
git clone <your-repo-url>
cd offline_agri_rag_ollama

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Ollama models (this may take a few minutes)
ollama pull llama3
ollama pull mxbai-embed-large

# 4. Start the ChatGPT-style interface
python run.py
```

## Verify Installation

```bash
# Test knowledge graph
python run.py build-kg

# Run system tests
python run.py test

# Start ChatGPT-style chat interface
python run.py chat
```

## Access Points

- **ChatGPT-Style Interface**: http://localhost:8501
- **Knowledge Graph Viewer**: Built into chat interface
- **System Status**: Check terminal output
- **Logs**: Streamlit logs in terminal

## Troubleshooting

### Ollama Not Found
```bash
# Install Ollama first
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve  # Start Ollama service
```

### Port Already in Use
```bash
# Use different port
streamlit run streamlit_openwebui_style.py --server.port 8502
```

### Missing Dependencies
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

## Optional: Weather API

1. Get free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Copy `.env.example` to `.env`
3. Add your API key to `.env`

## Success Indicators

✅ Ollama models loaded  
✅ Knowledge graph built (22 nodes, 72 edges)  
✅ Streamlit interface accessible  
✅ Chat responses working  

## Next Steps

- Try example queries in the chat interface
- Explore the knowledge graph relationships
- Test weather-based agricultural advice