from llm.factory import get_llm

_llm = None

def _get_llm():
    global _llm
    if _llm is None:
        _llm = get_llm()
    return _llm


def handle_explain_error(payload):
    text = payload["text"]

    prompt = f"""
You are a debugging assistant.
Explain the following error in simple terms.
Suggest likely causes and fixes.

{text}
"""

    llm = _get_llm()

    for chunk in llm.generate_stream(prompt):
        yield chunk
