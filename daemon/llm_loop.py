import time
from state import shared_data
from intent.executo.handlers.explain_error import handle_explain_error


def llm_loop():
    print("[deskai] llm loop started", flush=True)

    while True:
        with shared_data.lock:
            value = shared_data.value
            text = shared_data.text
            shared_data.value = 0

        if int(value) == 1 and text:
            for chunk in handle_explain_error({"text": shared_data.text}):
                print(chunk, end="", flush=True)

        time.sleep(1.0)

