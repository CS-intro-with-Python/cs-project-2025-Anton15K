

from dataclasses import asdict
from flask import Blueprint, jsonify

from ..entities import User

bp = Blueprint("users", __name__)


@bp.get("/me")
def get_me():
    """Return the profile of the current user (stubbed)."""
    user = User(
        id=1,
        username="alice",
        email="alice@example.com",
        password_hash="<hashed>",
        rating=1200,
    )
    user_dict = asdict(user)
    user_dict.pop("password_hash", None)
    # Freeze created_at for example parity
    user_dict["created_at"] = "2025-01-01T00:00:00Z"
    return jsonify(user_dict)
