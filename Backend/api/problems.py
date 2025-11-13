

from dataclasses import asdict
from flask import Blueprint, jsonify, request

from ..entities import Problem

bp = Blueprint("problems", __name__)


@bp.get("")
def list_problems():
    items = [
        Problem(
            id=1,
            cf_id="1234A",
            title="Watermelon",
            estimated_rating=1200,
        )
    ]
    return jsonify({"items": [asdict(p) for p in items], "total": len(items)})


@bp.post("")
def create_problem():
    payload = request.get_json(silent=True) or {}
    problem = Problem(
        id=2,
        cf_id=payload.get("cf_id", "9999Z"),
        title=payload.get("title", "Demo Problem"),
        estimated_rating=1200,
    )
    return jsonify(asdict(problem)), 201


@bp.get("/<int:problem_id>")
def get_problem(problem_id: int):
    p = Problem(
        id=problem_id,
        cf_id="1234A",
        title="Watermelon",
        estimated_rating=1200,
    )
    data = asdict(p)
    # Freeze created_at for parity with previous example
    data["created_at"] = "2025-01-01T00:00:00Z"
    return jsonify(data)


@bp.get("/<int:problem_id>/estimate")
def estimate_problem(problem_id: int):
    p = Problem(id=problem_id, cf_id="1234A", title="Watermelon", estimated_rating=1350)
    return jsonify(
        {
            "problem_id": problem_id,
            "cf_id": p.cf_id,
            "estimated_rating": p.estimated_rating,
            "method": "solver-rating-distribution",
            "note": "Mocked estimate for scaffold",
            "problem": asdict(p),
        }
    )
