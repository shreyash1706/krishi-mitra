from datetime import datetime
import json
import time
import sqlite3
from tool_schema import KRISHI_TOOLS
from agri_tools import get_agri_forecast, get_historical_rainfall, get_soil_details
from web_tools import web_search
from market_tools import get_market_price, get_trending_crops
import re
import traceback

class BaseAgent:
    def __init__(self, agent_mode, system_prompt):
        self.agent_mode = agent_mode
        self.system_prompt = system_prompt
        self.llm = None
        self.tool_functions = {
            "get_agri_forecast": get_agri_forecast,
            "get_historical_rainfall": get_historical_rainfall,
            "get_soil_details": get_soil_details,
            "get_market_price": get_market_price,
            "get_trending_crops": get_trending_crops,
            "web_search": web_search
        }

    def set_llm(self, instance):
        self.llm = instance

    def _get_todays_date_prompt(self):
        today = datetime.now()
        return f"\n[TIME CONTEXT] Current Date: {today.strftime('%d-%m-%Y')}.\n"

    def get_history(self, session_id):
        conn = sqlite3.connect('krishi.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("""
        SELECT role, content FROM messages
        WHERE session_id = ?
        ORDER BY timestamp ASC
        """, (session_id,))
        rows = c.fetchall()
        conn.close()
        return [{"role": r["role"], "content": r["content"]} for r in rows]

    def save_message(self, session_id, role, content):
        if not content or not content.strip(): return
        conn = sqlite3.connect("krishi.db")
        c = conn.cursor()
        c.execute("INSERT INTO messages (session_id, role, content) VALUES (?,?,?)", (session_id, role, content.strip()))
        conn.commit()
        conn.close()

    def get_farmer_profile(self, user_id):
        conn = sqlite3.connect('krishi.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT name, district, soil_details, lat, lon FROM farmers WHERE user_id = ?", (user_id,))
        row = c.fetchone()
        conn.close()
        if row:
            return f"User Name: {row['name']}. Location: {row['district']} & Coordinates: {row['lat']}, {row['lon']}. Soil: {row['soil_details']}."
        return "No profile available for this user."

    def extract_visible_text(self, text):
        """Robustly extracts visible text by removing <think> and <tool_call> tags safely."""
        # 1. Remove all fully closed tags
        clean = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        clean = re.sub(r'<tool_call>.*?</tool_call>', '', clean, flags=re.DOTALL)
        
        # 2. Hide everything from the absolute first start tag to the end of string
        # This handles cases where tags are currently opening but not yet closed
        first_tag_pos = float('inf')
        for tag in ["<think>", "<tool_call>"]:
            pos = clean.find(tag)
            if pos != -1:
                first_tag_pos = min(first_tag_pos, pos)
        
        if first_tag_pos != float('inf'):
            clean = clean[:first_tag_pos]
            
        # 3. Handle partial tag starts (e.g. "<thi") reaching the stream
        for tag in ["<think>", "<tool_call>"]:
            for i in range(len(tag) - 1, 0, -1):
                if clean.endswith(tag[:i]):
                    clean = clean[:-i]
                    break
        return clean

    def extract_reasoning_text(self, text):
        """Extracts text contained within <think> tags or trailing open <think> tags."""
        think_blocks = re.findall(r'<think>(.*?)</think>', text, flags=re.DOTALL)
        extracted = "".join(think_blocks)
        
        unclosed_idx = text.rfind('<think>')
        closed_idx = text.rfind('</think>')
        if unclosed_idx != -1 and unclosed_idx > closed_idx:
            extracted += text[unclosed_idx + 7:]
        return extracted

    def run(self, user_query, session_id, user_id, should_think=True):
        self.save_message(session_id, "user", user_query)
        history = self.get_history(session_id)
        user_profile_string = self.get_farmer_profile(user_id)

        if history and history[-1]["role"] == "user":
            tag = " /think" if should_think else " /no_think"
            history[-1]["content"] += tag

        available_tools = [t["function"] for t in KRISHI_TOOLS if t["function"]["name"] in self.tool_functions]
        tools_str = json.dumps(available_tools, indent=2)
        tool_prompt = f"""
[AVAILABLE TOOLS]
You have access to these tools:
{tools_str}

To use a tool, you MUST output exactly this XML format:
<tool_call>
{{"name": "tool_name", "arguments": {{"arg1": "value"}}}}
</tool_call>
"""
        full_system_prompt = f"{self.system_prompt}\n{tool_prompt}\n{self._get_todays_date_prompt()}\n\n[USER PROFILE DETAILS]\n{user_profile_string}"
        messages = [{"role": "system", "content": full_system_prompt}] + history

        def generate_stream():
            t0 = time.time()
            
            # --- SHARED STATE ---
            buffers = {
                "raw": "",        # Pass 1 full raw
                "reasoning": "",  # Extracted reasoning from Pass 1
                "visible": "",    # Extracted visible from Pass 1
                "final_raw": "",  # Pass 2 full raw
                "final_visible": "" # Extracted visible from Pass 2
            }
            yielded = {"content": 0, "reasoning": 0}

            # -------------------------------------------------------
            # PASS 1: STREAM detection
            # -------------------------------------------------------
            output_stream = self.llm.create_chat_completion(
                messages=messages, temperature=0.1, max_tokens=4096, stream=True
            )

            for chunk in output_stream:
                delta = chunk.get('choices', [{}])[0].get('delta', {})
                
                # A. Handle native reasoning_content
                if delta.get('reasoning_content'):
                    rc = delta['reasoning_content']
                    buffers["reasoning"] += rc
                    yield json.dumps({"reasoning": rc, "agent": self.agent_mode, "session_id": session_id}) + "\n"
                
                # B. Handle text content (where <think> might be hidden)
                if delta.get('content'):
                    token = delta['content']
                    buffers["raw"] += token
                    
                    # 1. Update Reasoning Slot
                    current_r = self.extract_reasoning_text(buffers["raw"])
                    if len(current_r) > yielded["reasoning"]:
                        yield json.dumps({"reasoning": current_r[yielded["reasoning"]:], "agent": self.agent_mode, "session_id": session_id}) + "\n"
                        yielded["reasoning"] = len(current_r)
                    
                    # 2. Update Visible Slot
                    current_v = self.extract_visible_text(buffers["raw"])
                    if len(current_v) > yielded["content"]:
                        yield json.dumps({"chunk": current_v[yielded["content"]:], "agent": self.agent_mode, "session_id": session_id}) + "\n"
                        yielded["content"] = len(current_v)
            
            buffers["visible"] = self.extract_visible_text(buffers["raw"])

            # Force final yield for any remaining visible text
            final_v = self.extract_visible_text(buffers["raw"])
            if len(final_v) > yielded["content"]:
                yield json.dumps({"chunk": final_v[yielded["content"]:], "agent": self.agent_mode, "session_id": session_id}) + "\n"
                yielded["content"] = len(final_v)

            # -------------------------------------------------------
            # Parse tool calls
            # -------------------------------------------------------
            all_tools = []
            combined_text = buffers["raw"] + "\n" + buffers["reasoning"]
            print("[AGENT DEBUG] Combined text size:", len(combined_text))
            xml_tool_matches = re.findall(r'<tool_call>(.*?)</tool_call>', combined_text, flags=re.DOTALL)
            print("[AGENT DEBUG] Tool matches count:", len(xml_tool_matches))
            for m in xml_tool_matches:
                print("[AGENT DEBUG] Raw match:", repr(m))
                try:
                    parsed = json.loads(m.strip())
                    all_tools.append({"name": parsed["name"], "args_str": json.dumps(parsed.get("arguments", {}))})
                    print("[AGENT DEBUG] Successfully parsed tool call.")
                except Exception as e:
                    print(f"[AGENT DEBUG] Failed to parse tool call: {e}")

            if all_tools:
                messages.append({"role": "assistant", "content": buffers["raw"]})
                for tool in all_tools:
                    tool_name, args_str = tool["name"], tool["args_str"]
                    yield json.dumps({"reasoning": f"\n*(Taking action: {tool_name}...)*\n", "agent": self.agent_mode, "session_id": session_id}) + "\n"
                    
                    func = self.tool_functions.get(tool_name)
                    try:
                        args = json.loads(args_str) if args_str else {}
                        result = str(func(**args))
                    except Exception as e:
                        result = f"Error: {str(e)}"
                    
                    messages.append({"role": "user", "content": f"<tool_response>{result}</tool_response>"})
                
                messages.append({"role": "system", "content": "Provide final answer. NO thinking. NO tool calls."})
                
                # --- PASS 2 ---
                yielded["content_pass2"] = 0
                pass2_stream = self.llm.create_chat_completion(
                    messages=messages, temperature=0.7, max_tokens=2048, stream=True
                )
                
                for chunk_obj in pass2_stream:
                    delta = chunk_obj.get('choices', [{}])[0].get('delta', {})
                    token = delta.get('content', '') or delta.get('reasoning_content', '')
                    if token:
                        buffers["final_raw"] += token
                        yield json.dumps({"chunk": token, "agent": self.agent_mode, "session_id": session_id}) + "\n"
                
                # In Pass 2 we told it NO THINKING, so whatever it generated IS the final visible text.
                # Do NOT strip <think> because if it maliciously used <think> it would become empty.
                buffers["final_visible"] = buffers["final_raw"]
                
                # Fallback if pass 2 was somehow empty but pass 1 had something
                if not buffers["final_visible"].strip():
                    buffers["final_visible"] = self.extract_visible_text(buffers["raw"])
                
                self.save_message(session_id, "assistant", buffers["final_visible"])
            else:
                self.save_message(session_id, "assistant", final_v)
                
            print(f"[AGENT] Done. Session: {session_id}")

        return generate_stream()