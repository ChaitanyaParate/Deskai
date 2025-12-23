from intent.router.type import Intent
from context_model.type import ScreenContext

from .handlers.summarize import handle_summarize
from .handlers.explain_error import handle_explain_error
from .handlers.search import handle_search


def execute_intent(intent: Intent, context: ScreenContext):
    if intent.name == "summarize":
        return handle_summarize(intent.payload)

    if intent.name == "explain_error":
        return handle_explain_error(intent.payload)

    if intent.name == "search":
        return handle_search(intent.payload)

    return None
