from dataclasses import dataclass
from typing import Optional
from context_model.type import ScreenContext

@dataclass
class DaemonState:
    context: Optional[ScreenContext] = None
    text: str = ""
    window_id: Optional[str] = None
