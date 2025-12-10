
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
    """
    Adjust a user's rating
    ---
    tags:
      - Ratings
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            problem_id:
              type: integer
              example: 1
            delta:
              type: integer
              example: 25
              description: Rating change amount
            note:
              type: string
              example: "Solved problem faster than expected"
    responses:
      200:
        description: Rating adjusted
        schema:
          type: object
          properties:
            problem_id:
              type: integer
            previous_estimate:
              type: integer
            new_estimate:
              type: integer
            applied_delta:
              type: integer
            message:
              type: string
    """
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
    """
    Calculate performance rating based on solve time
    ---
    tags:
      - Ratings
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - user_time
          properties:
            user_time:
              type: integer
              example: 1200
              description: Solve time in seconds
            solvers_data:
              type: array
              items:
                type: object
              description: Array of solver data with their times and ratings
    responses:
      200:
        description: Performance calculated
        schema:
          type: object
          properties:
            user_time:
              type: integer
            performance_rating:
              type: integer
            time_percentile:
              type: number
              format: float
      400:
        description: Invalid user_time
    """
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
    """
    Calculate rating delta based on expected vs actual performance
    ---
    tags:
      - Ratings
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - user_rating
          properties:
            user_rating:
              type: integer
              example: 1500
              description: Current user rating
            problem_rating:
              type: integer
              example: 1600
              description: Problem difficulty rating
            time_percentile:
              type: number
              format: float
              example: 75.0
            performance_rating:
              type: integer
              example: 1650
    responses:
      200:
        description: Delta calculated
        schema:
          type: object
          properties:
            user_rating:
              type: integer
            problem_rating:
              type: integer
            expected_score:
              type: number
            actual_score:
              type: number
            rating_delta:
              type: integer
      400:
        description: Missing user_rating
    """
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


