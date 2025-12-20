import cv2
import pytesseract
from collections import defaultdict
from ocr.types import BBox, OCRLine, OCRResult, OCRWord


def run_ocr(image, config="--oem 3 --psm 6", lang="eng") -> OCRResult:
    if image is None or image.ndim != 3:
        return OCRResult(lines=[])

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(
        gray,
        output_type=pytesseract.Output.DICT,
        lang=lang,
        config=config
    )

    grouped_words = defaultdict(list)
    n = len(data["text"])

    for i in range(n):
        text = data["text"][i].strip()
        if not text:
            continue

        try:
            conf = float(data["conf"][i])
        except ValueError:
            continue

        bbox: BBox = (
            data["left"][i],
            data["top"][i],
            data["width"][i],
            data["height"][i],
        )

        word = OCRWord(
            text=text,
            conf=conf,
            bbox=bbox
        )

        line_id = (
            data["page_num"][i],
            data["block_num"][i],
            data["par_num"][i],
            data["line_num"][i],
        )

        grouped_words[line_id].append(word)

    lines = []

    for words in grouped_words.values():
        words = sorted(words, key=lambda w: w.bbox[0])

        x1 = min(w.bbox[0] for w in words)
        y1 = min(w.bbox[1] for w in words)
        x2 = max(w.bbox[0] + w.bbox[2] for w in words)
        y2 = max(w.bbox[1] + w.bbox[3] for w in words)

        line_bbox: BBox = (x1, y1, x2 - x1, y2 - y1)

        line_text = " ".join(w.text for w in words)
        line_conf = sum(w.conf for w in words) / len(words)

        lines.append(
            OCRLine(
                text=line_text,
                conf=line_conf,
                bbox=line_bbox,
                words=words
            )
        )

    return OCRResult(lines=lines)


