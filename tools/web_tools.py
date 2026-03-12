from duckduckgo_search import DDGS

from tools.base import Tool

MAX_RESULTS = 5


def web_search(query: str) -> str:
    """Busca en internet usando DuckDuckGo y devuelve los resultados."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=MAX_RESULTS))
    except Exception as e:
        return f"Error during web search: {e}"

    if not results:
        return "No results found."

    output = []
    for i, r in enumerate(results, 1):
        title = r.get("title", "")
        body = r.get("body", "")
        url = r.get("href", "")
        output.append(f"{i}. {title}\n   {body}\n   URL: {url}")

    return "\n\n".join(output)


web_search_tool = Tool(
    name="web_search",
    description="Search the internet using DuckDuckGo. Returns the top results with title, snippet and URL.",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query.",
            }
        },
        "required": ["query"],
    },
    function=web_search,
)
