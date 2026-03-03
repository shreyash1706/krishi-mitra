from fastapi import FastAPI
from pydantic import BaseModel
from agent import BaseAgent
from llama_cpp import Llama
from router import IntentRouter
from typing import Optional
import sqlite3
from agri_tools import get_coords

app = FastAPI(title="Krishi Mitra API")

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

# model_path = r"C:\Users\anjal\Desktop\krishi-mitra\models\qwen2-0_5b-instruct-q4_k_m.gguf"
model_path = "models/Qwen3-14B-Q4_K_M.gguf"

SHARED_LLM = Llama(
    model_path=model_path,
    n_gpu_layers=0,
    n_ctx=2048,
    n_threads=6,
    verbose=False
)

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
            "Use 'get_agri_forecast' before advising on irrigation."
        ),
    ),
    "pest": BaseAgent(
        agent_mode="Pest & Disease",
        system_prompt=(
            "You are Krishi Mitra, a Plant Pathologist. "
            "Use 'get_agri_forecast' before diagnosing fungal issues."
        ),
    ),
    "market": BaseAgent(
        agent_mode="Market Expert",
        system_prompt=(
            "You are Krishi Mitra, a Market Analyst. "
            "ALWAYS use 'get_market_price' before answering."
        ),
    ),
    "finance": BaseAgent(
        agent_mode="Finance Advisor",
        system_prompt=(
            "You are Krishi Mitra, a Banking Consultant for Farmers."
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

class UserRequest(BaseModel):
    user_id: str
    name: str
    district: Optional[str] = None
    village: Optional[str]
# --------------------------------------------------
# CHAT ENDPOINT
# --------------------------------------------------
@app.post("/register")
async def register_endpoint(req: UserRequest):
    
    if req.village=="":
        lat, lon = get_coords(req.village, req.district)
    else:
        try:
            with open("maharashtra_districts_coords.json", "r") as f:
                district_coords = json.load(f)
            
            # The JSON stores a list: [latitude, longitude]
            coords_list = district_coords.get(req.district)   
            
            lat = coords_list[0]
            lon = coords_list[1]
                
        except Exception as e:
            print(f"Error loading district coords: {e}")
    conn = sqlite3.connect("krishi.db")
    c = conn.cursor()

    c.execute("SELECT user_id FROM farmers WHERE user_id = ?", (req.user_id,))
    farmer = c.fetchone()

    if not farmer:
        # Insert new farmer
        c.execute("""
            INSERT INTO farmers (user_id, name, village, district,lat,lon)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (req.user_id, req.name, req.village, req.district,lat,lon))
    else:
        # Update farmer details if they changed
        c.execute("""
            UPDATE farmers
            SET name = ?, village = ?, district = ?, lat = ?, lon = ?
            WHERE user_id = ?
        """, (req.name, req.village, req.district, req.user_id))

    conn.commit()
    conn.close()
    return {"status": "success", "message": "User registered/updated"} 

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    
    # 4. RUN ROUTER EVERY TIME (Fast & Cheap)
    decision = router.classify(req.query, debug=True)
    target = decision.get("agent", "crop")
    should_think = decision.get("think", False)
    
    # 4. SESSION MANAGEMENT
    if not req.session_id:
        # Brand new chat
        conn = sqlite3.connect("krishi.db")
        c = conn.cursor()
        c.execute("INSERT INTO sessions (user_id, agent_mode, title) VALUES (?, ?, ?)", 
                  (req.user_id, target, req.query[:31]))
        req.session_id = c.lastrowid
        conn.commit()
        conn.close()
    
    # Notice we don't need the 'else' block to fetch the old agent anymore!
    # If the user switches topics mid-chat, 'target' smoothly shifts to the new agent 
    # but keeps saving to the same session_id so the UI tab stays the same.

    # 4. DISPATCH
    active_agent = AGENTS.get(target, AGENTS["crop"])
    
    # Pass 'should_think' down to the agent
    reply = active_agent.run(req.query, req.session_id, req.user_id, should_think)
    
    return {
        "reply": reply,
        "session_id": req.session_id,
        "agent": target
    }  

