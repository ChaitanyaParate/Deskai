from .type import Intent
from context_model.type import ScreenContext

ERROR_KEYWORDS = [
    "error", "exception", "traceback",
    "failed", "not found", "segmentation fault"
]

def route_intent(
    user_command: str,
    context: ScreenContext,
    text: str
    ) -> Intent:

    cmd = user_command.lower().strip()

    # ---- No command ----
    if not cmd:
        return Intent("noop", {})

    # ---- Summarize ----
    if any(k in cmd for k in ["summarize", "summary", "tl;dr"]):
        return Intent(
            "summarize",
            {"text": text, "context": context.label}
        )

    # ---- Explain error ----
    if (
        context.label in ["terminal", "code_editor"]
        and any(k in text.lower() for k in ERROR_KEYWORDS)
        and any(k in cmd for k in ["explain", "why", "what happened"])
    ):
        return Intent(
            "explain_error",
            {"text": text}
        )

    # ---- Search ----
    if any(k in cmd for k in ["search", "google", "find"]):
        return Intent(
            "search",
            {"query": cmd.replace("search", "").strip()}
        )

    # ---- Default ----
    return Intent("noop", {})
