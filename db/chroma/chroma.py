from app.config import EMBEDDING_MODEL, OLLAMA_BASE_URL
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import chromadb as chroma

ollamma_embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)

# chroma client
client = chroma.HttpClient(host="chroma", port=8080)

# chroma DB
chroma_db = Chroma(
    collection_name="documents",
    embedding_function=ollamma_embeddings,
    client=client
)
