# Authentication endpoints using SQLAlchemy models.

from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from ..models import User

bp = Blueprint("auth", __name__)


@bp.post("/register")
def register():
    payload = request.get_json(silent=True) or {}
    username = payload.get("username")
    email = payload.get("email")
    password = payload.get("password")

    if not all([username, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    existing = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing:
        return jsonify({"error": "Username or email already exists"}), 409

    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"user": user.to_dict(), "message": "Registered successfully"}), 201


@bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    username = payload.get("username")
    password = payload.get("password")

    if not all([username, password]):
        return jsonify({"error": "Missing credentials"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "user": user.to_dict(),
        "token": "session-token-placeholder",
        "message": "Login successful"
    })


@bp.post("/logout")
def logout():
    return jsonify({"message": "Logged out"})

