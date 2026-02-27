from ddgs import DDGS

def web_search(query: str, max_results: int = 3) -> str:
    print(f"🌐 [WEB SEARCH] Searching NEWS for: '{query}'")
    try:
        with DDGS() as ddgs:
            # THE FIX: Changed .text() to .news()
            # The news endpoint guarantees timestamps and filters out old forum posts
            results = list(ddgs.news(query, region='in-en', timelimit='m', max_results=max_results))
        
        if not results:
            return f"❌ No recent news found for '{query}' in the past month."
            
        formatted_output = f"Top {len(results)} Recent News Results for '{query}':\n\n"
        for i, res in enumerate(results):
            # The news endpoint returns a specific 'date' key!
            published_date = res.get('date', 'Unknown Date')
            
            formatted_output += (
                f"{i+1} Title: {res.get('title', 'No Title')}\n"
                f"Date Published: {published_date}\n" # <--- Now we explicitly give Qwen the date
                f"Snippet: {res.get('body', 'No Snippet available.')}\n"
                f"Source: {res.get('source', 'Unknown Source')}\n"
                f"{'-'*50}\n"
            )
            
        return formatted_output
        
    except Exception as e:
        return f"❌ Error performing news search: {str(e)}"