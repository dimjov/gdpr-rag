from typing import List, Tuple, Optional, Dict, Any
from src.embedder import get_embedding
from src.vector_store import get_chroma_client, get_or_create_collection
from src.config import TOP_K, COLLECTION_NAME
from src.utils import try_extract_article_id

def retrieve(query: str, where: Optional[Dict[str, Any]] = None, n_results: int = TOP_K) -> List[Tuple[str, dict]]:
    """
    Returns list of (document_text, metadata) tuples.
    Example: Article match first (e.g., "Article 6"), then semantic search.
    """
    client = get_chroma_client()
    collection = get_or_create_collection(client, COLLECTION_NAME)

    # 1) Exact article id path if user referenced "Article N"
    art_node = try_extract_article_id(query)
    if art_node:
        exact = collection.get(where={"node_id": art_node}, include=["documents", "metadatas", "ids"])
        docs, metas = [], []
        if exact and exact.get("documents"):
            for dlist, mlist in zip(exact["documents"], exact["metadatas"]):
                for d, m in zip(dlist, mlist):
                    docs.append(d); metas.append(m)
        if docs:
            return list(zip(docs[:n_results], metas[:n_results]))

    # 2) Optional metadata filter from caller
    where = where or {}

    # 3) Semantic search
    qemb = get_embedding(query)
    res = collection.query(query_embeddings=[qemb], where=where, n_results=n_results)
    documents = res.get("documents", [[]])[0]
    metadatas = res.get("metadatas", [[]])[0]
    return list(zip(documents, metadatas))
