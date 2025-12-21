from dataclasses import dataclass
from typing import Optional
from context_model.type import ScreenContext

@dataclass
class DaemonState:
    context: Optional[ScreenContext] = None
    text: str = ""
    window_id: Optional[str] = None
    streak_count: int = 0
    last_text_hash: Optional[int] = None
    last_context: Optional[ScreenContext] = None
    streak_label: str = ""
    last_window_id: str | None = None
    last_window_time: float = 0.0


