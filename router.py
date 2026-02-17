import json

class IntentRouter:
    def __init__(self, llm_instance):
        self.llm = llm_instance

    def classify(self, query: str, debug=True):
        # 1. Define the Schema (The Rules)
        # This tells the model exactly what keys and values are allowed.
        router_schema = {"type":"json_object",
        "schema":{
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

        # 2. Define the Prompt
        # Note: We remove "general" from the prompt since we removed it from the enum
        messages = [
            {
                "role": "system", 
                "content": "You are a classification engine. Output JSON only. Choose between crop,pest, market and finance for agent depending on the domain of the query and decide between think or not based on if the query might involve reseasoning or planning. Default to 'crop' if unsure."
            },
            {
                "role": "user", 
                "content": query
            }
        ]

        try:
            # 3. Call with response_format
            response = self.llm.create_chat_completion(
                messages=messages,
                response_format={
                    "type": "json_object",
                    "schema": router_schema
                },
                max_tokens=50,
                temperature=0.1 # Low temp for consistency
            )

            raw_text = response['choices'][0]['message']['content']
            
            if debug:
                print(f"[ROUTER RAW]: {raw_text}")
            # print(response)
            # print()
            return json.loads(raw_text)

        except Exception as e:
            if debug: print(f"[Router Error]: {e}")
            return {"agent": "crop", "think": False}