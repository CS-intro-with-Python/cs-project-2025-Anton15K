"""User-related endpoints (stubs).

Purpose:
- Retrieve information about the currently authenticated user.

Future behavior:
- Integrate with Flask-Login to read the session user (or JWT claims).
- Expand to include profile updates and user search/admin endpoints.
"""
from __future__ import annotations

from flask_restx import Namespace, Resource, fields

ns = Namespace("users", description="User profile and account operations")

user_model = ns.model(
    "User",
    {
        "id": fields.Integer(example=1),
        "username": fields.String(example="alice"),
        "email": fields.String(example="alice@example.com"),
        "rating": fields.Integer(example=1200),
        "created_at": fields.String(example="2025-01-01T00:00:00Z"),
    },
)


@ns.route("/me")
class MeResource(Resource):
    @ns.doc(
        description=(
            "Return the profile of the current user. In the future this will "
            "use session or token authentication to identify the caller."
        )
    )
    @ns.marshal_with(user_model)
    def get(self):
        # Stubbed response; not using real auth yet
        return {
            "id": 1,
            "username": "alice",
            "email": "alice@example.com",
            "rating": 1200,
            "created_at": "2025-01-01T00:00:00Z",
        }
