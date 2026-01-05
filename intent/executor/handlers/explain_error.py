
# ------------ Create Prompt and pass it to LLM -------------------
def handle_explain_error(payload, llm):
    print("[deskai] prompt initialised", flush=True)
    text = payload["text"][0]


    prompt = f"""
    You are a debugging assistant.

    The input below is a COMPLETE error report.
    Do NOT ask follow-up questions.
    Do NOT request more information.
    Do NOT address the user.

    Your task:
    - Explain the error clearly
    - Identify the most likely root cause
    - Suggest concrete fixes

    Error report:
    {text}

    Response:
    """


    for chunk in llm.generate_stream(prompt):
        yield chunk

