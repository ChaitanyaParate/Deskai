from dataclasses import dataclass, field
from typing import Optional
from context_model.type import ScreenContext
import threading

@dataclass
class GlobalState:
    context: Optional[ScreenContext] = None
    text: str = ""

    window_id: Optional[str] = None
    last_window_id: Optional[str] = None
    last_window_time: float = 0.0

    streak_count: int = 0
    streak_label: str = ""

    last_text_hash: Optional[str] = None
    last_context: Optional[ScreenContext] = None

    lock: threading.Lock = field(default_factory=threading.Lock)
