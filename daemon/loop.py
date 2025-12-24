import time
import hashlib
import os
from queue import Empty

from capture.windows import get_window_under_cursor
from capture.screen import capture_active_window
from ocr.engine import run_ocr
from ocr.postprocess import lines_to_text
from context_model.infer import ContextInferencer
from daemon.state import DaemonState

from intent.router.router import route_intent
from daemon.intent_worker import start_intent_worker, intent_queue, result_queue
from daemon.ipc import start_ipc_server

from intent.executo.executor import execute_intent
MAX_TEXT_CHARS = 1000
POLL_INTERVAL = 2.0
STREAK_REQUIRED = 2
CONF_OVERRIDE = 0.85

os.environ["TOKENIZERS_PARALLELISM"] = "false"

state = DaemonState()

def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

# def handle_command(cmd: str):
#     if not cmd:
#         return
#     if not state.context or not state.text:
#         print("[deskai] command ignored (no stable context yet)")
#         return

#     intent = route_intent(cmd, state.context, state.text)
#     intent_queue.put((intent, state.context))
#     print("[deskai] result queued", flush=True)

#     print(f"[deskai] intent queued: {intent.name}", flush=True)

# def handle_command(cmd):
#     if state.context is None or state.text is None:
#         return "Context not ready yet."

#     intent = route_intent(cmd, state.context, state.text)
#     intent_queue.put((intent, state.context))

#     try:
#         result = result_queue.get(timeout=80)
#     except Empty:
#         return "Intent timed out."

#     return result.get("content", "No output")

def handle_command(cmd):
    intent = route_intent(cmd, state.context, state.text)
    result = execute_intent(intent, state)

    if result is None:
        return "[deskai] No result"

    if isinstance(result, dict):
        return result.get("content", "")

    return result



def run_daemon():
    
    print("[deskai] run_daemon started", flush=True)
    inferencer = ContextInferencer()
    #start_intent_worker()
    start_ipc_server(handle_command)

    time.sleep(0.3)

    last_process_time = 0.0

    while True:
        
        win = get_window_under_cursor()
        if not win or win.get("pid") is None:
            time.sleep(POLL_INTERVAL)
            continue

        now = time.time()

        if win["window_id"] != state.last_window_id:
            state.last_window_id = win["window_id"]
            state.last_window_time = now
            time.sleep(0.2)
            continue

        if now - last_process_time < POLL_INTERVAL:
            time.sleep(0.2)
            continue

        capture = capture_active_window()
        if not capture:
            time.sleep(POLL_INTERVAL)
            continue

        ocr_result = run_ocr(capture["image"])
        raw_text = lines_to_text(ocr_result.lines)
        text = raw_text[:MAX_TEXT_CHARS]
        text_hash = stable_hash(text)

        if text_hash == state.last_text_hash and state.context:
            context = state.context
        else:
            context = inferencer.predict(text)

        if state.streak_label == context.label:
            state.streak_count += 1
        else:
            state.streak_label = context.label
            state.streak_count = 1

        accept = (
            state.streak_count >= STREAK_REQUIRED
            or context.confidence >= CONF_OVERRIDE
        )

        if accept:
            if not state.context or state.context.label != context.label:
                print(f"[deskai] {context.label} ({context.confidence:.2f})")

            state.context = context
            state.text = text
            state.last_text_hash = text_hash

        try:
            result = result_queue.get_nowait()
            print("[deskai][intent result]")
            print(result.get("content"))
        except Empty:
            pass

        del ocr_result, raw_text, text
        last_process_time = now
        time.sleep(POLL_INTERVAL)

