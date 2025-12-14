
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

    def set_password(self, password: str):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

