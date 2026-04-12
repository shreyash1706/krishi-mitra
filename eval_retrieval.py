import json
import os
import time
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# Initialization
print("Loading model 'all-MiniLM-L6-v2'...")
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Connecting to Qdrant...")
client = QdrantClient(path="qdrant_storage")

def evaluate_retrieval():
    queries_file = "eval_queries.json"
    if not os.path.exists(queries_file):
        print(f"Error: {queries_file} not found.")
        return

    with open(queries_file, 'r') as f:
        eval_data = json.load(f)

    results = []
    
    # Metrics
    metrics = {
        "overall": {"count": 0, "r1": 0, "r3": 0, "r5": 0, "mrr_sum": 0.0},
        "crop_kb": {"count": 0, "r1": 0, "r3": 0, "r5": 0, "mrr_sum": 0.0},
        "pests_kb": {"count": 0, "r1": 0, "r3": 0, "r5": 0, "mrr_sum": 0.0},
        "finance_kb": {"count": 0, "r1": 0, "r3": 0, "r5": 0, "mrr_sum": 0.0}
    }

    print("\nStarting evaluation...")
    print("-" * 80)
    print(f"{'ID':<4} | {'Collection':<12} | {'MRR':<5} | {'R@1':<3} | {'R@3':<3} | {'R@5':<3} | Query")
    print("-" * 80)

    for item in eval_data:
        q_id = item["id"]
        query = item["query"]
        collection_name = item["collection"]
        expected_sources = item["expected_sources"]

        # Search
        query_vector = model.encode(query).tolist()
        search_result = client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=5
        )

        retrieved_sources = []
        for hit in search_result.points:
            source = hit.payload.get("source", "Unknown")
            # Usually the source could be an absolute path or filename. 
            # From previous ingest scripts, the source is the base filename like "agriculture_maha.md"
            base_source = os.path.basename(source)
            retrieved_sources.append(base_source)

        # Calculate metrics for this query
        rank = -1
        for i, src in enumerate(retrieved_sources):
            if any(exp in src for exp in expected_sources):
                rank = i + 1
                break
        
        r1 = 1 if rank == 1 else 0
        r3 = 1 if 1 <= rank <= 3 else 0
        r5 = 1 if 1 <= rank <= 5 else 0
        mrr = 1.0 / rank if rank > 0 else 0.0

        # Update metrics
        col = metrics[collection_name]
        over = metrics["overall"]
        
        for m in (col, over):
            m["count"] += 1
            m["r1"] += r1
            m["r3"] += r3
            m["r5"] += r5
            m["mrr_sum"] += mrr

        # Save query result
        results.append({
            "id": q_id,
            "query": query,
            "collection": collection_name,
            "expected_sources": expected_sources,
            "retrieved_sources": retrieved_sources,
            "rank": rank,
            "metrics": {
                "Recall@1": r1,
                "Recall@3": r3,
                "Recall@5": r5,
                "MRR": round(mrr, 3)
            }
        })
        
        # Print row
        mrr_str = f"{mrr:.2f}"
        print(f"{q_id:<4} | {collection_name:<12} | {mrr_str:<5} | {r1:<3} | {r3:<3} | {r5:<3} | {query[:35]}...")

    print("-" * 80)
    
    # Calculate final averages
    final_metrics = {}
    for key, val in metrics.items():
        count = val["count"]
        if count == 0:
            continue
        final_metrics[key] = {
            "count": count,
            "Recall@1": round(val["r1"] / count, 3),
            "Recall@3": round(val["r3"] / count, 3),
            "Recall@5": round(val["r5"] / count, 3),
            "MRR": round(val["mrr_sum"] / count, 3)
        }

    # Print summary
    print("\nEvaluation Summary:")
    print("=" * 60)
    for key, fm in final_metrics.items():
        print(f"--- {key.upper()} (n={fm['count']}) ---")
        print(f" Recall@1: {fm['Recall@1']*100:.1f}%")
        print(f" Recall@3: {fm['Recall@3']*100:.1f}%")
        print(f" Recall@5: {fm['Recall@5']*100:.1f}%")
        print(f" MRR:      {fm['MRR']:.3f}\n")

    # Write to file
    output_file = "eval_results.json"
    output_data = {
        "summary": final_metrics,
        "details": results
    }
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=4)
    print(f"Detailed results saved to {output_file}")

if __name__ == "__main__":
    evaluate_retrieval()
