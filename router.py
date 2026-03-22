import json
import re

class IntentRouter:
    def __init__(self, llm_instance):
        self.llm = llm_instance

    def classify(self, query: str, debug=True):
        router_schema = {"type": "json_object",
        "schema": {
            "type": "object",
            "properties": {
                "agent": {
                    "type": "string",
                    "enum": ["crop", "pest", "market", "finance"]
                },
                "think": {
                    "type": "boolean"
                }
            },
            "required": ["agent", "think"]
        }}

        messages = [
            {
                "role": "system",
                "content": "You are a classification engine. Output JSON only. Choose between crop, pest, market and finance for agent depending on the domain of the query and decide between think or not based on if the query might involve reasoning or planning. Default to 'crop' if unsure. /no_think"
            },
            {
                "role": "user",
                "content": query + " /no_think"
            }
        ]

        try:
            response = self.llm.create_chat_completion(
                messages=messages,
                response_format=router_schema,
                max_tokens=64,
                temperature=0.1
            )

            raw_text = response['choices'][0]['message']['content'].strip()

            if debug:
                print(f"[ROUTER RAW]: {raw_text}")

            # Non-greedy regex: grab the FIRST {...} block only
            match = re.search(r'\{[^}]*\}', raw_text)
            if match:
                json_str = match.group()
                return json.loads(json_str)

            return json.loads(raw_text)

        except Exception as e:
            if debug: print(f"[Router Error]: {e}")
            return {"agent": "crop", "think": False}