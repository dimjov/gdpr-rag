import re
import json
from bs4 import BeautifulSoup
from pathlib import Path

INPUT_HTML = Path("data/gdpr.html")
OUTPUT_JSON = Path("data/gdpr_structured.json")

def clean_text(s: str) -> str:
    """Normalize whitespace."""
    if not s:
        return ""
    return " ".join(s.split()).strip()

def extract_gdpr_structure(html_path: Path):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    results = []

    # ---------- Citations ----------
    for div in soup.find_all("div", id=lambda x: x and x.startswith("cit_")):
        paragraphs = div.find_all("p", class_="oj-normal")
        if not paragraphs:
            continue
        text = " ".join(clean_text(p.get_text()) for p in paragraphs)
        results.append({
            "id": div["id"],
            "type": "citation",
            "title": f"Citation {div['id'].split('_')[1]}",
            "content": text
        })

    # ---------- Recitals ----------
    for div in soup.find_all("div", id=lambda x: x and x.startswith("rct_")):
        num = div["id"].split("_")[1]
        tds = div.find_all("td", valign="top")
        if len(tds) == 2:
            # left = number (e.g., (1)), right = text
            body = " ".join(clean_text(p.get_text()) for p in tds[1].find_all("p", class_="oj-normal"))
        else:
            body = " ".join(clean_text(p.get_text()) for p in div.find_all("p", class_="oj-normal"))
        results.append({
            "id": div["id"],
            "type": "recital",
            "title": f"Recital {num}",
            "content": body
        })

    # ---------- Chapters ----------
    for div in soup.find_all("div", id=lambda x: x and re.match(r"^cpt_[IVXLC]+$", x)):
        chap_num = div["id"].split("_")[1]
        chap_label = div.find("p", class_="oj-ti-section-1")
        chap_name = div.find("p", class_="oj-ti-section-2")
        chap_label_text = clean_text(chap_label.get_text()) if chap_label else f"Chapter {chap_num}"
        chap_name_text = clean_text(chap_name.get_text()) if chap_name else ""
        results.append({
            "id": div["id"],
            "type": "chapter",
            "title": f"{chap_label_text} — {chap_name_text}".strip("— "),
            "content": ""
        })

    # ---------- Sections ----------
    for div in soup.find_all("div", id=lambda x: x and re.match(r"^cpt_[IVXLC]+\.sct_\d+$", x)):
        sec_num = div["id"].split(".sct_")[1]
        sec_label = div.find("p", class_="oj-ti-section-1")
        sec_name = div.find("p", class_="oj-ti-section-2")
        sec_label_text = clean_text(sec_label.get_text()) if sec_label else f"Section {sec_num}"
        sec_name_text = clean_text(sec_name.get_text()) if sec_name else ""
        results.append({
            "id": div["id"],
            "type": "section",
            "title": f"{sec_label_text} — {sec_name_text}".strip("— "),
            "content": ""
        })

    # ---------- Articles ----------
    for div in soup.find_all("div", id=lambda x: x and re.match(r"^art_\d+$", x)):
        art_id = div["id"]
        art_title_tag = div.find("p", class_="oj-ti-art")
        art_name_tag = div.find("p", class_="oj-sti-art")
        art_title = clean_text(art_title_tag.get_text()) if art_title_tag else ""
        art_name = clean_text(art_name_tag.get_text()) if art_name_tag else ""
        paragraphs = div.find_all("p", class_="oj-normal")
        text = " ".join(clean_text(p.get_text()) for p in paragraphs)
        results.append({
            "id": art_id,
            "type": "article",
            "title": f"{art_title} — {art_name}".strip("— "),
            "content": text
        })

    return results

def main():
    print(f"📖 Parsing GDPR HTML: {INPUT_HTML}")
    docs = extract_gdpr_structure(INPUT_HTML)
    print(f"✅ Extracted {len(docs)} structured elements.")
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
