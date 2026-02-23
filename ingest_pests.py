"""
ingest_pests.py - Clean ingestion for pests knowledge base into Qdrant.
"""
import os
import re
import uuid
from pathlib import Path
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from tqdm import tqdm

try:
    import ftfy
    HAS_FTFY = True
except ImportError:
    HAS_FTFY = False

# ========================
# CONFIG
# ========================
KB_DIR = Path("kb/kb_pests")
QDRANT_PATH = "qdrant_storage"
COLLECTION_NAME = "pests_kb"
MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE = 800
OVERLAP = 150

def html_table_to_markdown(table_soup):
    rows = []
    trs = table_soup.find_all("tr")
    if not trs: return ""
    for i, tr in enumerate(trs):
        cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
        if not any(cells): continue
        rows.append("| " + " | ".join(cells) + " |")
        if i == 0 and len(cells) > 0:
            rows.append("| " + " | ".join(["---"] * len(cells)) + " |")
    return "\n".join(rows)

def clean_text(text: str) -> str:
    if HAS_FTFY: text = ftfy.fix_text(text)
    soup = BeautifulSoup(text, "lxml")
    for table in soup.find_all("table"):
        md = html_table_to_markdown(table)
        table.replace_with("\n\n" + md + "\n\n")
    text = soup.get_text(separator="\n")
    # Aggressive multi-pass tag strip
    for _ in range(3):
        text = re.sub(r'<[^>]+>', ' ', text, flags=re.DOTALL)
    text = re.sub(r'\S{60,}', '', text)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = re.sub(r'&[a-zA-Z]+;', ' ', text)
    text = re.sub(r'&#\d+;', ' ', text)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', ' ', text)
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    sentences = re.split(r'(?<=[.?!])\s+', text)
    chunks, current, clen = [], [], 0
    for sent in sentences:
        slen = len(sent)
        if clen + slen > chunk_size and current:
            chunks.append(" ".join(current))
            ob, ol = [], 0
            for s in reversed(current):
                if ol + len(s) < overlap:
                    ob.insert(0, s)
                    ol += len(s)
                else: break
            current, clen = ob + [sent], ol + slen
        else:
            current.append(sent)
            clen += slen
    if current: chunks.append(" ".join(current))
    return [c for c in chunks if len(c.strip()) > 30]

def main():
    print(f"Loading model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    client = QdrantClient(path=QDRANT_PATH)
    try: client.delete_collection(COLLECTION_NAME)
    except: pass
    client.create_collection(collection_name=COLLECTION_NAME, vectors_config=VectorParams(size=384, distance=Distance.COSINE))
    md_files = list(KB_DIR.glob("*.md"))
    all_chunks = []
    for f in md_files:
        raw = f.read_text(encoding="utf-8", errors="replace")
        cleaned = clean_text(raw)
        chunks = chunk_text(cleaned)
        for c in chunks: all_chunks.append({"text": c, "source": f.name})
    BATCH = 100
    for i in tqdm(range(0, len(all_chunks), BATCH), desc="Upserting"):
        batch = all_chunks[i : i + BATCH]
        texts = [c["text"] for c in batch]
        vectors = model.encode(texts, show_progress_bar=False).tolist()
        points = [PointStruct(id=str(uuid.uuid4()), vector=vec, payload={"text": c["text"], "source": c["source"]}) for c, vec in zip(batch, vectors)]
        client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"\n✅ {COLLECTION_NAME} COMPLETE")

if __name__ == "__main__":
    main()
