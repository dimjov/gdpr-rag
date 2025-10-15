import requests
from src.config import OLLAMA_URL, LLM_MODEL, MAX_CONTEXT_CHARS

RULES = (
    "You are a GDPR assistant. Answer ONLY from the provided context (GDPR text). "
    "If the answer is not clearly supported by the context, reply: "
    "'I couldn't find that in the indexed GDPR text.' Do NOT guess. "
    "Always mention the relevant Article/Recital titles you used."
)

def _trim_context(chunks: list[str], max_chars: int = MAX_CONTEXT_CHARS) -> str:
    out = []
    total = 0
    for c in chunks:
        if total + len(c) + 2 > max_chars:
            break
        out.append(c)
        total += len(c) + 2
    return "\n\n---\n\n".join(out)

def generate_answer(context_chunks: list[str], query: str) -> str:
    if not context_chunks:
        return "I couldn't find relevant passages in the indexed GDPR text."

    context_text = _trim_context(context_chunks)
    prompt = (
        f"{RULES}\n\n"
        f"Question: {query}\n\n"
        f"Context:\n{context_text}\n\n"
        f"Answer:"
    )

    r = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": LLM_MODEL, "prompt": prompt, "stream": False},
        timeout=300,
    )
    r.raise_for_status()
    return r.json().get("response", "").strip()
