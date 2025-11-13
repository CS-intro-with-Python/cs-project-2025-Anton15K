
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class RatingAdjustment:
    id: int
    user_id: int
    problem_id: int
    delta: int
    note: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
