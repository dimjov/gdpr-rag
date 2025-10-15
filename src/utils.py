import re
from typing import Iterable, List

def clean_text(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"\s+", " ", s)
    s = s.replace("’", "'").replace("“", '"').replace("”", '"')
    return s.strip()

def chunk_by_words(text: str, max_words: int = 300) -> List[str]:
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

def print_boxed(text: str) -> None:
    text = text.strip()
    width = 100
    border = "=" * width
    print("\n" + border)
    while text:
        print(text[:width])
        text = text[width:]
    print(border + "\n")

def normalize_title(t: str) -> str:
    t = (t or "").lower().strip()
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"[^\w\s\-–—:]", "", t)
    return t

def try_extract_article_id(query: str) -> str | None:
    """Return art_N id from query if the user references 'Article N'."""
    m = re.search(r"\barticle\s+(\d+)\b", query, flags=re.IGNORECASE)
    if m:
        return f"art_{int(m.group(1))}"
    return None
