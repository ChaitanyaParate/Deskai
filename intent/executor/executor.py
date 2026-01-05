from context_model.type import ScreenContext

from .handlers.summarize import handle_summarize
from .handlers.explain_error import handle_explain_error
from .handlers.search import handle_search

from llm.factory import get_llm
# ------------ Deside Behavior -------------------
_llm = None

def _get_llm():
    global _llm
    if _llm is None:
        _llm = get_llm()
    return _llm

def execute_intent(intent, context):
    print(f"[deskai] worker executed")
    llm = _get_llm()
    if intent == "summarize":

        for chunk in handle_summarize(context, llm):
            yield chunk

    if intent == "explain_error":
        
        for chunk in handle_explain_error(context, llm):
            yield chunk

    if intent == "search":

        for chunk in handle_search(context, llm):
            yield chunk

    return None
