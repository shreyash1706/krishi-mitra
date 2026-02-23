

KRISHI_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_agri_forecast",
            "description": "Get the 7-day agriculture-specific weather forecast (temperature, rain, wind, humidity, evaporation). Useful for planning sowing, spraying, irrigation and general farming help.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat": {"type": "number", "description": "Latitude of the farm"},
                    "lon": {"type": "number", "description": "Longitude of the farm"}
                },
                "required": ["lat", "lon"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_historical_rainfall",
            "description": "Get past rainfall and temperature data for a specific date range. Useful for analyzing past droughts or yield drops.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat": {"type": "number"},
                    "lon": {"type": "number"},
                    "start_date": {"type": "string", "description": "Start date in YYYY-MM-DD format"},
                    "end_date": {"type": "string", "description": "End date in YYYY-MM-DD format"}
                },
                "required": ["lat", "lon", "start_date", "end_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_soil_details",
            "description": "Get soil type, pH, nitrogen, organic carbon and water holding capacity for a location. CRITICAL before recommending fertilizers or crop types or pest & disease advice.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat": {"type": "number"},
                    "lon": {"type": "number"}
                },
                "required": ["lat", "lon"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_market_price",
            "description": "Fetch real-time crop prices from APMC markets in Maharashtra.",
            "parameters": {
                "type": "object",
                "properties": {
                    "crop_name": {"type": "string", "description": "Name of the crop (e.g., 'onion', 'cotton')"},
                    "location": {"type": "string", "description": "Village, APMC name, or District of the user"}
                },
                "required": ["crop_name", "location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the live internet. Use this ONLY when you need real-time news, recent events, or information not available in your knowledge base (e.g., 'latest government farming subsidies 2026', 'recent pest outbreaks in Maharashtra').",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string", 
                        "description": "The exact search query to type into the search engine. Make it specific."
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Number of results to fetch. Default is 3. Max is 5."
                    }
                },
                "required": ["query"]
            }
        }
    }
]