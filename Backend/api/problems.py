

from flask import Blueprint, jsonify, request

bp = Blueprint("problems", __name__)


@bp.get("")
def list_problems():
    items = [
        {
            "id": 1,
            "cf_id": "1234A",
            "title": "Watermelon",
            "estimated_rating": 1200,
            "created_at": "2025-01-01T00:00:00Z",
        }
    ]
    return jsonify({"items": items, "total": len(items)})


@bp.post("")
def create_problem():
    payload = request.get_json(silent=True) or {}
    return (
        jsonify(
            {
                "id": 2,
                "cf_id": payload.get("cf_id", "9999Z"),
                "title": payload.get("title", "Demo Problem"),
                "estimated_rating": 1200,
                "created_at": "2025-01-02T00:00:00Z",
            }
        ),
        201,
    )


@bp.get("/<int:problem_id>")
def get_problem(problem_id: int):
    return jsonify(
        {
            "id": problem_id,
            "cf_id": "1234A",
            "title": "Watermelon",
            "estimated_rating": 1200,
            "created_at": "2025-01-01T00:00:00Z",
        }
    )


@bp.get("/<int:problem_id>/estimate")
def estimate_problem(problem_id: int):
    return jsonify(
        {
            "problem_id": problem_id,
            "cf_id": "1234A",
            "estimated_rating": 1350,
            "method": "solver-rating-distribution",
            "note": "Mocked estimate for scaffold",
        }
    )
