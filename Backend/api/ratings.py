
from dataclasses import asdict
from flask import Blueprint, jsonify, request

from ..entities import RatingAdjustment
from ..tools import (
    calculate_performance_rating,
    calculate_time_percentile,
    calculate_actual_performance_score,
    calculate_expected_performance_score,
    calculate_rating_delta,
)

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


@bp.post("/calculate-performance")
def calculate_performance():
    """Calculate performance rating based on solve time and solver data."""
    payload = request.get_json(silent=True) or {}
    user_time = payload.get("user_time", 0)
    solvers_data = payload.get("solvers_data", [])
    
    if user_time <= 0:
        return jsonify({"error": "user_time must be positive"}), 400
    
    performance = calculate_performance_rating(user_time, solvers_data)
    percentile = calculate_time_percentile(user_time, solvers_data)
    
    return jsonify({
        "user_time": user_time,
        "performance_rating": performance,
        "time_percentile": percentile,
    })


@bp.post("/calculate-delta")
def calculate_delta():
    """Calculate rating delta based on expected vs actual performance."""
    payload = request.get_json(silent=True) or {}
    user_rating = payload.get("user_rating")
    problem_rating = payload.get("problem_rating")
    time_percentile = payload.get("time_percentile", 50.0)
    performance_rating = payload.get("performance_rating", 1500)
    
    if user_rating is None:
        return jsonify({"error": "user_rating is required"}), 400
    
    expected = calculate_expected_performance_score(user_rating, problem_rating)
    actual = calculate_actual_performance_score(time_percentile)
    delta = calculate_rating_delta(user_rating, performance_rating, expected, actual)
    
    return jsonify({
        "user_rating": user_rating,
        "problem_rating": problem_rating,
        "expected_score": expected,
        "actual_score": actual,
        "rating_delta": delta,
    })

