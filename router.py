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
                "required": ["search_plans", "primary_domain", "think"]
            }
        }
        
        # Notice we moved the exact structure into the prompt itself!
        system_prompt = """
        You are an advanced agricultural classification and search-planning engine. Output JSON only.

        Your job is to read the user's query and decide which knowledge databases ("crop", "pest", "finance") need to be searched to provide a complete answer.

        For each database you select, you must write a highly optimized `search_query` that extracts the core concepts for vector retrieval.

        You MUST output a valid JSON object with EXACTLY this structure:
        {
            "search_plans": [
                {
                    "domain": "pest",
                    "search_query": "..."
                }
            ],
            "primary_domain": "...",
            "think": true
        }

        EXAMPLE INPUT: "My grapes have white powder on the leaves. What spray should I buy?"
        EXAMPLE OUTPUT: 
        {
            "search_plans": [
                {"domain": "pest", "search_query": "grapes white powdery mildew fungal infection fungicide"},
                {"domain": "crop", "search_query": "grape vine canopy management for airflow"}
            ],
            "primary_domain": "pest",
            "think": true
        }

        Decide `think: True` if the query involves multi-step reasoning, planning, or synthesizing data, if it can be answered with a simple answer or tool call then think: False. Default to 'crop' if entirely unsure.
        DO NOT wrap the output in markdown. Start your response directly with { and end with }.
        
        
        /no_think
        """

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
            return {
                "search_plans": [{"domain": "crop", "search_query": query}], 
                "primary_domain": "crop",
                "think": False
            }