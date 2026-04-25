import sys
import os
import json

sys.path.append(os.path.abspath(".."))

from router import IntentRouter
from llama_cpp import Llama

# -------------------------------
# 🔧 MODEL CONFIG (EDIT THIS ONLY)
# -------------------------------
MODELS = {
    "TinyLlama": "../models/tinyllama.gguf",
    # "Mistral": "../models/mistral.gguf",
    # "Llama2": "../models/llama2.gguf"
}

# -------------------------------
# LOAD DATASET
# -------------------------------
with open("routing_dataset.json") as f:
    data = json.load(f)

# -------------------------------
# EVALUATION FUNCTION
# -------------------------------
def evaluate_model(model_name, model_path):
    print(f"\n🚀 Evaluating: {model_name}")

    llm = Llama(
        model_path=model_path,
        n_ctx=2048,
        n_threads=4
    )

    router = IntentRouter(llm)

    correct = 0

    for item in data:
        question = item["question"]
        expected = item["expected_domain"]

        result = router.classify(question, debug=False)
        predicted_raw = result.get("primary_domain", "unknown").lower()

        # -------------------------------
        # NORMALIZATION
        # -------------------------------
        if "crop" in predicted_raw or "agriculture" in predicted_raw:
            predicted = "crop"
        elif "pest" in predicted_raw or "pesticide" in predicted_raw:
            predicted = "pest"
        elif "finance" in predicted_raw or "subsidy" in predicted_raw:
            predicted = "finance"
        else:
            predicted = "unknown"

        if predicted == expected:
            correct += 1

    accuracy = correct / len(data)
    print(f"✅ {model_name} Accuracy: {accuracy}")

    return accuracy


# -------------------------------
# RUN ALL MODELS
# -------------------------------
results = {}

for name, path in MODELS.items():
    try:
        results[name] = evaluate_model(name, path)
    except Exception as e:
        print(f"❌ Error with {name}: {e}")

# -------------------------------
# FINAL COMPARISON
# -------------------------------
print("\n=== MODEL COMPARISON ===")
for name, acc in results.items():
    print(f"{name}: {acc}")