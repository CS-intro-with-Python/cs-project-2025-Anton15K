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

from flask_restx import Namespace, Resource, fields

ns = Namespace("auth", description="User registration and authentication")

# Request/Response Schemas
register_req = ns.model(
    "RegisterRequest",
    {
        "username": fields.String(required=True, description="Unique username"),
        "email": fields.String(required=True, description="User email address"),
        "password": fields.String(required=True, description="Plain password (to be hashed)")
    },
)

user_model = ns.model(
    "User",
    {
        "id": fields.Integer(example=1),
        "username": fields.String(example="alice"),
        "email": fields.String(example="alice@example.com"),
        "rating": fields.Integer(example=1200),
    },
)

register_resp = ns.model(
    "RegisterResponse",
    {
        "user": fields.Nested(user_model),
        "message": fields.String(example="Registered successfully"),
    },
)

login_req = ns.model(
    "LoginRequest",
    {
        "username": fields.String(required=False, description="Username (or email)"),
        "email": fields.String(required=False, description="Email (alternative to username)"),
        "password": fields.String(required=True, description="Plain password"),
    },
)

login_resp = ns.model(
    "LoginResponse",
    {
        "user": fields.Nested(user_model),
        "token": fields.String(example="fake-session-token"),
        "message": fields.String(example="Login successful"),
    },
)

logout_resp = ns.model(
    "LogoutResponse",
    {"message": fields.String(example="Logged out")},
)


@ns.route("/register")
class RegisterResource(Resource):
    @ns.expect(register_req, validate=True)
    @ns.marshal_with(register_resp, code=201)
    @ns.doc(description="Create a new user account. In the future, this will store the user in the DB and return the created user.")
    def post(self):
        payload = ns.payload or {}
        user = {
            "id": 1,
            "username": payload.get("username", "demo"),
            "email": payload.get("email", "demo@example.com"),
            "rating": 1200,
        }
        return {"user": user, "message": "Registered successfully"}, 201


@ns.route("/login")
class LoginResource(Resource):
    @ns.expect(login_req, validate=True)
    @ns.marshal_with(login_resp)
    @ns.doc(description="Authenticate a user. Will validate credentials and initiate a session or return a token in the future.")
    def post(self):
        user = {
            "id": 1,
            "username": (ns.payload or {}).get("username", "alice"),
            "email": (ns.payload or {}).get("email", "alice@example.com"),
            "rating": 1200,
        }
        return {"user": user, "token": "fake-session-token", "message": "Login successful"}


@ns.route("/logout")
class LogoutResource(Resource):
    @ns.marshal_with(logout_resp)
    @ns.doc(description="Terminate the current session. Future implementation will clear the user session or invalidate the token.")
    def post(self):
        return {"message": "Logged out"}
