from fastapi import FastAPI
from pydantic import BaseModel
from agent import BaseAgent
from llama_cpp import Llama
from router import IntentRouter
from typing import Optional
import sqlite3

app = FastAPI(title="Krishi Mitra API")

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

model_path = r"C:\Users\anjal\Desktop\krishi-mitra\models\qwen2-0_5b-instruct-q4_k_m.gguf"

SHARED_LLM = Llama(
    model_path=model_path,
    n_gpu_layers=0,
    n_ctx=2048,
    n_threads=6,
    verbose=True
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
    name: Optional[str] = None
    village: Optional[str] = None
    district: Optional[str] = None


# --------------------------------------------------
# CHAT ENDPOINT
# --------------------------------------------------

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):

    # 1️⃣ ROUTER DECISION
    decision = router.classify(req.query, debug=True)
    target = decision.get("agent", "crop")
    should_think = decision.get("think", False)

    # 2️⃣ DATABASE CONNECTION
    conn = sqlite3.connect("krishi.db")
    c = conn.cursor()

    # --------------------------------------------------
    # ENSURE FARMER EXISTS OR UPDATE
    # --------------------------------------------------
    c.execute("SELECT user_id FROM farmers WHERE user_id = ?", (req.user_id,))
    farmer = c.fetchone()

    if not farmer:
        # Insert new farmer
        c.execute("""
            INSERT INTO farmers (user_id, name, village, district)
            VALUES (?, ?, ?, ?)
        """, (
            req.user_id,
            req.name,
            req.village,
            req.district
        ))
    else:
        # Update farmer details if provided
        c.execute("""
            UPDATE farmers
            SET name = ?, village = ?, district = ?
            WHERE user_id = ?
        """, (
            req.name,
            req.village,
            req.district,
            req.user_id
        ))

    # --------------------------------------------------
    # CREATE SESSION IF NEW
    # --------------------------------------------------
    if not req.session_id:
        c.execute("""
            INSERT INTO sessions (user_id, agent_mode, title)
            VALUES (?, ?, ?)
        """, (
            req.user_id,
            target,
            req.query[:30]
        ))

        req.session_id = c.lastrowid

    conn.commit()
    conn.close()

    # 3️⃣ DISPATCH TO AGENT
    active_agent = AGENTS.get(target, AGENTS["crop"])

    reply = active_agent.run(
        req.query,
        req.session_id,
        req.user_id,
        should_think
    )

    # 4️⃣ RETURN RESPONSE
    return {
        "reply": reply,
        "session_id": req.session_id,
        "agent": target
    }