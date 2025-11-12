"""User-related endpoints (stubs).

Purpose:
- Retrieve information about the currently authenticated user.

Future behavior:
- Integrate with Flask-Login to read the session user (or JWT claims).
- Expand to include profile updates and user search/admin endpoints.
"""
from __future__ import annotations

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
