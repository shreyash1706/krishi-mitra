import json

class IntentRouter:
    def __init__(self, llm_instance):
        self.llm = llm_instance

    def classify(self, query: str, debug=True):
        
        router_schema = {
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {
                    "search_plans": {
                        "type": "array",
                        "description": "List of databases to search and the specific queries to use.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "domain": {
                                    "type": "string",
                                    "enum": ["crop", "pest", "finance"],
                                    "description": "The specific database to query."
                                },
                                "search_query": {
                                    "type": "string",
                                    "description": "A refined, specific search string optimized for document retrieval. (HyDE concept)"
                                }
                            },
                            "required": ["domain", "search_query"]
                        }
                    },
                    "primary_domain": {
                        "type": "string",
                        "enum": ["crop", "pest", "market", "finance"],
                        "description": "The main focus of the user's question."
                    },
                    "think": {
                        "type": "boolean",
                        "description": "True if the user's request requires reasoning, planning, or complex synthesis."
                    }
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
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]

        try:
            response = self.llm.create_chat_completion(
                messages=messages,
                # ONLY use json_object. Drop the strict 'schema' parameter!
                response_format={"type": "json_object", "schema": router_schema}, 
                max_tokens=250, 
                temperature=0.1
            )

            raw_text = response['choices'][0]['message']['content']
            
            if debug:
                print(f"[ROUTER RAW]: {raw_text}")
                
            return json.loads(raw_text)

        except Exception as e:
            if debug: print(f"[Router Error]: {e}")
            return {
                "search_plans": [{"domain": "crop", "search_query": query}], 
                "primary_domain": "crop",
                "think": False
            }