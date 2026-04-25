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
QDRANT_PATH = "../qdrant_storage"
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
def get_knowledge(query: str, domain: str, top_k: int = 5, threshold: float = 0.5) -> str:
    """Retrieves document chunks from the specified Qdrant domain."""
    collection_map = {
        "crop": "crop_kb",
        "finance": "finance_kb",
        "pest": "pests_kb"
    }
    
    collection_name = collection_map.get(domain.lower(), "crop_kb")
    vec = embed_model.encode(query).tolist()
    
    try:
        results = client.query_points(
            collection_name=collection_name,
            query=vec,
            limit=top_k,
        )
    except Exception as e:
        print(f"Failed to query {collection_name}: {e}")
        return ""

    hits = [p.payload.get("text", "").strip() for p in results.points if p.score >= threshold]
    
    if not hits:
        return ""
        
    # Format hits into a readable block for the LLM
    formatted_context = f"\n--- VERIFIED KNOWLEDGE: {domain.upper()} ---\n"
    formatted_context += "\n".join(hits)
    return formatted_context


