import chromadb as chroma
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from app.config import EMBEDDING_MODEL, OLLAMA_BASE_URL

ollamma_embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)

# chroma client
client = chroma.HttpClient(host="chroma", port=8000)

# chroma DB
chroma_db = Chroma(
    collection_name="documents", embedding_function=ollamma_embeddings, client=client
)
