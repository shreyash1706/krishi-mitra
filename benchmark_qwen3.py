import requests
import time

url = "http://127.0.0.1:8000/chat"
test_queries = [
    "What are the best soil conditions for growing cotton?",
    "How do I treat powdery mildew on my tomato plants?",
    "What is the current market price of wheat?",
    "Can you give me a financial plan for buying a tractor?"
]

print("Starting Qwen3-8B Server Latency Benchmark...")
print("-" * 50)

results = []

for idx, q in enumerate(test_queries):
    print(f"[{idx+1}/{len(test_queries)}] Query: '{q}'")
    start_t = time.time()
    try:
        req = {
            "user_id": "eval_bot",
            "query": q,
            "session_id": 999
        }
        res = requests.post(url, json=req, timeout=120)
        end_t = time.time()
        
        if res.status_code == 200:
            data = res.json()
            timing = data.get("timing", {})
            total_s = timing.get("total_s", end_t - start_t)
            agent_s = timing.get("agent_s", 0)
            target = data.get("agent", "unknown")
            answer_len = len(data.get("reply", ""))
            
            print(f"  -> Success! Routed to: {target}")
            print(f"  -> Router Time : {timing.get('router_s', 0):.2f}s")
            print(f"  -> Agent Time  : {agent_s:.2f}s")
            print(f"  -> Total Latency: {total_s:.2f}s")
            print(f"  -> Response Len: {answer_len} chars\n")
            
            results.append(total_s)
        else:
            print(f"  -> Failed (HTTP {res.status_code}): {res.text}\n")
    except Exception as e:
        print(f"  -> Error: {e}\n")

if results:
    avg = sum(results) / len(results)
    print("-" * 50)
    print(f"AVERAGE LATENCY (End-to-End): {avg:.2f} seconds")
    print(f"GPU Offloading: Active (4 layers)")
    print(f"KV Cache: 8-bit Quantized (q8_0)")
    print("-" * 50)
