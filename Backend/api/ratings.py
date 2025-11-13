
from flask import Blueprint, jsonify, request

bp = Blueprint("ratings", __name__)


@bp.post("/adjust")
def adjust_rating():
    payload = request.get_json(silent=True) or {}
    prev = 1300
    delta = int(payload.get("delta", 0))
    new_estimate = prev + delta
    return jsonify(
        {
            "problem_id": payload.get("problem_id", 1),
            "previous_estimate": prev,
            "new_estimate": new_estimate,
            "applied_delta": delta,
            "message": "Adjustment recorded (mocked)",
        }
    )
