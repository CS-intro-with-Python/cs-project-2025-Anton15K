# Authentication endpoints using SQLAlchemy models.

from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db, create_access_token, create_refresh_token, decode_token
from ..models import User

bp = Blueprint("auth", __name__)


@bp.post("/register")
def register():
    """
    Register a new user
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
              example: johndoe
              description: Unique username
            email:
              type: string
              format: email
              example: john@example.com
              description: User's email address
            password:
              type: string
              format: password
              example: securePassword123
              description: User's password
    responses:
      201:
        description: User registered successfully
        schema:
          type: object
          properties:
            user:
              type: object
              properties:
                id:
                  type: integer
                username:
                  type: string
                email:
                  type: string
                rating:
                  type: integer
            access_token:
              type: string
              description: JWT access token
            refresh_token:
              type: string
              description: JWT refresh token for obtaining new access tokens
            expires_in:
              type: integer
              description: Token expiration time in seconds
            message:
              type: string
      400:
        description: Missing required fields
      409:
        description: Username or email already exists
    """
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

    # Generate JWT tokens
    access_token = create_access_token(user.id, {"username": user.username})
    refresh_token = create_refresh_token(user.id)

    return jsonify({
        "user": user.to_dict(),
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": current_app.config["JWT_ACCESS_TOKEN_EXPIRES"],
        "message": "Registered successfully"
    }), 201


@bp.post("/login")
def login():
    """
    Login with username and password
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: johndoe
            password:
              type: string
              format: password
              example: securePassword123
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            user:
              type: object
            access_token:
              type: string
              description: JWT access token for API authentication
            refresh_token:
              type: string
              description: JWT refresh token for obtaining new access tokens
            expires_in:
              type: integer
              description: Access token expiration time in seconds
            message:
              type: string
      400:
        description: Missing credentials
      401:
        description: Invalid credentials
    """
    payload = request.get_json(silent=True) or {}
    username = payload.get("username")
    password = payload.get("password")

    if not all([username, password]):
        return jsonify({"error": "Missing credentials"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate JWT tokens
    access_token = create_access_token(user.id, {"username": user.username})
    refresh_token = create_refresh_token(user.id)

    return jsonify({
        "user": user.to_dict(),
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": current_app.config["JWT_ACCESS_TOKEN_EXPIRES"],
        "message": "Login successful"
    })


@bp.post("/refresh")
def refresh():
    """
    Refresh access token using refresh token
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - refresh_token
          properties:
            refresh_token:
              type: string
              description: The refresh token obtained during login
    responses:
      200:
        description: Token refreshed successfully
        schema:
          type: object
          properties:
            access_token:
              type: string
              description: New JWT access token
            expires_in:
              type: integer
              description: Token expiration time in seconds
      400:
        description: Missing refresh token
      401:
        description: Invalid or expired refresh token
    """
    payload = request.get_json(silent=True) or {}
    refresh_token = payload.get("refresh_token")

    if not refresh_token:
        return jsonify({"error": "Missing refresh token"}), 400

    # Decode and validate refresh token
    token_payload = decode_token(refresh_token)
    if not token_payload:
        return jsonify({"error": "Invalid or expired refresh token"}), 401

    if token_payload.get("type") != "refresh":
        return jsonify({"error": "Invalid token type"}), 401

    # Get user from database
    user = User.query.get(int(token_payload["sub"]))
    if not user:
        return jsonify({"error": "User not found"}), 401

    # Generate new access token
    access_token = create_access_token(user.id, {"username": user.username})

    return jsonify({
        "access_token": access_token,
        "expires_in": current_app.config["JWT_ACCESS_TOKEN_EXPIRES"],
    })


@bp.post("/logout")
def logout():
    """
    Logout the current user
    ---
    tags:
      - Auth
    description: |
      Client-side logout. Since JWTs are stateless, the server doesn't maintain
      session state. To logout, simply discard the tokens on the client side.
      For enhanced security, implement token blacklisting on the server.
    responses:
      200:
        description: Logged out successfully
        schema:
          type: object
          properties:
            message:
              type: string
    """
    return jsonify({"message": "Logged out. Please discard your tokens."})



