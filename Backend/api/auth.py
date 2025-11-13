

from dataclasses import asdict
from flask import Blueprint, jsonify, request

from ..entities import User

bp = Blueprint("auth", __name__)


@bp.post("/register")
def register():
    payload = request.get_json(silent=True) or {}
    user = User(
        id=1,
        username=payload.get("username", "demo"),
        email=payload.get("email", "demo@example.com"),
        password_hash="<hashed>",
    )
    user_dict = asdict(user)
    # Never expose password hash
    user_dict.pop("password_hash", None)
    return jsonify({"user": user_dict, "message": "Registered successfully"}), 201


@bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    user = User(
        id=1,
        username=payload.get("username", "alice"),
        email=payload.get("email", "alice@example.com"),
        password_hash="<hashed>",
    )
    user_dict = asdict(user)
    user_dict.pop("password_hash", None)
    return jsonify({"user": user_dict, "token": "fake-session-token", "message": "Login successful"})


@bp.post("/logout")
def logout():
    return jsonify({"message": "Logged out"})
