import json
from llama_cpp import Llama
from tools import get_agri_forecast, get_historical_rainfall,get_soil_details
import requests
from datetime import datetime, timedelta
import time


def run_api_tests(loc):
        try:
            with open('maharashtra_district_coords.json','r') as file:
                coords = json.load(file)

        except Exception as e:
            print(e)

    # for loc in coords.keys():
        lat,long = coords[loc]
        
        print(get_soil_details(lat,long+0.05))
        # time.sleep(10)
          
        
def run_sanity_check():
    print("\n--- 🛠️ PHASE 1: DIRECT FUNCTION TEST ---")
    
    # Test 1: Forecast (Nashik Coordinates)
    print("\n1. Testing Forecast API...")
    forecast = get_agri_forecast(19.99, 73.78)
    if "temp_max" in forecast:
        print("✅ Forecast API Success! Data received.")
    else:
        print("❌ Forecast API Failed:", forecast)

    # Test 2: History (Last Year)
    print("\n2. Testing Historical API...")
    last_year_start = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    last_year_end = (datetime.now() - timedelta(days=360)).strftime('%Y-%m-%d')
    
    history = get_historical_rainfall(19.99, 73.78, last_year_start, last_year_end)
    if "total_rainfall_mm" in history:
        print("✅ Historical API Success! Data received.")
    else:
        print("❌ Historical API Failed:", history)

def run_llm_test():
    print("\n--- 🧠 PHASE 2: LLM TOOL SELECTION TEST ---")
    
    model_path = "models/Qwen3-8B-Q6_K.gguf"  # <--- UPDATE THIS PATH
    
    try:
        print(f"Loading Model from {model_path}...")
        llm = Llama(
            model_path=model_path,
            n_ctx=4096,
            verbose=False
        )
    except Exception as e:
        print(f"❌ Could not load model: {e}")
        return

    # A "System Prompt" that teaches the model how to use tools
    system_prompt = """You are an Agronomist AI. You have access to the following tools:

1. get_agri_forecast(lat, lon): Use this for future weather, spraying advice, or irrigation planning.
2. get_historical_rainfall(lat, lon, start_date, end_date): Use this for past comparisons or yield analysis.

FORMAT INSTRUCTION:
If you need to use a tool, output ONLY a JSON object like this:
{ "tool": "tool_name", "args": { "arg1": value, "arg2": value } }

Do not output any thinking or explanations. Just the JSON."""

    # Test Queries
    queries = [
        ("Should I spray pesticide in Nashik tomorrow?", 19.99, 73.78),
        ("How much rain did we get last year in June?", 19.99, 73.78)
    ]

    for q_text, lat, lon in queries:
        print(f"\nUSER: {q_text}")
        
        output = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Location: {lat}, {lon}. Query: {q_text}"}
            ],
            temperature=0.1 # Low temp for precision
        )
        
        reply = output['choices'][0]['message']['content']
        print(f"🤖 LLM RAW OUTPUT: {reply}")
        
        # Verify if it picked the right tool
        try:
            # Clean up potential markdown blocks like ```json ... ```
            clean_reply = reply.replace("```json", "").replace("```", "").strip()
            tool_call = json.loads(clean_reply)
            
            if "spray" in q_text.lower() and tool_call.get("tool") == "get_agri_forecast":
                print("✅ PASSED: Correctly selected Forecast tool.")
            elif "last year" in q_text.lower() and tool_call.get("tool") == "get_historical_rainfall":
                print("✅ PASSED: Correctly selected Historical tool.")
            else:
                print("⚠️ WARNING: Logic might be incorrect.")
                
        except json.JSONDecodeError:
            print("❌ FAILED: LLM did not output valid JSON.")

if __name__ == "__main__":
    run_api_tests("Nagpur")
