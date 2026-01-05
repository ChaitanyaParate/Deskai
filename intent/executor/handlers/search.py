import webbrowser
import urllib.parse

def handle_search(payload):
    query = payload.get("query", "")
    if not query:
        return None

    url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
    webbrowser.open(url)

    return {
        "type": "action",
        "action": "open_browser",
        "query": query
    }
