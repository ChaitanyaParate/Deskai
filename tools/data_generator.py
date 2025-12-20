import json
import os
from capture.screen import capture_active_window
from ocr.engine import run_ocr
from ocr.types import OCRResult
import time

path = "/media/chaitanyaparate/New Volume/Programming/Python/Deep_Learning/deskai/dataset/data.json"

def append_to_json(file_path, data):
    if not isinstance(data, dict):
        raise ValueError("data must be a dictionary")

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                content = json.load(f)
            except json.JSONDecodeError:
                content = []
    else:
        content = []

    if not isinstance(content, list):
        raise ValueError("JSON file must contain a list")

    content.append(data)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)

def ocrresult_to_text(ocr: OCRResult) -> str:
    return "\n".join(line.text for line in ocr.lines)

time.sleep(2)

img = capture_active_window()

out = run_ocr(img["image"])

out = ocrresult_to_text(out)

j = {
    "text": out,
    "label": "unknown"
}

append_to_json(path, j)