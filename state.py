import threading
from typing import Optional
from context_model.type import ScreenContext

# ---- Shared Data ----
class GlobalState:
    def __init__(self):
        self.lock = threading.Lock()

        self.context: Optional[ScreenContext] = None
        self.text: str = ""

        self.value: int = 0

        self.window_id: Optional[str] = None
        self.last_window_id: Optional[str] = None
        self.last_window_time: float = 0.0

        self.streak_count: int = 0
        self.streak_label: str = ""

        self.last_text_hash: Optional[str] = None
        self.last_context: Optional[ScreenContext] = None


shared_data = GlobalState()
