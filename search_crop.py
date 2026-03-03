"""
search_crop.py - Retrieval-only semantic search for the crop knowledge base.
No LLM synthesis — returns top-k matching chunks with scores and sources.
Usage:
    python search_crop.py
    python search_crop.py "your query here"
"""
import sys
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# ========================
# CONFIG
# ========================
CROP_COLLECTION_NAME = "crop_kb"
FINANCE_COLLECTION_NAME = "finance_kb"
PEST_COLLECTION_NAME = "pest_kb"
MODEL_NAME = "all-MiniLM-L6-v2"
QDRANT_PATH = "qdrant_storage"
TOP_K = 5
SIM_THRESHOLD = 0.5  # minimum cosine similarity to include a result

# ========================
# LOAD (once)
# ========================
print("Loading embedding model...")
embed_model = SentenceTransformer(MODEL_NAME)
client = QdrantClient(path=QDRANT_PATH)
print("Ready.\n")


# ========================
# RETRIEVAL
# ========================
def search(query: str, top_k: int = TOP_K, threshold: float = SIM_THRESHOLD, collection_name: str = CROP_COLLECTION_NAME):
    """Return top-k chunks from crop_kb above the similarity threshold."""
    vec = embed_model.encode(query).tolist()
    results = client.query_points(
        collection_name=collection_name,
        query=vec,
        limit=top_k,
    )
    hits = [
        {
            "score": round(p.score, 4),
            "source": p.payload.get("source", "unknown"),
            "text": p.payload.get("text", "").strip(),
        }
        for p in results.points
        if p.score >= threshold
    ]
    return hits


def display(hits, query: str):
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"Found {len(hits)} relevant chunk(s)")
    print('='*60)
    if not hits:
        print("No results above similarity threshold.")
        return
    for i, h in enumerate(hits, 1):
        print(f"\n[{i}] Score: {h['score']}  |  Source: {h['source']}")
        print("-" * 50)
        print(h["text"])
    print(f"\n{'='*60}\n")


# ========================
# MAIN
# ========================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Single query from command line
        q = " ".join(sys.argv[1:])
        display(search(q), q)
    else:
        # Interactive mode
        print("Crop RAG - Retrieval Mode. Type 'exit' to quit.\n")
        while True:
            try:
                q = input("Query: ").strip()
                if q.lower() in ("exit", "quit", ""):
                    break
                display(search(q), q)
            except KeyboardInterrupt:
                break
