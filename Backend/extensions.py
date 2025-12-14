
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, jsonify, request, g
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# CORS for browser clients (permissive by default now)
cors = CORS()

# SQLAlchemy for database ORM
db = SQLAlchemy()



# JWT Utility Functions
def create_access_token(user_id: int, additional_claims: dict = None) -> str:
    """
    Create a JWT access token for the given user.
    
    Args:
        user_id: The user's ID
        additional_claims: Optional additional claims to include in the token
    
    Returns:
        Encoded JWT token string
    """
    expires_delta = timedelta(seconds=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"])
    expire = datetime.now(timezone.utc) + expires_delta
    
    payload = {
        "sub": str(user_id),
        "iat": datetime.now(timezone.utc),
        "exp": expire,
        "type": "access",
    }
    
    if additional_claims:
        payload.update(additional_claims)
    
    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm=current_app.config["JWT_ALGORITHM"],
    )


def create_refresh_token(user_id: int) -> str:
    """
    Create a JWT refresh token for the given user.
    
    Args:
        user_id: The user's ID
    
    Returns:
        Encoded JWT refresh token string
    """
    expires_delta = timedelta(seconds=current_app.config["JWT_REFRESH_TOKEN_EXPIRES"])
    expire = datetime.now(timezone.utc) + expires_delta
    
    payload = {
        "sub": str(user_id),
        "iat": datetime.now(timezone.utc),
        "exp": expire,
        "type": "refresh",
    }
    
    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm=current_app.config["JWT_ALGORITHM"],
    )


def decode_token(token: str) -> dict | None:
    """
    Decode and validate a JWT token.
    
    Args:
        token: The JWT token string
    
    Returns:
        Decoded token payload dict, or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config["JWT_SECRET_KEY"],
            algorithms=[current_app.config["JWT_ALGORITHM"]],
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    """
    Decorator to protect routes with JWT authentication.
    
    The current user will be available as g.current_user in the decorated function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]
        
        if not token:
            return jsonify({"error": "Missing authorization token"}), 401
        
        # Decode and validate token
        payload = decode_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        if payload.get("type") != "access":
            return jsonify({"error": "Invalid token type"}), 401
        
        # Get user from database
        from .models import User
        user = db.session.get(User, int(payload["sub"]))
        if not user:
            return jsonify({"error": "User not found"}), 401
        
        # Store user in g for access in the route
        g.current_user = user
        
        return f(*args, **kwargs)
    
    return decorated

