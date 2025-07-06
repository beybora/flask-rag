import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# Setup embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_key,
    model_name="text-embedding-3-small"
)

# Persistent Chroma client
chroma_client = chromadb.PersistentClient(path="chroma_storage")

# Get or create collection
collection = chroma_client.get_or_create_collection(
    name="document_collection",
    embedding_function=openai_ef
)

# Expose for import
__all__ = ["collection"]
