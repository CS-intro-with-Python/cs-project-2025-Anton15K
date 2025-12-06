
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Problem:
    id: int
    cf_id: str
    title: str
    estimated_rating: int = 1200
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    contest_id: Optional[int] = None
    problem_index: Optional[str] = None
    initial_estimated_rating: Optional[int] = None
