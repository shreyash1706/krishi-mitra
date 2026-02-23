from qdrant_client import QdrantClient

client = QdrantClient(path="qdrant_storage")
collections = ["crop_kb", "finance_kb", "pests_kb"]

for col in collections:
    try:
        count = client.get_collection(col).points_count
        print(f"Collection {col}: {count} points")
    except Exception as e:
        print(f"Collection {col} failed: {e}")
