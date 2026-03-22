import json
import re
import time
from tqdm import tqdm # pip install tqdm (gives you a nice progress bar)
from router import IntentRouter
from search import get_knowledge
from agent import BaseAgent
from llama_cpp import Llama
# --- IMPORT YOUR EXISTING KRISHI MITRA FUNCTIONS HERE ---
# from your_router_file import router
# from your_db_file import get_knowledge
# from your_llm_file import generate_qwen_response

import re

print("🧠 Booting up Qwen-14B into VRAM...")
qwen_llm = Llama(
    model_path="models/Qwen3-14B-Q4_K_M.gguf",
    n_gpu_layers=0,
    n_ctx=4096,
    verbose=False
)

# 1. CROP AGENT
crop_agent = BaseAgent(
    agent_mode="Crop Planner",
    system_prompt="You are Krishi Mitra, an expert Agronomist. Focus on soil, sowing, and harvesting."
)
crop_agent.set_llm(qwen_llm)

# 2. PEST AGENT
pest_agent = BaseAgent(
    agent_mode="Plant Pathologist",
    system_prompt="You are Krishi Mitra, an expert Plant Pathologist. Diagnose diseases and recommend chemical/organic treatments."
)
pest_agent.set_llm(qwen_llm)

# 3. FINANCE AGENT
finance_agent = BaseAgent(
    agent_mode="Agri-Financial Advisor",
    system_prompt="You are Krishi Mitra, an expert in agricultural economics. Focus on ROI, market prices, and loan subsidies."
)
finance_agent.set_llm(qwen_llm)

# --- THE AGENT ROUTER DICTIONARY ---
# This maps the Intent Router's JSON output directly to your Python objects
AGENT_DIRECTORY = {
    "crop": crop_agent,
    "pest": pest_agent,
    "finance": finance_agent,
    "market": finance_agent # Grouping market and finance together for now
}

router = IntentRouter(qwen_llm)

def generate_stateless_eval_response(agent_instance, question, compiled_knowledge):
    """
    Bypasses the SQLite DB to safely generate responses for 200 eval questions.
    """
    # 1. Build the exact system prompt your agent uses
    system_prompt = agent_instance.system_prompt
    today_str = agent_instance._get_todays_date_prompt()
    
    # Use a dummy profile for evaluation consistency
    dummy_profile = "User Name: Eval_Test. Location: Pune & Coordinates: 18.52, 73.85. Soil: None."
    
    full_system_prompt = f"{system_prompt}\n{today_str}\n\n[USER PROFILE DETAILS]\n{dummy_profile}"
    
    if compiled_knowledge != "":
        full_system_prompt += f"\n\n[COMPILED KNOWLEDGE]\n{compiled_knowledge}"

    # 2. Force the think tag on the user's query
    forced_query = question + " /think"

    # 3. Format messages array
    messages = [
        {"role": "system", "content": full_system_prompt},
        {"role": "user", "content": forced_query}
    ]

    # 4. Call your LLM directly (Bypassing the tools/DB loop in .run())
    output = agent_instance.llm.create_chat_completion(
        messages=messages,
        temperature=0.1
    )
    
    raw_reply = output['choices'][0]['message'].get('content', '')
    
    # 5. Strip the think tags to get the clean answer
    clean_reply = re.sub(r'<think>.*?</think>', '', raw_reply, flags=re.DOTALL).strip()
    
    return raw_reply, clean_reply

def clean_think_tags(raw_text):
    """Removes everything inside <think>...</think> and returns just the final answer."""
    # The re.DOTALL flag ensures it matches across multiple newlines
    clean_text = re.sub(r'<think>.*?</think>', '', raw_text, flags=re.DOTALL)
    return clean_text.strip()

def process_eval_dataset(input_json_path, output_json_path):
    # 1. Load the 200 questions
    with open(input_json_path, 'r') as f:
        eval_data = json.load(f)
    
    results = []

    print(f"🚀 Starting batch evaluation for {len(eval_data)} questions...")
    
    # Loop through with a progress bar
    for index, item in enumerate(tqdm(eval_data)):
        question = item.get("question")
        
        try:
            # --- STEP 1: ROUTING ---
            decision = router.classify(question)
            search_plans = decision.get("search_plans", [])
            primary_domain = decision.get("primary_domain", "crop")
            
            # 🛑 FORCE THINK MODE (Ignore the router's choice)
            should_think = True 

            # --- STEP 2: RAG RETRIEVAL ---
            compiled_knowledge = ""
            if search_plans:
                for plan in search_plans:
                    domain = plan.get("domain")
                    search_query = plan.get("search_query")
                    
                    # Fetch from your Qdrant database
                    retrieved_text = get_knowledge(query=search_query, domain=domain)
                    if retrieved_text:
                        compiled_knowledge += f"\n--- FROM {domain.upper()} DATABASE ---\n{retrieved_text}\n"

            # --- STEP 3: BUILD PROMPT & GENERATE ---
            if primary_domain=="crop":
                agent_inst = crop_agent
            elif primary_domain == "pest":
                agent_inst = pest_agent
            else:
                agent_inst = finance_agent
            # Since you want to force it to think, append /think to the user query behind the scenes
            
            # Call your local Qwen model
            raw_response, final_clean_answer = generate_stateless_eval_response(
                agent_instance=agent_inst, 
                question=question, 
                compiled_knowledge=compiled_knowledge
            )

            # --- STEP 5: STORE RICH DATA ---
            # We store everything so you can debug if a question fails
            output_record = {
                "document_name": item.get("document_name", "unknown"),
                "question": question,
                "expected_answer": item.get("expected_answer", ""),
                "difficulty": item.get("difficulty", "unknown"),
                "generated_answer": final_clean_answer,       # <--- The clean text for grading
                "raw_response": raw_response,                 # <--- Keep the thoughts just in case
                "router_plans": search_plans,                 # <--- To prove your routing works
                "retrieved_context": compiled_knowledge       # <--- Needed for RAGAS Context Precision
            }
            
            results.append(output_record)

        except Exception as e:
            print(f"\n❌ FAILED on question {index}: {question}")
            print(f"Error: {e}")
            # Append a failed record so the loop doesn't completely die and ruin the array
            results.append({"question": question, "error": str(e)})

        # --- CRITICAL: INCREMENTAL SAVE ---
        # Overwrite the file after every single question. 
        # If your PC crashes at question 150, you still have 150 answers saved!
        with open(output_json_path, 'w') as f:
            json.dump(results, f, indent=4)

    print(f"\n✅ Finished! Results saved to {output_json_path}")

# --- RUN IT ---
if __name__ == "__main__":
    INPUT_FILE = "cleaned_dataset.json" # Your 200 questions
    OUTPUT_FILE = "krishi_mitra_results.json" 
    
    process_eval_dataset(INPUT_FILE, OUTPUT_FILE)