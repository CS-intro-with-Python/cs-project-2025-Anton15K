# Codeforces API integration endpoints for fetching user/problem data and analyzing solver performance.

from flask import Blueprint, jsonify, request

from ..tools import (
    get_user_info,
    get_problem_info,
    check_submission,
    get_solvers_for_problem,
    estimate_problem_difficulty,
)

bp = Blueprint("codeforces", __name__)


@bp.get("/user/<handle>")
def get_cf_user(handle: str):
    user_data = get_user_info(handle)
    if user_data is None:
        return jsonify({"error": "User not found or API error"}), 404
    return jsonify(user_data)


@bp.get("/problem/<int:contest_id>/<index>")
def get_cf_problem(contest_id: int, index: str):
    problem_data = get_problem_info(contest_id, index)
    if problem_data is None:
        return jsonify({"error": "Problem not found or API error"}), 404
    return jsonify(problem_data)


@bp.get("/problem/<int:contest_id>/<index>/analyze")
def analyze_problem(contest_id: int, index: str):
    solver_data = get_solvers_for_problem(contest_id, index)
    
    if not solver_data.get("solvers"):
        return jsonify({
            "contest_id": contest_id,
            "problem_index": index,
            "error": "No solver data available",
            "estimated_difficulty": 1500,
        }), 200
    
    estimated_difficulty = estimate_problem_difficulty(solver_data["solvers"])
    
    return jsonify({
        "contest_id": contest_id,
        "problem_index": index,
        "estimated_difficulty": estimated_difficulty,
        "solver_count": len(solver_data["solvers"]),
        "participant_count": len(solver_data["all_participants"]),
    })


@bp.post("/check-submission")
def check_cf_submission():
    payload = request.get_json(silent=True) or {}
    handle = payload.get("handle")
    contest_id = payload.get("contest_id")
    index = payload.get("index")
    
    if not all([handle, contest_id, index]):
        return jsonify({"error": "Missing required fields: handle, contest_id, index"}), 400
    
    solved, submission = check_submission(handle, contest_id, index)
    
    return jsonify({
        "handle": handle,
        "contest_id": contest_id,
        "index": index,
        "solved": solved,
        "submission": submission,
    })
