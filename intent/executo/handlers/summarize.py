# ------------ Create Prompt and pass it to LLM -------------------
def handle_summarize(payload, llm):
    print("[deskai] prompt initialised", flush=True)
    text = payload["text"][0]
    context = payload["text"][1]

    prompt = f"""
Summarize the following {context} content concisely.
Focus on key points only.

{text}
"""

    for chunk in llm.generate_stream(prompt):
        yield chunk
