from llm.factory import get_llm

_llm = None

def _get_llm():
    global _llm
    if _llm is None:
        _llm = get_llm()
    return _llm


def handle_explain_error(payload):
    print("[deskai] prompt initialised", flush=True)
    text = payload["text"]

#     prompt = f"""
# You are a debugging assistant.
# Explain the following error in simple terms.
# Suggest likely causes and fixes.

# {text}
# """

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

    llm = _get_llm()

    for chunk in llm.generate_stream(prompt):
        yield chunk
