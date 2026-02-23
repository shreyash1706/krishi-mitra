## tests/test_web_llm.py
import requests
import time

BASE_URL = "http://127.0.0.1:8000"
USER_ID = "farmer_web_tester"

def chat(query: str):
    print(f"\n🧑‍🌾 User: {query}")
    payload = {"user_id": USER_ID, "query": query}

    start_time = time.time()
    try:
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        response.raise_for_status()
        data = response.json()
        
        print(f"⏱️  Time: {time.time() - start_time:.1f}s | 🧭 Agent: {data['agent'].upper()}")
        print(f"🤖 Krishi Mitra:\n{data['reply']}")
        print("-" * 60)
    except Exception as e:
        print(f"❌ API Error: {e}")

def run_llm_test():
    print("🚀 Starting LLM Web Search Integration Test...\n")
    
    # This should trigger the Finance Agent to use the Web Search tool
    # chat("Are there any new announcements for the PM Kisan Samman Nidhi scheme in the news recently?")
    
    # This should trigger the Pest/Crop Agent to check recent events
    chat("Has there been any news about pink bollworm attacks in Maharashtra this month?")

if __name__ == "__main__":
    # Make sure your FastAPI server (uvicorn main:app) is running in another terminal!
    run_llm_test()