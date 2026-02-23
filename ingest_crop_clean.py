import os
import re
from uuid import uuid4
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

KB_FOLDER = "kb/kb_crop_clean"
COLLECTION_NAME = "crop_kb"
QDRANT_PATH = "qdrant_storage"
MODEL_NAME = "all-MiniLM-L6-v2"

print("Loading model...")
model = SentenceTransformer(MODEL_NAME)
embedding_size = len(model.encode("test"))

client = QdrantClient(path=QDRANT_PATH)

# delete old collection if exists
collections = [c.name for c in client.get_collections().collections]
if COLLECTION_NAME in collections:
    client.delete_collection(collection_name=COLLECTION_NAME)

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=embedding_size, distance=Distance.COSINE)
)

print("Collection created.")

def chunk_text(text, chunk_size=500):
    paragraphs = text.split(". ")
    chunks = []
    current = ""

    for p in paragraphs:
        if len(current) + len(p) < chunk_size:
            current += p + ". "
        else:
            chunks.append(current.strip())
            current = p + ". "

    if current:
        chunks.append(current.strip())

    return chunks

points = []

for file in os.listdir(KB_FOLDER):
    if file.endswith(".md"):
        with open(os.path.join(KB_FOLDER, file), "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)

        for chunk in chunks:
            vector = model.encode(chunk).tolist()

            points.append(
                PointStruct(
                    id=str(uuid4()),
                    vector=vector,
                    payload={
                        "text": chunk,
                        "source": file
                    }
                )
            )

print("Uploading...")
for i in tqdm(range(0, len(points), 100)):
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points[i:i+100]
    )

print("✅ Crop KB rebuilt cleanly!")
