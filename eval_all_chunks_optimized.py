import json
import random
import re
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from tqdm import tqdm

print("Loading embedding model 'all-MiniLM-L6-v2'...")
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Connecting to Qdrant...")
client = QdrantClient(path="qdrant_storage")

collections = ["crop_kb", "pests_kb", "finance_kb"]

def get_query_from_text(text):
    """
    Extracts a more robust, longer phrase to ensure semantic uniqueness.
    Avoids tiny generic chunks like "Table 1 shows".
    """
    # Clean up formatting a bit for the query
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    words = clean_text.split()
    
    # We want a 25-30 word chunk to guarantee unique semantic embedding matching
    # rather than just 10 words which could overlap with 50 other table headers.
    target_len = min(len(words), random.randint(25, 30))
    if len(words) <= target_len:
        return text
        
    start_idx = random.randint(0, len(words) - target_len)
    query_words = words[start_idx:start_idx+target_len]
    return " ".join(query_words)

results = {
    "total_evaluated": 0,
    "success_at_1": 0,
    "success_at_5": 0,
    "success_at_10": 0,
    "failed": []
}

for coll in collections:
    print(f"\nEvaluating collection: {coll}")
    
    count_res = client.count(collection_name=coll)
    total_chunks = count_res.count
    
    offset = None
    with tqdm(total=total_chunks, desc=f"Evaluating {coll}") as pbar:
        while True:
            records, offset = client.scroll(
                collection_name=coll,
                limit=100,
                offset=offset,
                with_payload=True,
                with_vectors=False
            )
            
            for r in records:
                target_id = r.id
                text = r.payload.get("text", "")
                
                # Skip extremely tiny or empty chunks
                if len(text.strip().split()) < 10:
                    pbar.update(1)
                    continue
                    
                # Generate a strong synthetic query
                query = get_query_from_text(text)
                
                # Encode and search, expanding Top-K slightly handling thousands of identical chunks
                vec = model.encode(query).tolist()
                search_result = client.query_points(
                    collection_name=coll,
                    query=vec,
                    limit=10 
                )
                
                retrieved_ids = [hit.id for hit in search_result.points]
                
                results["total_evaluated"] += 1
                
                if target_id in retrieved_ids:
                    results["success_at_10"] += 1
                    rank = retrieved_ids.index(target_id)
                    if rank < 5:
                        results["success_at_5"] += 1
                    if rank == 0:
                        results["success_at_1"] += 1
                else:
                    results["failed"].append({
                        "collection": coll,
                        "target_id": target_id,
                        "synthetic_query": query,
                        "retrieved_ids": retrieved_ids
                    })
                
                pbar.update(1)
                
            if offset is None:
                break

print("\n" + "="*50)
print("CHUNK-LEVEL EVALUATION (OPTIMIZED)")
print("="*50)
print(f"Total Valid Chunks Evaluated: {results['total_evaluated']}")
print(f"Recall@1 (Exact Chunk Match): {results['success_at_1']} ({(results['success_at_1']/results['total_evaluated'])*100:.2f}%)")
print(f"Recall@5 (Exact Chunk Match): {results['success_at_5']} ({(results['success_at_5']/results['total_evaluated'])*100:.2f}%)")
print(f"Recall@10 (Exact Chunk Match): {results['success_at_10']} ({(results['success_at_10']/results['total_evaluated'])*100:.2f}%)")
