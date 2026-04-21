import sys
import os
import json
from config import MODEL_PATH, MODE
sys.path.append(os.path.abspath(".."))

from llm_loader import load_llm, generate_answer
from evaluator import *

# Load model
if MODE == "online":
    tokenizer, model = load_llm()
# Load dataset
with open("dataset.json") as f:
    data = json.load(f)

precision_scores = []
recall_scores = []
routing_scores = []
faithfulness_scores = []

for i, item in enumerate(data):
    question = item["question"]
    
    expected_answer = item.get("expected_answer", "")
    generated_answer = item.get("generated_answer", "")
    retrieved_context_raw = item.get("retrieved_context", "")
    router_plans = item.get("router_plans", [])

    print(f"\n🔍 Question: {question}")

    # -------------------------------
    # 1. CONTEXT
    # -------------------------------
    retrieved_context = [retrieved_context_raw.lower()]

    # -------------------------------
    # 2. PRECISION & RECALL
    # -------------------------------
    precision_scores.append(context_precision(retrieved_context, [expected_answer.lower()]))
    recall_scores.append(context_recall(retrieved_context, [expected_answer.lower()]))

    # -------------------------------
    # 3. ROUTING
    # -------------------------------
    if router_plans:
        predicted_domain = router_plans[0]["domain"]
    else:
        predicted_domain = "unknown"

    if "pest" in question.lower():
        true_domain = "pest"
    elif "loan" in question.lower() or "cost" in question.lower():
        true_domain = "finance"
    else:
        true_domain = "crop"

    routing_scores.append(routing_accuracy(predicted_domain, true_domain))

    # -------------------------------
    # 4. GENERATE / USE ANSWER  
    # -------------------------------
    if MODE == "online":
        if 'model' not in globals():
            tokenizer, model = load_llm()
        
        prompt = f"Context: {retrieved_context}\nQuestion: {question}"
        answer = generate_answer(tokenizer, model, prompt)

    else:
        answer = generated_answer
    if i < 3:
      print("\n🧠 Generated Answer:", answer[:200])
      print("📚 Retrieved Context:", retrieved_context[0][:200])
      print("✅ Expected Answer:", expected_answer[:200])
        
    # -------------------------------
    # 5. FAITHFULNESS 
    # -------------------------------
    faithfulness_scores.append(
        faithfulness(answer, retrieved_context)
    )

# Final Results
print("\n=== FINAL METRICS ===")
print("Context Precision:", sum(precision_scores)/len(precision_scores))
print("Context Recall:", sum(recall_scores)/len(recall_scores))
print("Routing Accuracy:", sum(routing_scores)/len(routing_scores))
print("Faithfulness:", sum(faithfulness_scores)/len(faithfulness_scores))