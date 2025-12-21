import time
import hashlib
import os

from capture.windows import get_window_under_cursor
from capture.screen import capture_active_window
from ocr.engine import run_ocr
from ocr.postprocess import lines_to_text
from context_model.infer import ContextInferencer
from daemon.state import DaemonState

MAX_TEXT_CHARS = 1000
POLL_INTERVAL = 2.0
STREAK_REQUIRED = 2
CONF_OVERRIDE = 0.85

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def run_daemon():
    inferencer = ContextInferencer()
    state = DaemonState()
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

        # ---------- cleanup ----------
        del ocr_result
        del raw_text
        del text

        last_process_time = now
        time.sleep(POLL_INTERVAL)
