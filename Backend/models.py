"""Simple SQLAlchemy models (structure only).

These represent the core domain entities. The project does not require
persistence yet; models are defined to provide shapes for future work
and to back RESTX schemas. Foreign keys are declared but not enforced
at runtime until a real database is configured and migrations are added.
"""
from __future__ import annotations

from datetime import datetime

from .extensions import db


class User(db.Model):  # type: ignore[name-defined]
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, default=1200, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<User {self.username}>"


class Problem(db.Model):  # type: ignore[name-defined]
    __tablename__ = "problems"

    id = db.Column(db.Integer, primary_key=True)
    cf_id = db.Column(db.String(32), unique=True, nullable=False)  # Codeforces ID like 1234A
    title = db.Column(db.String(255), nullable=False)
    estimated_rating = db.Column(db.Integer, default=1200, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Problem {self.cf_id} {self.title}>"


class Attempt(db.Model):  # type: ignore[name-defined]
    __tablename__ = "attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey("problems.id"), nullable=False)

    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ended_at = db.Column(db.DateTime, nullable=True)
    duration_sec = db.Column(db.Integer, nullable=True)
    result = db.Column(db.String(32), nullable=True)  # e.g., "solved", "failed", "timeout"

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Attempt {self.id} user={self.user_id} problem={self.problem_id}>"


class RatingAdjustment(db.Model):  # type: ignore[name-defined]
    __tablename__ = "rating_adjustments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey("problems.id"), nullable=False)
    delta = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<RatingAdjustment {self.delta} for problem={self.problem_id} by user={self.user_id}>"
