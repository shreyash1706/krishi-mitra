from datetime import datetime
import json
from llama_cpp import Llama
import sqlite3
from tool_schema import KRISHI_TOOLS
from agri_tools import get_agri_forecast, get_historical_rainfall, get_soil_details
from market_tools import get_market_price
import re
import traceback
class BaseAgent:
    def __init__(self, agent_mode,system_prompt):
        self.agent_mode = agent_mode
        self.system_prompt =system_prompt

        #main.py holds model instance 
        self.llm = None
        self.tool_functions = {
            "get_agri_forecast": get_agri_forecast,
            "get_historical_rainfall": get_historical_rainfall,
            "get_soil_details": get_soil_details,
            "get_market_price": get_market_price
            #more to come
        }
    def set_llm(self, instance):
        self.llm = instance 
        
    def _get_todays_date_prompt(self):
        today = datetime.now()
        return f"\n[TIME CONTEXT] Current Date: {today.strftime('%d-%m-%Y')}.\n"

    def get_history(self,session_id):
        conn = sqlite3.connect('krishi.db')
        conn.row_factory = sqlite3.Row
        c= conn.cursor()

        c.execute("""
        SELECT role,content FROM messages
        WHERE session_id = ?
        ORDER BY timestamp ASC
        """, (session_id,))

        rows =c.fetchall()
        conn.close()

        return [{"role":r["role"], "content": r["content"]} for r in rows]


    def save_message(self,session_id,role,content):
        #save message to a tab 
        conn = sqlite3.connect("krishi.db")  
        c = conn.cursor()

        c.execute("INSERT INTO messages (session_id, role, content) VALUES (?,?,?)",(session_id, role ,content))
        conn.commit()
        conn.close()
        
    def get_farmer_profile(self, user_id):
        """Fetches the farmer's profile to inject into the AI's brain."""
        conn = sqlite3.connect('krishi.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT name, district, soil_details FROM farmers WHERE user_id = ?", (user_id,))
        row = c.fetchone()
        conn.close()
        
        if row:
            return f"User Name: {row['name']}. Location: {row['district']}. Soil: {row['soil_details']}."
        return "No profile available for this user."

    def run(self, user_query, session_id, user_id, should_think=True):
        #TODO: get_faremr_profile not used to attach user details in the system prompt 
        # 1. Save the CLEAN message to the database for the user UI
        self.save_message(session_id, "user", user_query)
        history = self.get_history(session_id)
        
        # --- THE FIX: INJECT THE THINKING TAG ---
        # Modify the very last message in the history (which is the query we just saved)
        if history and history[-1]["role"] == "user":
            tag = " /think" if should_think else " /no think"
            history[-1]["content"] += tag

        full_system_prompt = self.system_prompt + self._get_todays_date_prompt()
        messages = [{"role": "system", "content": full_system_prompt}] + history

        print(f"🤖 [{self.agent_mode}] Thinking Mode: {should_think}...")
        
        print(messages)
        
        # 2. FIRST PASS (Allow LLM to call tools)
        output = self.llm.create_chat_completion(
            messages=messages,
            tools=KRISHI_TOOLS,
            tool_choice="auto", 
            temperature=0.1
        )
        
        response_message = output['choices'][0]['message']
        print(response_message)

        content = response_message.get('content', '')
        # 3. CHECK FOR NATIVE TOOL CALLS
        if "<tool_call>" in content:
            json_str_match = re.search(r"<tool_call>(.*?)</tool_call>", content, re.DOTALL)
            
            if json_str_match:
                json_str = json_str_match.group(1).strip()
                
                try:
                    tool_call = json.loads(json_str)
                    tool_name = tool_call.get("name")
                    
                    # Fix: arguments is already a dictionary, do NOT json.loads it again!
                    tool_args = tool_call.get("arguments", {})

                    print(f"🛠️ [TOOL CALLED] {tool_name} with {tool_args}")

                    # 4. EXECUTE THE PYTHON FUNCTION
                    func = self.tool_functions.get(tool_name)
                    if func:
                        try:
                            # We unpack the dictionary as arguments into the function
                            tool_result = str(func(**tool_args))
                        except Exception as e:
                            err_details = traceback.format_exc()
                            print(f"Crash dump:\n{err_details}")
                            tool_result = f"Error executing tool. Please try again"
                    else:
                        tool_result = f"Tool {tool_name} not found."

                    print(f"✅ [TOOL RESULT]: {tool_result}")

                    # 5. FEED RESULT BACK TO LLM
                    messages.append(response_message)
                    
                    # Since Qwen is using text-based XML tool calling, we feed the result back 
                    # exactly how Qwen expects to read it
                    messages.append({
                        "role": "user",
                        "content": f"<tool_response>\n{tool_result}\n</tool_response>"
                    })

                    print(f"🧠 [{self.agent_mode}] Reading tool data and formulating final answer...")
                    
                    # 6. SECOND PASS (Final Answer based on data)
                    final_output = self.llm.create_chat_completion(
                        messages=messages,
                        temperature=0.7
                    )
                    final_reply = final_output['choices'][0]['message']['content']
                    
                    # Clean up <think> tags from the final reply
                    clean_reply = re.sub(r'<think>.*?</think>', '', final_reply, flags=re.DOTALL).strip()
                    
                    self.save_message(session_id, "assistant", clean_reply)
                    return clean_reply
                    
                except json.JSONDecodeError as e:
                    print(f"❌ JSON Parse Error: {e}")
                    return "Error parsing tool request."

        else:
            # LLM didn't need a tool, just replied normally
            reply = response_message.get('content', '')
            
            # Clean up <think> tags if they exist
            clean_reply = re.sub(r'<think>.*?</think>', '', reply, flags=re.DOTALL).strip()
            
            self.save_message(session_id, "assistant", clean_reply)
            return clean_reply