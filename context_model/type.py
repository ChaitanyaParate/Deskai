from dataclasses import dataclass


@dataclass(frozen=True)
class ScreenContext:
    label: str        # terminal | code_editor | browser | pdf | unknown
    confidence: float # 0.0 – 1.0
