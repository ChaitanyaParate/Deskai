from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class Intent:
    name: str
    payload: Dict[str, Any]
