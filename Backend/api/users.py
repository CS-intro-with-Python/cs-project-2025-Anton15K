

from flask import Blueprint, jsonify

bp = Blueprint("users", __name__)


@bp.get("/me")
def get_me():
    """Return the profile of the current user (stubbed)."""
    return jsonify(
        {
            "id": 1,
            "username": "alice",
            "email": "alice@example.com",
            "rating": 1200,
            "created_at": "2025-01-01T00:00:00Z",
        }
    )
