import time
from capture.windows import get_window_under_cursor
from capture.screen import capture_active_window
from ocr.engine import run_ocr
from ocr.postprocess import lines_to_text
from context_model.infer import ContextInferencer
from daemon.state import DaemonState

POLL_INTERVAL = 1

def run_daemon():
    inferencer = ContextInferencer()
    state = DaemonState()
    last_window = None

    while True:
        win = get_window_under_cursor()
        print(win)
        if not win:
            time.sleep(POLL_INTERVAL)
            continue

        if win["window_id"] == last_window:
            time.sleep(POLL_INTERVAL)
            continue

        last_window = win["window_id"]

        capture = capture_active_window()
        if not capture:
            continue

        ocr_result = run_ocr(capture["image"])
        text = lines_to_text(ocr_result.lines)

        context = inferencer.predict(text)

        state.context = context
        state.text = text
        state.window_id = win["window_id"]

        print(
            f"[deskai] {context.label} "
            f"({context.confidence:.2f}) | "
            f"window={win['title'][:40]}"
        )

        time.sleep(POLL_INTERVAL)
