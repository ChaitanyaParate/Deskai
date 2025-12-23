def handle_summarize(payload):
    text = payload["text"]
    context = payload.get("context", "unknown")

    prompt = f"""
Summarize the following {context} content concisely.
Focus on key points only.

{text}
"""

    # LLM call
    return {
        "type": "text",
        "content": prompt.strip()
    }
