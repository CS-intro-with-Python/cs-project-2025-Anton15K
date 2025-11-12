"""Authentication endpoints (stubs).

Purpose:
- Allow users to register, log in, and log out.
- For now, these endpoints do not implement real persistence or sessions.

Future behavior:
- Integrate with Flask-Login for session-based auth (or JWT tokens if desired).
- Persist users in the database and validate credentials securely.
- Hash passwords using a library like werkzeug.security or passlib.
"""
from __future__ import annotations

from flask import Blueprint, jsonify, request

bp = Blueprint("auth", __name__)


@bp.post("/register")
def register():
    payload = request.get_json(silent=True) or {}
    user = {
        "id": 1,
        "username": payload.get("username", "demo"),
        "email": payload.get("email", "demo@example.com"),
        "rating": 1200,
    }
    return jsonify({"user": user, "message": "Registered successfully"}), 201


@bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    user = {
        "id": 1,
        "username": payload.get("username", "alice"),
        "email": payload.get("email", "alice@example.com"),
        "rating": 1200,
    }
    return jsonify({"user": user, "token": "fake-session-token", "message": "Login successful"})


@bp.post("/logout")
def logout():
    return jsonify({"message": "Logged out"})
