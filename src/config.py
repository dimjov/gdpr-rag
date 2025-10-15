import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# --- Paths (resolve relative to this file) ---
BASE_DIR = Path(__file__).resolve().parent
DATA_JSON_PATH = (BASE_DIR / "../data/gdpr_structured.json").resolve().as_posix()
CHROMA_PATH = (BASE_DIR / "../chroma_db").resolve().as_posix()

# --- Ollama ---
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text:v1.5")
LLM_MODEL = os.getenv("LLM_MODEL", "phi3:mini")

# --- Retrieval / RAG settings ---
COLLECTION_NAME = "gdpr"
TOP_K = int(os.getenv("TOP_K", "5"))
MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", "8000"))
CHUNK_MAX_WORDS = int(os.getenv("CHUNK_MAX_WORDS", "300"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "128"))

# Silence Chroma telemetry noise (optional)
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")
