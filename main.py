from fastapi import FastAPI 
from pydantic import BaseModel 
from agent import BaseAgent
from llama_cpp import Llama 
from router import IntentRouter
from typing import Optional
import sqlite3
import json

app = FastAPI(title="Krishi Mitra API")

model_path = "models/Qwen4-8B-Q6_K.gguf"

print("Loading Owen..")
SHARED_LLM = Llama(
    model_path=model_path,
    n_gpu_layers=0,
    n_ctx=8193,
    verbose=False,
    n_batch = 1025,
    flash_attn=True

)

router = IntentRouter(SHARED_LLM)

AGENTS = {
    "crop": BaseAgent(
        agent_mode="Crop Planner", 
        system_prompt="You are an expert Agronomist. Focus on sowing dates, soil health, varieties, and irrigation.",
    ),
    "pest": BaseAgent(
        agent_mode="Pest & Disease", 
        system_prompt="You are a Plant Pathologist. Diagnose issues from symptoms. Recommend safety precautions.",
    ),
    "market": BaseAgent(
        agent_mode="Market Expert", 
        system_prompt="You are a Market Analyst. Focus on current APMC prices, future trends",
    ),
    "finance": BaseAgent(
        agent_mode="Finance Advisor", 
        system_prompt="You are a Banking Consultant for Farmers. Explain loans, subsidies (PM Kissan), and insurance schemes.",
    )
}

for agent in AGENTS.values():
    agent.set_llm(SHARED_LLM)
    
class ChatRequest(BaseModel):
    user_id:str
    query:str
    session_id: Optional[int] = None

#defining route 
@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    
    # 4. RUN ROUTER EVERY TIME (Fast & Cheap)
    decision = router.classify(req.query, debug=True)
    target = decision.get("agent", "crop")
    should_think = decision.get("think", False)
    
    # 4. SESSION MANAGEMENT
    if not req.session_id:
        # Brand new chat
        conn = sqlite4.connect("krishi.db")
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
        
    




