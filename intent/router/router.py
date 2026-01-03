# ------------ Checks Commands -------------------

def route_intent(user_command, context):

    cmd = user_command.lower().strip()

    # ---- No command ----
    if not cmd:
        return "Noop"

    # ---- Summarize ----
    elif cmd in ["summarize", "summary"]:
        return "summarize"
    
    # ---- Search ----
    elif cmd in ["search", "google", "find"]:
        return [
            "search",
            {"query": cmd.replace("search", "").strip()}
        ]

    # ---- Explain error ----
    if (context.label in ["terminal", "code_editor"] and cmd in ["explain_error", "explain", "explain error", "error"]):
        return "explain_error"


    # ---- Default ----
    return "Noop"
