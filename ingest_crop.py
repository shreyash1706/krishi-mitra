"""
ingest_crop.py - Clean ingestion for crop knowledge base into Qdrant.
Handles:
  - HTML/XML tags (BeautifulSoup + Regex fallback)
  - HTML tables -> Markdown tables
  - Broken UTF-8 / Windows-1252 mojibake (ftfy)
  - PDF extraction artifacts
  - Sliding window chunking with overlap
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
KB_DIR = Path("kb/kb_crop")
QDRANT_PATH = "qdrant_storage"
COLLECTION_NAME = "crop_kb"
MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE = 800    # Increased slightly for better table context
OVERLAP = 150


# ========================
# CLEANING
# ========================
def html_table_to_markdown(table_soup):
    """Converts a BeautifulSoup table object to a Markdown table string."""
    rows = []
    trs = table_soup.find_all("tr")
    if not trs:
        return ""

    for i, tr in enumerate(trs):
        cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
        if not any(cells):
            continue
        
        # Format as markdown row
        rows.append("| " + " | ".join(cells) + " |")
        
        # Add separator after header row
        if i == 0 and len(cells) > 0:
            sep = "| " + " | ".join(["---"] * len(cells)) + " |"
            rows.append(sep)
            
    return "\n".join(rows)

def clean_text(text: str) -> str:
    # 1. Fix mojibake
    if HAS_FTFY:
        text = ftfy.fix_text(text)

    # 2. Parse HTML
    # Using 'lxml' which is robust
    soup = BeautifulSoup(text, "lxml")
    
    # Replace tables with markdown format
    for table in soup.find_all("table"):
        md_table = html_table_to_markdown(table)
        table.replace_with("\n\n" + md_table + "\n\n")

    # 3. Pull text but keep structure
    text = soup.get_text(separator="\n")

    # 4. CRITICAL: Aggressive Manual Tag Stripping (Fallback for malformed/partial HTML)
    # We use re.DOTALL to handle tags that span multiple lines
    # We run it in a loop to catch nested or broken tags
    for _ in range(3):
        text = re.sub(r'<[^>]+>', ' ', text, flags=re.DOTALL)

    # 5. Remove long noisy tokens (PDF artifacts)
    text = re.sub(r'\S{60,}', '', text)

    # 6. Decode entities and clean whitespace
    # Decode common HTML entities manually just in case
    text = text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = re.sub(r'&[a-zA-Z]+;', ' ', text)
    text = re.sub(r'&#\d+;', ' ', text)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', ' ', text)
    
    # Normalize spacing
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


# ========================
# CHUNKING
# ========================
def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP):
    sentences = re.split(r'(?<=[.?!])\s+', text)
    chunks = []
    current = []
    current_len = 0

    for sent in sentences:
        slen = len(sent)
        if current_len + slen > chunk_size and current:
            chunks.append(" ".join(current))
            overlap_buf, olen = [], 0
            for s in reversed(current):
                if olen + len(s) < overlap:
                    overlap_buf.insert(0, s)
                    olen += len(s)
                else:
                    break
            current = overlap_buf + [sent]
            current_len = olen + slen
        else:
            current.append(sent)
            current_len += slen

    if current:
        chunks.append(" ".join(current))

    return [c for c in chunks if len(c.strip()) > 30]


# ========================
# MAIN
# ========================
def main():
    print(f"Loading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    client = QdrantClient(path=QDRANT_PATH)

    try:
        client.delete_collection(COLLECTION_NAME)
        print("Old collection deleted.")
    except Exception:
        pass

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    print("Collection created.")

    md_files = list(KB_DIR.glob("*.md"))
    print(f"Reading {len(md_files)} files...")

    all_chunks = []
    for fpath in md_files:
        raw = fpath.read_text(encoding="utf-8", errors="replace")
        cleaned = clean_text(raw)
        chunks = chunk_text(cleaned)
        for chunk in chunks:
            all_chunks.append({"text": chunk, "source": fpath.name})

    print(f"Total chunks: {len(all_chunks)}")

    BATCH = 100
    for i in tqdm(range(0, len(all_chunks), BATCH), desc="Upserting"):
        batch = all_chunks[i : i + BATCH]
        texts = [c["text"] for c in batch]
        vectors = model.encode(texts, show_progress_bar=False).tolist()
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vec,
                payload={"text": c["text"], "source": c["source"]},
            )
            for c, vec in zip(batch, vectors)
        ]
        client.upsert(collection_name=COLLECTION_NAME, points=points)

    print(f"\n✅ {COLLECTION_NAME} COMPLETE")


if __name__ == "__main__":
    main()
