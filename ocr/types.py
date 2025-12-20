from dataclasses import dataclass
from typing import List, Tuple

BBox = Tuple[int, int, int, int]  

@dataclass(frozen=True)
class OCRWord:
    text: str
    conf: float
    bbox: BBox

@dataclass(frozen=True)
class OCRLine:
    text: str
    conf: float
    bbox: BBox
    words: List[OCRWord]


@dataclass(frozen=True)
class OCRResult:
    lines: List[OCRLine]
