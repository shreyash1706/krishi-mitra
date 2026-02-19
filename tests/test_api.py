import requests
import time

# Ensure your FastAPI server is running on this port (e.g., uvicorn main:app --reload)
BASE_URL = "http://127.0.0.1:8000"
USER_ID = "test_farmer_001"

def send_message(query: str, session_id: int = None):
    """Sends a message to the API and prints the response."""
    print(f"\n🧑‍🌾 User: {query}")
    
    payload = {
        "user_id": USER_ID,
        "query": query
    }
    if session_id is not None:
        payload["session_id"] = session_id

    start_time = time.time()
    
    try:
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        response.raise_for_status() # Raise an exception for bad status codes
        
        data = response.json()
        end_time = time.time()
        
        agent_used = data.get("agent", "unknown")
        reply = data.get("reply", "")
        new_session_id = data.get("session_id")
        
        print(f"⏱️  Time taken: {end_time - start_time:.2f}s")
        print(f"🧭 Routed to Agent: [{agent_used.upper()}]")
        print(f"🤖 Krishi Mitra:\n{reply}")
        print("-" * 50)
        
        return new_session_id
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to the API. Is your FastAPI server running?")
        exit(1)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        if 'response' in locals():
            print(response.text)
        return session_id

def run_conversational_test():
    print("🚀 Starting Krishi Mitra API Integration Test...\n")
    session_id = None

    # --- TEST 1: Soil Tool & Crop Agent ---
    # We provide exact lat/lon so the LLM doesn't have to guess.
    query_1 = "I am planning to farm at lat 19.08, lon 76.97. Can you check the soil details there and tell me what is good to grow?"
    session_id = send_message(query_1, session_id)

    # --- TEST 2: Weather Tool (Memory Check) ---
    """   # Testing if it remembers the location from the previous turn OR uses the one provided.
    query_2 = "What is the 7-day weather forecast looking like for my farm at lat 18.52, lon 73.85? Will it rain?"
    session_id = send_message(query_2, session_id)

    # --- TEST 3: Market Tool & Routing switch ---
    # Testing if the router successfully switches from Crop/Weather to Market.
    query_3 = "I also have some onion harvested. What is the current market price for onion in Lasalgaon?"
    session_id = send_message(query_3, session_id)

    # --- TEST 4: Finance Agent (No Tool / Pure LLM Knowledge) ---
    # Testing if it routes to Finance and maintains conversation flow.
    query_4 = "Are there any government subsidies available for buying a tractor?"
    session_id = send_message(query_4, session_id)

    # --- TEST 5: Historical Rainfall Tool ---
    query_5 = "Can you check the historical rainfall at lat 19.99, lon 73.78 between 2023-06-01 and 2023-08-31?"
    session_id = send_message(query_5, session_id)

    print("\n✅ API Testing Complete!")
    """
if __name__ == "__main__":
    # Make sure you have installed requests: pip install requests
    run_conversational_test()