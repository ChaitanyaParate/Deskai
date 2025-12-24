from intent.router.type import Intent
from context_model.type import ScreenContext

from .handlers.summarize import handle_summarize
from .handlers.explain_error import handle_explain_error
from .handlers.search import handle_search


def execute_intent(intent: Intent, state: ScreenContext):
    print(f"[deskai] worker executed")
    if intent.name == "summarize":
        return handle_summarize(intent.payload)

    if intent.name == "explain_error":
        
        return handle_explain_error({
            "text": state.text
        })

    if intent.name == "search":
        return handle_search(intent.payload)

    return None
