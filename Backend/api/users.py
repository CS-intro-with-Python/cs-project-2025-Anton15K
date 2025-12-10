# User management endpoints using SQLAlchemy models.

from flask import Blueprint, jsonify, g

from ..models import User
from ..extensions import token_required

bp = Blueprint("users", __name__)


@bp.get("/me")
@token_required
def get_me():
    """
    Get current authenticated user profile
    ---
    tags:
      - Users
    security:
      - Bearer: []
    responses:
      200:
        description: User profile
        schema:
          type: object
          properties:
            id:
              type: integer
            username:
              type: string
            email:
              type: string
            cf_handle:
              type: string
              description: Codeforces handle
            rating:
              type: integer
            created_at:
              type: string
              format: date-time
      401:
        description: Missing or invalid token
    """
    return jsonify(g.current_user.to_dict())


@bp.get("")
def list_users():
    """
    List all users
    ---
    tags:
      - Users
    responses:
      200:
        description: List of all users
        schema:
          type: object
          properties:
            items:
              type: array
              items:
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
            total:
              type: integer
    """
    users = User.query.all()
    return jsonify({"items": [u.to_dict() for u in users], "total": len(users)})


