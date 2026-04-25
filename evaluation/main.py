import sys
import os
import json

sys.path.append(os.path.abspath(".."))

from search import get_knowledge
from evaluator import context_precision, context_recall

# Load dataset
with open("retrieval_dataset.json") as f:
    data = json.load(f)

precision_scores = []
recall_scores = []

for item in data:
    question = item["question"]
    expected_context = item["expected_context"]

    print(f"\n🔍 Question: {question}")

    # -------------------------------
    # 1. REAL RETRIEVAL (FIXED)
    # -------------------------------
    retrieved_text = get_knowledge(question, domain="crop")
    retrieved_context = [retrieved_text.lower()]

    # -------------------------------
    # 2. METRICS
    # -------------------------------
    precision = context_precision(retrieved_context, expected_context)
    recall = context_recall(retrieved_context, expected_context)

    precision_scores.append(precision)
    recall_scores.append(recall)

    print("Precision:", precision)
    print("Recall:", recall)

# Final Results
print("\n=== FINAL RETRIEVAL METRICS ===")
print("Average Precision:", sum(precision_scores)/len(precision_scores))
print("Average Recall:", sum(recall_scores)/len(recall_scores))