"""Attempt-related endpoints (stubs).

Purpose:
- Start and complete a problem-solving attempt with a simple timer.
- Fetch recent attempt history for the current user.

Future behavior:
- Persist attempts and compute durations on the server.
- Enforce authentication and associate attempts with the real user id.
"""
from __future__ import annotations

from datetime import datetime

from flask_restx import Namespace, Resource, fields

ns = Namespace("attempts", description="Start/complete attempts and view history")

attempt_model = ns.model(
    "Attempt",
    {
        "id": fields.Integer(example=1),
        "user_id": fields.Integer(example=1),
        "problem_id": fields.Integer(example=42),
        "started_at": fields.String(example="2025-01-01T12:00:00Z"),
        "ended_at": fields.String(example="2025-01-01T12:30:00Z", nullable=True),
        "duration_sec": fields.Integer(example=1800, nullable=True),
        "result": fields.String(example="solved", description="solved|failed|timeout"),
    },
)

start_req = ns.model(
    "StartAttemptRequest",
    {
        "problem_id": fields.Integer(required=True, description="Internal problem id"),
    },
)

start_resp = ns.model(
    "StartAttemptResponse",
    {
        "attempt": fields.Nested(attempt_model),
        "message": fields.String(example="Attempt started"),
    },
)

complete_req = ns.model(
    "CompleteAttemptRequest",
    {
        "attempt_id": fields.Integer(required=True),
        "result": fields.String(required=True, description="solved|failed|timeout"),
        "ended_at": fields.String(required=False, description="ISO time; server may override"),
    },
)

complete_resp = ns.model(
    "CompleteAttemptResponse",
    {
        "attempt": fields.Nested(attempt_model),
        "message": fields.String(example="Attempt completed"),
    },
)

history_resp = ns.model(
    "AttemptHistoryResponse",
    {
        "items": fields.List(fields.Nested(attempt_model)),
        "total": fields.Integer(example=1),
    },
)


@ns.route("/start")
class StartAttempt(Resource):
    @ns.expect(start_req, validate=True)
    @ns.marshal_with(start_resp, code=201)
    @ns.doc(description="Start a new attempt for the given problem. Associates attempt with current user (stubbed).")
    def post(self):
        payload = ns.payload or {}
        now = datetime.utcnow().isoformat() + "Z"
        attempt = {
            "id": 100,
            "user_id": 1,  # would come from session
            "problem_id": payload.get("problem_id", 42),
            "started_at": now,
            "ended_at": None,
            "duration_sec": None,
            "result": None,
        }
        return {"attempt": attempt, "message": "Attempt started"}, 201


@ns.route("/complete")
class CompleteAttempt(Resource):
    @ns.expect(complete_req, validate=True)
    @ns.marshal_with(complete_resp)
    @ns.doc(description="Complete an existing attempt and record the result and duration (mocked).")
    def post(self):
        payload = ns.payload or {}
        ended = payload.get("ended_at") or (datetime.utcnow().isoformat() + "Z")
        attempt = {
            "id": payload.get("attempt_id", 100),
            "user_id": 1,
            "problem_id": 42,
            "started_at": "2025-01-01T12:00:00Z",
            "ended_at": ended,
            "duration_sec": 1800,
            "result": payload.get("result", "solved"),
        }
        return {"attempt": attempt, "message": "Attempt completed"}


@ns.route("/history")
class AttemptHistory(Resource):
    @ns.marshal_with(history_resp)
    @ns.doc(description="Return recent attempts for the current user.")
    def get(self):
        items = [
            {
                "id": 100,
                "user_id": 1,
                "problem_id": 42,
                "started_at": "2025-01-01T12:00:00Z",
                "ended_at": "2025-01-01T12:30:00Z",
                "duration_sec": 1800,
                "result": "solved",
            }
        ]
        return {"items": items, "total": len(items)}
