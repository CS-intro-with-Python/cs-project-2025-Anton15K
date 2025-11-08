"""Problem-related database models."""

from __future__ import annotations

from datetime import datetime

from ..extensions import db


class Problem(db.Model):
    __tablename__ = "problems"

    id = db.Column(db.Integer, primary_key=True)
    codeforces_id = db.Column(db.String(32), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    tags = db.Column(db.JSON, nullable=True)
    estimated_rating = db.Column(db.Integer, nullable=True)
    last_updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
