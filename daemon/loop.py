import time
import hashlib
import os

from capture.windows import get_window_under_cursor
from capture.screen import capture_window_under_cursor
from ocr.engine import run_ocr
from ocr.postprocess import lines_to_text
from context_model.infer import ContextInferencer
from state import shared_data

MAX_TEXT_CHARS = 1000
POLL_INTERVAL = 2.0
STREAK_REQUIRED = 2
CONF_OVERRIDE = 0.85

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---- Main OCR Loop ----

def run_daemon():
    
    print("[deskai] run_daemon started", flush=True)
    inferencer = ContextInferencer()

    time.sleep(0.3)

    last_process_time = 0.0

    while True:
        
        win = get_window_under_cursor()
        if not win or win.get("pid") is None:
            time.sleep(POLL_INTERVAL)
            continue

        now = time.time()

        with shared_data.lock:
            if win["window_id"] != shared_data.last_window_id:
                shared_data.last_window_id = win["window_id"]
                shared_data.last_window_time = now
                time.sleep(0.2)
                continue

        if now - last_process_time < POLL_INTERVAL:
            time.sleep(0.2)
            continue

        capture = capture_window_under_cursor()
        if not capture:
            time.sleep(POLL_INTERVAL)
            continue

        ocr_result = run_ocr(capture["image"])
        raw_text = lines_to_text(ocr_result.lines)
        text = raw_text[:MAX_TEXT_CHARS]
        text_hash = stable_hash(text)

        with shared_data.lock:

            if text_hash == shared_data.last_text_hash and shared_data.context:
                context = shared_data.context
            else:
                context = inferencer.predict(text)

            if shared_data.streak_label == context.label:
                shared_data.streak_count += 1
            else:
                shared_data.streak_label = context.label
                shared_data.streak_count = 1

            accept = (
                shared_data.streak_count >= STREAK_REQUIRED
                or context.confidence >= CONF_OVERRIDE
            )

            if accept:
                if not shared_data.context or shared_data.context.label != context.label:
                    print(f"[deskai] {context.label} ({context.confidence:.2f})")

                shared_data.context = context
                shared_data.text = text
                shared_data.last_text_hash = text_hash


        del ocr_result, raw_text, text
        last_process_time = now
        time.sleep(POLL_INTERVAL)

