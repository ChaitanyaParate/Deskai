from ocr.types import OCRLine, OCRResult

def sort_lines(lines):
    return sorted(lines, key=lambda l: (l.bbox[1], l.bbox[0]))


def lines_to_text(lines):
    lines = sort_lines(lines)
    return "\n".join(line.text for line in lines)


def confidence_stats(lines):
    if not lines:
        return {"mean": 0, "min": 0, "max": 0}

    confs = [line.conf for line in lines]
    return {
        "mean": sum(confs) / len(confs),
        "min": min(confs),
        "max": max(confs),
    }


def normalize_text(text):
    text = text.replace("\t", " ")
    text = " ".join(text.split())
    return text
