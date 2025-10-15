import json
from pathlib import Path
from tqdm import tqdm

from src.config import DATA_JSON_PATH, CHUNK_MAX_WORDS, BATCH_SIZE, COLLECTION_NAME
from src.utils import clean_text, chunk_by_words, normalize_title
from src.embedder import get_embedding
from src.vector_store import get_chroma_client, get_or_create_collection

def _iter_docs():
    with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        # expected keys: id, type, title, content; optional: chapter, section
        node_id = item.get("id", "").strip()
        node_type = item.get("type", "").strip()
        title = clean_text(item.get("title", ""))
        content = clean_text(item.get("content", ""))
        chapter = item.get("chapter")
        section = item.get("section")

        if not node_id or not content:
            continue

        # chunk long content
        chunks = chunk_by_words(content, CHUNK_MAX_WORDS)
        for j, chunk in enumerate(chunks):
            yield {
                "id": f"{node_id}:{j}",
                "node_id": node_id,                 # base id (for exact targeting, e.g. art_6)
                "type": node_type,
                "title": title,
                "title_norm": normalize_title(title),
                "chapter": chapter or "",
                "section": section or "",
                "text": chunk,
            }

def ingest():
    client = get_chroma_client()
    collection = get_or_create_collection(client, COLLECTION_NAME)

    ids, docs, metas, embs = [], [], [], []
    count = 0

    for rec in tqdm(_iter_docs(), desc="Embedding & adding", unit="chunk"):
        ids.append(rec["id"])
        docs.append(rec["text"])
        metas.append({
            "node_id": rec["node_id"],
            "type": rec["type"],
            "title": rec["title"],
            "title_norm": rec["title_norm"],
            "chapter": rec["chapter"],
            "section": rec["section"],
        })
        embs.append(get_embedding(rec["text"]))
        count += 1

        if len(ids) >= BATCH_SIZE:
            collection.add(ids=ids, documents=docs, metadatas=metas, embeddings=embs)
            ids, docs, metas, embs = [], [], [], []

    if ids:  # flush remainder
        collection.add(ids=ids, documents=docs, metadatas=metas, embeddings=embs)

    print(f"✅ Ingested {count} chunks into collection '{COLLECTION_NAME}'.")

if __name__ == "__main__":
    ingest()
