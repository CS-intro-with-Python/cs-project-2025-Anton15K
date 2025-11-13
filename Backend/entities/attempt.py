
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Attempt:
    id: int
    user_id: int
    problem_id: int
    started_at: str = field(default_factory=lambda: datetime.now().isoformat() + "Z")
    ended_at: Optional[str] = None
    duration_sec: Optional[int] = None
    result: Optional[str] = None  # e.g., "solved", "failed", "timeout"
