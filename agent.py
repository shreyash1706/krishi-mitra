import json
from llama_cpp import Llama
import sqlite3


class BaseAgent:
    def __init__(self, agent_mode,system_prompt):
        self.agent_mode = agent_mode
        self.system_prompt =system_prompt

        #main.py holds model instance 
        self.llm = None

    def set_llm(self, instance):
        self.llm = instance 

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

    def run(self, user_query, session_id, user_id, should_think):
        self.save_message(session_id, "user", user_query)
        history = self.get_history(session_id)
                
        user_context = self.get_farmer_profile(user_id)
        
        # --- DYNAMIC INJECTION ---
        if should_think:
            # Let it reason naturally
            dynamic_system = f"{self.system_prompt}\n\n[USER CONTEXT]\n{user_context} /think"
        else:
            # The Muzzle: Force it to be brief and skip thinking
            dynamic_system = f"{self.system_prompt}\n\n[USER CONTEXT]\n{user_context}\n\n[CRITICAL]: The user made a simple statement, greeting, or basic query. DO NOT over-analyze. /no_think"
        
        messages = [{"role": "system", "content": dynamic_system}] + history

        output = self.llm.create_chat_completion(messages=messages, temperature=0.7)
        reply = output['choices'][0]['message']['content']

        self.save_message(session_id, "assistant", reply)
        return reply