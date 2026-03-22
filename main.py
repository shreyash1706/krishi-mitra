from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agent import BaseAgent
from router import IntentRouter
from typing import Optional
import sqlite3
import time
import logging
import json
from agri_tools import get_coords
from search import get_knowledge
import json


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("krishi")

import requests

app = FastAPI(title="Krishi Mitra API")

class LlamaServerClient:
    """Proxy class to talk to the standalone llama.cpp server API"""
    def __call__(self, *args, **kwargs):
        return self.create_chat_completion(*args, **kwargs)
        
    def create_chat_completion(self, messages, tools=None, tool_choice=None, temperature=0.7, max_tokens=None, response_format=None, stream=False):
        payload = {
            "messages": messages,
            "temperature": temperature,
            "frequency_penalty": 1.1,
            "presence_penalty": 0.8,
            "top_p": 0.95
        }
        if tools: 
            payload["tools"] = tools
        if tool_choice: 
            payload["tool_choice"] = tool_choice
        if max_tokens: 
            payload["max_tokens"] = max_tokens
        if response_format: 
            payload["response_format"] = response_format
        if stream:
            payload["stream"] = True
            
        try:
            r = requests.post("http://127.0.0.1:8080/v1/chat/completions", json=payload, stream=stream)
            r.raise_for_status()
            
            if stream:
                def stream_gen():
                    for line in r.iter_lines():
                        if line:
                            line = line.decode('utf-8')
                            if line.startswith("data: "):
                                data_str = line[6:]
                                if data_str == "[DONE]":
                                    break
                                try:
                                    yield json.loads(data_str)
                                except json.JSONDecodeError:
                                    pass
                return stream_gen()
            else:
                resp_json = r.json()
                # Qwen3/Reasoning models might separate the thought
                choice = resp_json.get('choices', [{}])[0]
                msg = choice.get('message', {})
                if not msg.get('content') and msg.get('reasoning_content'):
                    msg['content'] = f"<think>{msg['reasoning_content']}</think>"
                elif msg.get('reasoning_content'):
                    # Prepend if both exist
                    msg['content'] = f"<think>{msg['reasoning_content']}</think>\n{msg['content']}"
                return resp_json
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling local llama.cpp server: {e}")
            if stream:
                def error_gen():
                    yield {"choices": [{"delta": {"content": "Error: Local LLM server unavailable."}}]}
                return error_gen()
            return {"choices": [{"message": {"content": "Error: Local LLM server unavailable."}}]}

# model_path = "models/Qwen3-8B-Q4_K_M.gguf" (now loaded by server executable)
SHARED_LLM = LlamaServerClient()

router = IntentRouter(SHARED_LLM)

# --------------------------------------------------
# AGENTS
# --------------------------------------------------

AGENTS = {
    "crop": BaseAgent(
        agent_mode="Crop Planner",
        system_prompt=(
            "You are Krishi Mitra, an expert Agronomist. "
            "ALWAYS use the 'get_soil_details' tool before recommending crops. "
            "Use 'get_agri_forecast' before advising on irrigation. "
            "CRITICAL: Provide direct, complete, and practical answers. "
            "Do NOT ask follow-up questions. Do NOT ask the user for more information."
        ),
    ),
    "pest": BaseAgent(
        agent_mode="Pest & Disease",
        system_prompt=(
            "You are Krishi Mitra, a Plant Pathologist. "
            "Use 'get_agri_forecast' before diagnosing fungal issues. "
            "CRITICAL: Provide direct, complete, and practical answers. "
            "Do NOT ask follow-up questions. Do NOT ask the user for more information."
        ),
    ),
    "market": BaseAgent(
        agent_mode="Market Expert",
        system_prompt=(
            "You are Krishi Mitra, a Market Analyst. "
            "ALWAYS use 'get_market_price' before answering. "
            "CRITICAL: Provide direct, complete, and practical answers. "
            "Do NOT ask follow-up questions. Do NOT ask the user for more information."
        ),
    ),
    "finance": BaseAgent(
        agent_mode="Finance Advisor",
        system_prompt=(
            "You are Krishi Mitra, a Banking Consultant for Farmers. "
            "CRITICAL: Provide direct, complete, and practical answers. "
            "Do NOT ask follow-up questions. Do NOT ask the user for more information."
        ),
    )
}

for agent in AGENTS.values():
    agent.set_llm(SHARED_LLM)

# --------------------------------------------------
# REQUEST MODEL (UPDATED)
# --------------------------------------------------

class ChatRequest(BaseModel):
    user_id: str
    query: str
    session_id: Optional[int] = None
    output_language: Optional[str] = "English"

class UserRequest(BaseModel):
    user_id: str
    name: str
    district: str
    village: Optional[str] = None
# --------------------------------------------------
# CHAT ENDPOINT
# --------------------------------------------------
@app.post("/register")
async def register_endpoint(req: UserRequest):
    
    lat, lon = 0.0, 0.0
    
    if req.village=="":
        coords = get_coords(req.village, req.district)
        if coords: lat, lon = coords
    else:
        try:
            with open("maharashtra_districts_coords.json", "r") as f:
                district_coords = json.load(f)
            
            # The JSON stores a list: [latitude, longitude]
            coords_list = district_coords.get(req.district)   
            if coords_list:
                lat = coords_list[0]
                lon = coords_list[1]
                
        except Exception as e:
            print(f"Error loading district coords: {e}")
            raise HTTPException(status_code=400, detail=f"Could not resolve coordinates: {e}")  # ✅ Don't silently continue

    print(lat, lon)
    conn = sqlite3.connect("krishi.db")
    c = conn.cursor()

    c.execute("SELECT user_id FROM farmers WHERE user_id = ?", (req.user_id,))
    farmer = c.fetchone()

    if not farmer:
        # Insert new farmer
        c.execute("""
            INSERT INTO farmers (user_id, name, village, district,lat,lon)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (req.user_id, req.name, req.village, req.district, lat, lon))
    else:
        # Update farmer details if they changed
        c.execute("""
            UPDATE farmers
            SET name = ?, village = ?, district = ?, lat = ?, lon = ?
            WHERE user_id = ?
        """, (req.name, req.village, req.district, lat, lon, req.user_id))

    conn.commit()
    conn.close()
    return {"status": "success", "message": "User registered/updated"} 

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    total_start = time.time()
    
    # 1. RUN ROUTER EVERY TIME (Fast & Cheap)
    router_start = time.time()
    decision = router.classify(req.query, debug=True)
    router_time = time.time() - router_start
    logger.info(f"⏱️ Router: {router_time:.2f}s")
    
    target = decision.get("agent", "crop")
    should_think = True # Force deep-reasoning ON for all queries to ensure UI thought-block guarantees
    search_plans = decision.get("search_plans", [])
    primary_domain = decision.get("primary_domain", "crop")

    compiled_knowledge = ""

    # Execute the HyDE queries against their respective databases
    for plan in search_plans:
        search_q = plan.get("search_query", plan.get("query", ""))
        print(f"\n[RAG DEBUG] Attempting to retrieve knowledge for domain '{plan.get('domain')}' using query: '{search_q}'...")
        knowledge = get_knowledge(search_q, plan.get("domain", "crop"))
        if knowledge:
            print(f"[RAG DEBUG] Successfully retrieved {len(knowledge)} chars of verified data!")
            compiled_knowledge += knowledge + "\n"
        else:
            print(f"[RAG DEBUG] No confident semantic matches found.")
    
    # 2. SESSION MANAGEMENT
    if not req.session_id:
        # Brand new chat
        conn = sqlite3.connect("krishi.db")
        c = conn.cursor()
        c.execute("INSERT INTO sessions (user_id, agent_mode, title) VALUES (?, ?, ?)", 
                  (req.user_id, primary_domain, req.query[:31]))
        req.session_id = c.lastrowid
        conn.commit()
        conn.close()
    
    # 3. DISPATCH
    active_agent = AGENTS.get(target, AGENTS["crop"])
    
    final_query = req.query
    if compiled_knowledge.strip():
        # Append retrieved knowledge explicitly
        print(f"[RAG DEBUG] Knowledge appended to model context successfully.")
        final_query += f"\n\n[RETRIEVED KNOWLEDGE BASE RESULTS]\n{compiled_knowledge.strip()}"
        
    if req.output_language and req.output_language != "English":
        print(f"[ROUTER DEBUG] Enforcing final model response translation natively to {req.output_language}")
        final_query += f"\n\n[CRITICAL INSTRUCTION: You MUST translate your thought process and final response entirely into the {req.output_language} language. Keep the agricultural and technical terms accurate.]"

    # Return the real-time generator
    generator = active_agent.run(final_query, req.session_id, req.user_id, should_think)
    
    return StreamingResponse(generator, media_type="application/x-ndjson")
