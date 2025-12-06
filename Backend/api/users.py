# User management endpoints using SQLAlchemy models.

from flask import Blueprint, jsonify

from ..models import User

bp = Blueprint("users", __name__)


@bp.get("/me")
def get_me():
    """Return the profile of a demo user (first user in DB or mock)."""
    user = User.query.first()
    if not user:
        return jsonify({
            "id": 0,
            "username": "guest",
            "email": "guest@example.com",
            "rating": 1200,
            "created_at": "2025-01-01T00:00:00Z"
        })
    return jsonify(user.to_dict())


@bp.get("")
def list_users():
    """List all users."""
    users = User.query.all()
    return jsonify({"items": [u.to_dict() for u in users], "total": len(users)})

