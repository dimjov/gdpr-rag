import requests
from src.config import OLLAMA_URL, EMBED_MODEL

def get_embedding(text: str) -> list[float]:
    r = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=120,
    )
    r.raise_for_status()
    data = r.json()
    return data["embedding"]
