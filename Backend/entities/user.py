
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    id: int
    username: str
    email: str
    password_hash: str
    rating: int = 1200
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
