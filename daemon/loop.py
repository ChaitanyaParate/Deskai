import time
import hashlib
import os

from capture.windows import get_window_under_cursor
from capture.screen import capture_active_window
from ocr.engine import run_ocr
from ocr.postprocess import lines_to_text
from context_model.infer import ContextInferencer
from daemon.state import DaemonState

from intent.router.router import route_intent
from intent.executo.executor import execute_intent
import sys
import select

from daemon.intent_worker import intent_worker, start_intent_worker, intent_queue, result_queue
from queue import Empty

from daemon.ipc import start_ipc_server

MAX_TEXT_CHARS = 1000
POLL_INTERVAL = 2.0
STREAK_REQUIRED = 2
CONF_OVERRIDE = 0.85

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

CMD_FIFO = "/tmp/deskai_cmd"

if not os.path.exists(CMD_FIFO):
    raise RuntimeError("FIFO /tmp/deskai_cmd does not exist")

cmd_fd = os.open(CMD_FIFO, os.O_RDONLY | os.O_NONBLOCK)


def get_user_command():
    global cmd_fd

    r, _, _ = select.select([cmd_fd], [], [], 0)
    if not r:
        return None

    data = os.read(cmd_fd, 1024).decode().strip()

    if not data:
        # writer closed, reopen FIFO
        os.close(cmd_fd)
        cmd_fd = os.open(CMD_FIFO, os.O_RDONLY | os.O_NONBLOCK)
        return None

    return data
def handle_command(cmd, state):
    intent = route_intent(cmd, state.context, state.text)
    result = execute_intent(intent, state.context)
    if result and result["type"] == "text":
        print(f"[deskai][intent:{intent.name}]")
        print(result["content"])

start_ipc_server()

def run_daemon():
    inferencer = ContextInferencer()
    state = DaemonState()
    start_intent_worker()
    last_process_time = 0.0

    while True:
        win = get_window_under_cursor()
        if not win:
            time.sleep(POLL_INTERVAL)
            continue

        if win.get("pid") is None:
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

        # ---------- prediction ----------
        if text_hash == state.last_text_hash and state.context is not None:
            context = state.context
        else:
            context = inferencer.predict(text)

        # ---------- hysteresis ----------
        if state.streak_label == context.label:
            state.streak_count += 1
        else:
            state.streak_label = context.label
            state.streak_count = 1

        accept = (
            state.streak_count >= STREAK_REQUIRED
            or context.confidence >= CONF_OVERRIDE
        )

        # ---------- accept ----------
        if accept:
            if state.context is None or state.context.label != context.label:
                print(
                    f"[deskai] {context.label} "
                    f"({context.confidence:.2f}) | "
                    f"window pid={win['pid']}"
                )

            state.context = context
            state.last_text_hash = text_hash
            state.window_id = win["window_id"]

        # ---- Check for user command ----
        cmd = get_user_command()
        
        if cmd:
            print(f"[deskai] received command: {cmd}")

            intent = route_intent(
                user_command=cmd,
                context=state.context,
                text=text
            )

            handle_command(cmd, state)
            
            print(f"[deskai] intent routed: {intent.name}")

            intent_queue.put((intent, state.context))
            print("[deskai] intent queued")

        try:
            result = result_queue.get_nowait()
        except Empty:
            result = None

        if result:
            print("[deskai][intent result]")
            print(result.get("content"))


        # ---------- cleanup ----------
        del ocr_result
        del raw_text
        del text

        last_process_time = now
        time.sleep(POLL_INTERVAL)
