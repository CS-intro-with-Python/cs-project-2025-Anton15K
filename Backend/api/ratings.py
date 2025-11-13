
from dataclasses import asdict
from flask import Blueprint, jsonify, request

from ..entities import RatingAdjustment

bp = Blueprint("ratings", __name__)


@bp.post("/adjust")
def adjust_rating():
    payload = request.get_json(silent=True) or {}
    prev = 1300
    delta = int(payload.get("delta", 0))
    new_estimate = prev + delta

    adjustment = RatingAdjustment(
        id=1,
        user_id=1,
        problem_id=int(payload.get("problem_id", 1)),
        delta=delta,
        note=payload.get("note"),
    )

    return jsonify(
        {
            "problem_id": adjustment.problem_id,
            "previous_estimate": prev,
            "new_estimate": new_estimate,
            "applied_delta": adjustment.delta,
            "adjustment": asdict(adjustment),
            "message": "Adjustment recorded (mocked)",
        }
    )
