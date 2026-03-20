import json
import time
import sys 
import os
# Get the absolute path of the current directory's parent
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from router import IntentRouter
from llama_cpp import Llama
# Import your router from wherever you saved it
# from router import IntentRouter 

def evaluate_router(llm_instance):
    router = IntentRouter(llm_instance)
    
    # 1. Define the Test Suite
    # Mix of simple queries and complex, multi-domain problems
    test_cases = [
        {
            "id": 1,
            "query": "When is the exact time to sow Kharif maize in Maharashtra?",
            "expected_domains": ["crop"],
            "expected_think": False
        },
        {
            "id": 2,
            "query": "How do I apply for the PM-KISAN subsidy online?",
            "expected_domains": ["finance"],
            "expected_think": False
        },
        {
            "id": 3,
            "query": "My tomatoes have black spots on the bottom and the leaves are curling. Should I pull them out or spray something?",
            "expected_domains": ["pest", "crop"],
            "expected_think": True
        },
        {
            "id": 4,
            "query": "Onion prices are crashing at the Lasalgaon mandi. Is there any government scheme to cover my cold storage costs?",
            "expected_domains": ["market", "finance"],
            "expected_think": True
        },
        {
            "id": 5,
            "query": "Which crops should I select considering our neighbors have an aphid problem?",
            "expected_domains": ["crop", "pest"],
            "expected_think": True
        }
    ]

    print("🚜 Starting Router Evaluation...\n" + "="*50)
    
    total_passed = 0
    
    # 2. Run the Evaluation Loop
    for test in test_cases:
        print(f"\n📝 Test {test['id']}: {test['query']}")
        
        start_time = time.time()
        
        # Call your router
        result = router.classify(test['query'], debug=True)
        
        latency = time.time() - start_time
        
        # Extract the results
        generated_plans = result.get("search_plans", [])
        generated_domains = [plan.get("domain") for plan in generated_plans]
        generated_think = result.get("think")
        
        # 3. Grade the output
        # Check if all expected domains were identified
        domains_passed = all(domain in generated_domains for domain in test['expected_domains'])
        think_passed = (generated_think == test['expected_think'])
        
        if domains_passed and think_passed:
            print("✅ PASS")
            total_passed += 1
        else:
            print("❌ FAIL")
            print(f"   Expected Domains: {test['expected_domains']} | Got: {generated_domains}")
            print(f"   Expected Think: {test['expected_think']} | Got: {generated_think}")
            
        # 4. Print the HyDE Queries for Manual Review
        print(f"⏱️  Latency: {latency:.2f}s")
        print("🔍 Generated HyDE Queries:")
        for plan in generated_plans:
            print(f"   [{plan.get('domain').upper()}] -> {plan.get('search_query')}")
            
        print("-" * 50)

    # 5. Final Score
    print(f"\n📊 Final Score: {total_passed} / {len(test_cases)} Passed")
    print("Review the 'Generated HyDE Queries' above to ensure they are highly specific and not just copying the user prompt.")

# ==========================================
# How to run it:
# ==========================================
if __name__ == "__main__":
    # Initialize your actual LLM wrapper here
    my_llm =  Llama(
    model_path="/home/master-shreyash/Documents/krishi_mitra/models/Qwen3-14B-Q4_K_M.gguf",
    n_gpu_layers=0,
    n_ctx=2048,
    n_threads=6,
    verbose=False
)
    evaluate_router(my_llm)