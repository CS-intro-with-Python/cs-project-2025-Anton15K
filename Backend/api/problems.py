# Problem management endpoints using SQLAlchemy models.

from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models import Problem
from ..tools import estimate_problem_difficulty, get_solvers_for_problem

bp = Blueprint("problems", __name__)


@bp.get("")
def list_problems():
    problems = Problem.query.all()
    return jsonify({"items": [p.to_dict() for p in problems], "total": len(problems)})


@bp.post("")
def create_problem():
    payload = request.get_json(silent=True) or {}
    problem = Problem(
        cf_id=payload.get("cf_id", "9999Z"),
        title=payload.get("title", "Demo Problem"),
        contest_id=payload.get("contest_id"),
        problem_index=payload.get("problem_index"),
        estimated_rating=payload.get("estimated_rating", 1200),
    )
    db.session.add(problem)
    db.session.commit()
    return jsonify(problem.to_dict()), 201


@bp.get("/<int:problem_id>")
def get_problem(problem_id: int):
    problem = Problem.query.get(problem_id)
    if not problem:
        return jsonify({"error": "Problem not found"}), 404
    return jsonify(problem.to_dict())


@bp.get("/<int:problem_id>/estimate")
def estimate_problem(problem_id: int):
    problem = Problem.query.get(problem_id)
    if not problem:
        return jsonify({"error": "Problem not found"}), 404

    return jsonify({
        "problem_id": problem_id,
        "cf_id": problem.cf_id,
        "estimated_rating": problem.estimated_rating,
        "method": "stored",
        "problem": problem.to_dict(),
    })


@bp.post("/<int:problem_id>/estimate-from-cf")
def estimate_from_codeforces(problem_id: int):
    """Estimate problem difficulty using live Codeforces solver data."""
    payload = request.get_json(silent=True) or {}
    contest_id = payload.get("contest_id")
    problem_index = payload.get("problem_index")

    if not contest_id or not problem_index:
        return jsonify({"error": "contest_id and problem_index are required"}), 400

    solver_data = get_solvers_for_problem(contest_id, problem_index)

    if not solver_data.get("solvers"):
        return jsonify({
            "problem_id": problem_id,
            "estimated_rating": 1500,
            "method": "default",
            "note": "No solver data available from Codeforces",
        })

    estimated = estimate_problem_difficulty(solver_data["solvers"])

    # Update problem in database if it exists
    problem = Problem.query.get(problem_id)
    if problem:
        problem.estimated_rating = estimated
        problem.initial_estimated_rating = estimated
        db.session.commit()

    return jsonify({
        "problem_id": problem_id,
        "contest_id": contest_id,
        "problem_index": problem_index,
        "estimated_rating": estimated,
        "solver_count": len(solver_data["solvers"]),
        "method": "solver-rating-distribution",
    })


