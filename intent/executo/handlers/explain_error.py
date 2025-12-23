from llm.factory import get_llm

_llm = get_llm()

def handle_explain_error(payload):

    text = payload["text"]

    prompt = f"""
    You are a debugging assistant.
    See the code and
    Explain the following error in simple terms.
    If possible, suggest likely causes and fixes.

    {text}
    """
    response = _llm.generate(prompt)

    return {
        "type": "text",
        "content": response
    }

