
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Problem:
    id: int
    cf_id: str
    title: str
    estimated_rating: int = 1200
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
