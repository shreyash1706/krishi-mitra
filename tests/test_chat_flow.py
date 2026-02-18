import requests
import time

BASE_URL = "http://127.0.0.1:8000"
USER_ID = "farmer_test_99"

def chat(query: str, session_id: int = None):
    print(f"\n🧑‍🌾 User: {query}")
    payload = {"user_id": USER_ID, "query": query}
    if session_id:
        payload["session_id"] = session_id

    start_time = time.time()
    response = requests.post(f"{BASE_URL}/chat", json=payload).json()
    
    print(f"⏱️  Time: {time.time() - start_time:.1f}s | 🧭 Agent: {response['agent'].upper()}")
    print(f"🤖 Krishi Mitra: {response['reply']}")
    print("-" * 60)
    
    return response["session_id"]

def run_chat_flow():
    print("🚀 Starting Conversational Memory & Tool Test...\n")
    
    # Turn 1: Forces the LLM to use the Market Tool
    session_id = chat("What is the market price for Cotton in Jalgaon?")
    
    # Turn 2: Tests MEMORY. 
    # Notice we don't mention 'Cotton' or 'Jalgaon'. The LLM must look at the history, 
    # realize the context, and answer using the data it got from the tool in Turn 1.
    session_id = chat("Is that a good price compared to the state benchmark?", session_id)
    
    # Turn 3: Forces the LLM to use the Weather Tool
    session_id = chat("Okay. I want to spray pesticides on my cotton today. My farm is at lat 21.0, lon 75.5. Check the weather.", session_id)
    
    # Turn 4: Tests ROUTER and MEMORY together. 
    # It should switch to the Pest Agent, but remember the weather data from Turn 3 to give advice.
    session_id = chat("Based on that weather, is it safe to spray right now?", session_id)

if __name__ == "__main__":
    run_chat_flow()