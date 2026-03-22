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

        # main.py holds model instance
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
        conn = sqlite3.connect("krishi.db")
        c = conn.cursor()
        c.execute("INSERT INTO messages (session_id, role, content) VALUES (?,?,?)", (session_id, role, content))
        conn.commit()
        conn.close()

    def get_farmer_profile(self, user_id):
        """Fetches the farmer's profile to inject into the AI's brain."""
        conn = sqlite3.connect('krishi.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT name, district, soil_details, lat, lon FROM farmers WHERE user_id = ?", (user_id,))
        row = c.fetchone()
        conn.close()
        if row:
            return f"User Name: {row['name']}. Location: {row['district']} & Coordinates: {row['lat']}, {row['lon']}. Soil: {row['soil_details']}."
        return "No profile available for this user."

    def run(self, user_query, session_id, user_id, should_think=True):
        self.save_message(session_id, "user", user_query)
        history = self.get_history(session_id)

        user_profile_string = self.get_farmer_profile(user_id)

        # Only append /no_think if should_think is False
        if history and history[-1]["role"] == "user":
            tag = " /think" if should_think else " /no_think"
            history[-1]["content"] += tag

        # Build tool schema prompt since we no longer pass native tools array
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

            # -------------------------------------------------------
            # PASS 1: STREAM tokens live + detect tool calls
            # -------------------------------------------------------
            output_stream = self.llm.create_chat_completion(
                messages=messages,
                temperature=0.1,
                max_tokens=4096,  # Increased to allow full reasoning blocks without cut-offs
                stream=True
            )

            raw_content = ""
            reasoning_text = ""

            yielded_content_len = 0
            yielded_reason_len = 0

            for chunk in output_stream:
                delta = chunk.get('choices', [{}])[0].get('delta', {})

                # Accumulate and stream reasoning_content live (if natively supported by backend)
                if 'reasoning_content' in delta and delta['reasoning_content'] is not None:
                    rc = delta['reasoning_content']
                    reasoning_text += rc
                    yield json.dumps({"reasoning": rc, "agent": self.agent_mode, "session_id": session_id}) + "\n"

                # Stream content tokens LIVE to user safely (handles <think> mapped inside text stream)
                if 'content' in delta and delta['content'] is not None:
                    token = delta['content']
                    raw_content += token

                    # Extract visible text by obliterating all tags
                    visible_now = re.sub(r'<think>.*?</think>', '', raw_content, flags=re.DOTALL)
                    visible_now = re.sub(r'<tool_call>.*?</tool_call>', '', visible_now, flags=re.DOTALL)
                    
                    idx = visible_now.rfind('<think>')
                    if idx != -1: visible_now = visible_now[:idx]
                    idx = visible_now.rfind('<tool_call>')
                    if idx != -1: visible_now = visible_now[:idx]
                    
                    for tag in ["<tool_call>", "<think>"]:
                        for i in range(len(tag)-1, 0, -1):
                            if visible_now.endswith(tag[:i]):
                                visible_now = visible_now[:-i]
                                break
                                
                    if len(visible_now) > yielded_content_len:
                        new_chars = visible_now[yielded_content_len:]
                        yielded_content_len = len(visible_now)
                        if new_chars:
                            print(f"\r[UI DEBUG] Extracted {yielded_content_len} visible tokens safely to chat window...   ", end="", flush=True)
                            yield json.dumps({"chunk": new_chars, "agent": self.agent_mode, "session_id": session_id}) + "\n"

                    # Simultaneously extract reasoning dynamically to populate the expandable block
                    think_blocks = re.findall(r'<think>(.*?)</think>', raw_content, flags=re.DOTALL)
                    current_think = "".join(think_blocks)
                    
                    unclosed_idx = raw_content.rfind('<think>')
                    closed_idx = raw_content.rfind('</think>')
                    if unclosed_idx != -1 and unclosed_idx > closed_idx:
                        current_think += raw_content[unclosed_idx + 7:]
                        
                    if len(current_think) > yielded_reason_len:
                        new_rc = current_think[yielded_reason_len:]
                        yielded_reason_len = len(current_think)
                        if new_rc:
                            print(f"\r[UI DEBUG] Isolated {yielded_reason_len} reasoning tokens into expander...       ", end="", flush=True)
                            yield json.dumps({"reasoning": new_rc, "agent": self.agent_mode, "session_id": session_id}) + "\n"

            # If content was empty, fall back to reasoning_content
            if not raw_content.strip() and reasoning_text.strip():
                raw_content = reasoning_text
                # Strip think tags and display
                visible = re.sub(r'<think>.*?</think>', '', raw_content, flags=re.DOTALL).strip()
                display_text = re.sub(r'<tool_call>.*?</tool_call>', '', visible, flags=re.DOTALL).strip()
                if display_text:
                    yield json.dumps({"chunk": display_text, "agent": self.agent_mode, "session_id": session_id}) + "\n"
            
            t1 = time.time()
            print(f"[AGENT] Pass 1: {len(raw_content)} chars in {t1-t0:.1f}s")

            # -------------------------------------------------------
            # Parse tool calls from raw content
            # -------------------------------------------------------
            all_tools = []
            xml_tool_matches = re.findall(r'<tool_call>(.*?)</tool_call>', raw_content, flags=re.DOTALL)
            for m in xml_tool_matches:
                try:
                    parsed = json.loads(m.strip())
                    all_tools.append({"name": parsed["name"], "args_str": json.dumps(parsed.get("arguments", {}))})
                except:
                    pass

            has_tools = len(all_tools) > 0

            if has_tools:
                messages.append({"role": "assistant", "content": raw_content})

                for tool_info in all_tools:
                    tool_name = tool_info["name"]
                    args_str = tool_info["args_str"]

                    yield json.dumps({
                        "chunk": f"\n\n🛠️ Using structural tool: **{tool_name}**... ",
                        "agent": self.agent_mode,
                        "session_id": session_id
                    }) + "\n"

                    t_tool_start = time.time()


                    try:
                        tool_args = json.loads(args_str) if args_str else {}
                    except json.JSONDecodeError:
                        tool_args = {}

                    func = self.tool_functions.get(tool_name)
                    if func:
                        try:
                            tool_result = str(func(**tool_args))
                            if func == get_soil_details:
                                conn = sqlite3.connect("krishi.db")
                                c = conn.cursor()
                                c.execute("UPDATE farmers SET soil_details = ? WHERE user_id = ?", (tool_result, user_id))
                                conn.commit()
                                conn.close()
                        except Exception as e:
                            traceback.print_exc()
                            tool_result = f"Error executing tool: {e}"
                    else:
                        tool_result = f"Tool '{tool_name}' not found."

                    t_tool_end = time.time()
                    elapsed = t_tool_end - t_tool_start
                    yield json.dumps({
                        "chunk": f"*[Took {elapsed:.1f}s]*\n\n",
                        "agent": self.agent_mode,
                        "session_id": session_id
                    }) + "\n"

                    messages.append({
                        "role": "user",
                        "content": f"<tool_response>\n{tool_result}\n</tool_response>"
                    })

                messages.append({
                    "role": "system",
                    "content": "You have received the tool results. Provide the final answer to the user now. DO NOT output any <tool_call> tags. DO NOT ask for more information."
                })

                # -------------------------------------------------------
                # PASS 2: Final answer with tool results (streamed live)
                # -------------------------------------------------------
                t2 = time.time()
                pass2_stream = self.llm.create_chat_completion(
                    messages=messages,
                    temperature=0.7,
                    max_tokens=4096,
                    stream=True
                )

                final_text = ""
                yielded_final_len = 0
                for chunk in pass2_stream:
                    delta = chunk.get('choices', [{}])[0].get('delta', {})
                    if 'content' in delta and delta['content'] is not None:
                        c = delta['content']
                        final_text += c
                        
                        visible_now = re.sub(r'<think>.*?</think>', '', final_text, flags=re.DOTALL)
                        visible_now = re.sub(r'<tool_call>.*?</tool_call>', '', visible_now, flags=re.DOTALL)
                        idx = visible_now.rfind('<think>')
                        if idx != -1: visible_now = visible_now[:idx]
                        idx = visible_now.rfind('<tool_call>')
                        if idx != -1: visible_now = visible_now[:idx]
                        for tag in ["<tool_call>", "<think>"]:
                            for i in range(len(tag)-1, 0, -1):
                                if visible_now.endswith(tag[:i]):
                                    visible_now = visible_now[:-i]
                                    break
                                    
                        if len(visible_now) > yielded_final_len:
                            new_chars = visible_now[yielded_final_len:]
                            yielded_final_len = len(visible_now)
                            if new_chars:
                                print(f"\r[UI DEBUG] Extracted {yielded_final_len} visible tokens safely to chat window... ", end="", flush=True)
                                yield json.dumps({"chunk": new_chars, "agent": self.agent_mode, "session_id": session_id}) + "\n"
                    if 'reasoning_content' in delta and delta['reasoning_content'] is not None:
                        rc = delta['reasoning_content']
                        final_text += rc
                        yield json.dumps({"reasoning": rc, "agent": self.agent_mode, "session_id": session_id}) + "\n"

                t3 = time.time()
                print(f"[AGENT] Pass 2: {len(final_text)} chars in {t3-t2:.1f}s | Total: {t3-t0:.1f}s")
                clean_final = re.sub(r'<think>.*?</think>', '', final_text, flags=re.DOTALL).strip()
                visible = re.sub(r'<tool_call>.*?</tool_call>', '', re.sub(r'<think>.*?</think>', '', raw_content, flags=re.DOTALL), flags=re.DOTALL).strip()
                self.save_message(session_id, "assistant", (visible + "\n\n" + clean_final).strip())
            else:
                # No tools — save directly
                visible = re.sub(r'<tool_call>.*?</tool_call>', '', re.sub(r'<think>.*?</think>', '', raw_content, flags=re.DOTALL), flags=re.DOTALL).strip()
                self.save_message(session_id, "assistant", visible)
                print(f"[AGENT] Done (no tools): {time.time()-t0:.1f}s total")

        return generate_stream()