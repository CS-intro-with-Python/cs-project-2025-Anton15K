

from datetime import datetime

from flask import Blueprint, jsonify, request

bp = Blueprint("attempts", __name__)


@bp.post("/start")
def start_attempt():
    payload = request.get_json(silent=True) or {}
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
    return jsonify({"attempt": attempt, "message": "Attempt started"}), 201


@bp.post("/complete")
def complete_attempt():
    payload = request.get_json(silent=True) or {}
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
    return jsonify({"attempt": attempt, "message": "Attempt completed"})


@bp.get("/history")
def attempt_history():
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
    return jsonify({"items": items, "total": len(items)})
