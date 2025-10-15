import chromadb
from src.config import CHROMA_PATH, COLLECTION_NAME

def get_chroma_client():
    # Chroma ≥ 0.5 persistent client
    return chromadb.PersistentClient(path=CHROMA_PATH)

def get_or_create_collection(client, name: str = COLLECTION_NAME):
    return client.get_or_create_collection(name=name)
