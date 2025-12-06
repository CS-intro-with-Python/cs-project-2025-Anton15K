# Attempt tracking endpoints using SQLAlchemy models.

from datetime import datetime
from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models import Attempt

bp = Blueprint("attempts", __name__)


@bp.post("/start")
def start_attempt():
    payload = request.get_json(silent=True) or {}
    user_id = payload.get("user_id", 1)
    problem_id = payload.get("problem_id")

    if not problem_id:
        return jsonify({"error": "problem_id is required"}), 400

    attempt = Attempt(
        user_id=user_id,
        problem_id=problem_id,
        started_at=datetime.utcnow(),
    )
    db.session.add(attempt)
    db.session.commit()

    return jsonify({"attempt": attempt.to_dict(), "message": "Attempt started"}), 201


@bp.post("/complete")
def complete_attempt():
    payload = request.get_json(silent=True) or {}
    attempt_id = payload.get("attempt_id")

    if not attempt_id:
        return jsonify({"error": "attempt_id is required"}), 400

    attempt = Attempt.query.get(attempt_id)
    if not attempt:
        return jsonify({"error": "Attempt not found"}), 404

    attempt.ended_at = datetime.utcnow()
    if attempt.started_at:
        attempt.duration_sec = int((attempt.ended_at - attempt.started_at).total_seconds())
    attempt.result = payload.get("result", "solved")
    attempt.performance_rating = payload.get("performance_rating")
    attempt.time_percentile = payload.get("time_percentile")

    db.session.commit()

    return jsonify({"attempt": attempt.to_dict(), "message": "Attempt completed"})


@bp.get("/history")
def attempt_history():
    user_id = request.args.get("user_id", type=int)
    if user_id:
        attempts = Attempt.query.filter_by(user_id=user_id).all()
    else:
        attempts = Attempt.query.all()
    return jsonify({"items": [a.to_dict() for a in attempts], "total": len(attempts)})

