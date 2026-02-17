import requests

# The URL where your FastAPI server is listening
BASE_URL = "http://127.0.0.1:8000/chat"

print("--- TEST 1: New Chat (Testing Router & Profile Injection) ---")
# Notice we do NOT pass a session_id here. 
# This forces the Router to classify the intent and create a new tab.
payload_1 = {
    "user_id": "farmer_001",
    "query": "Hello! What crops are most suitable for my current soil type?"
}

response_1 = requests.post(BASE_URL, json=payload_1)
data_1 = response_1.json()

print(f"Agent Used: {data_1['agent']}")
print(f"Session ID Created: {data_1['session_id']}")
print(f"Bot Reply:\n{data_1['reply']}\n")


print("--- TEST 2: Follow-up Chat (Testing Memory & Tabs) ---")
# Extract the newly created session ID
session_id = data_1.get("session_id")

# We pass the session_id this time.
# The model should remember what crops it just suggested.
payload_2 = {
    "user_id": "farmer_001",
    "query": "When is the best time to sow the first crop you mentioned?",
    "session_id": session_id 
}

response_2 = requests.post(BASE_URL, json=payload_2)
data_2 = response_2.json()

print(f"Agent Used: {data_2['agent']}")
print(f"Session ID Used: {data_2['session_id']}")
print(f"Bot Reply:\n{data_2['reply']}\n")