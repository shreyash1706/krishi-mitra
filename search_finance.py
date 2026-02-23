"""
search_finance.py - Retrieval-only semantic search for the finance knowledge base.
No LLM synthesis — returns top-k matching chunks with scores and sources.
Usage:
    python search_finance.py
    python search_finance.py "your query here"
"""
import sys
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

COLLECTION_NAME = "finance_kb"
MODEL_NAME = "all-MiniLM-L6-v2"
QDRANT_PATH = "qdrant_storage"
TOP_K = 5
SIM_THRESHOLD = 0.35

print("Loading embedding model...")
embed_model = SentenceTransformer(MODEL_NAME)
client = QdrantClient(path=QDRANT_PATH)
print("Ready.\n")


def search(query: str, top_k: int = TOP_K, threshold: float = SIM_THRESHOLD):
    vec = embed_model.encode(query).tolist()
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vec,
        limit=top_k,
    )
    return [
        {
            "score": round(p.score, 4),
            "source": p.payload.get("source", "unknown"),
            "text": p.payload.get("text", "").strip(),
        }
        for p in results.points
        if p.score >= threshold
    ]


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


if __name__ == "__main__":
    if len(sys.argv) > 1:
        q = " ".join(sys.argv[1:])
        display(search(q), q)
    else:
        print("Finance RAG - Retrieval Mode. Type 'exit' to quit.\n")
        while True:
            try:
                q = input("Query: ").strip()
                if q.lower() in ("exit", "quit", ""):
                    break
                display(search(q), q)
            except KeyboardInterrupt:
                break
