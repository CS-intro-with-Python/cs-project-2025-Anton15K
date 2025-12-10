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
    """
    Get Codeforces user information
    ---
    tags:
      - Codeforces
    parameters:
      - in: path
        name: handle
        type: string
        required: true
        description: Codeforces handle
        example: tourist
    responses:
      200:
        description: User information
        schema:
          type: object
          properties:
            handle:
              type: string
            rating:
              type: integer
            rank:
              type: string
            maxRating:
              type: integer
      404:
        description: User not found
    """
    user_data = get_user_info(handle)
    if user_data is None:
        return jsonify({"error": "User not found or API error"}), 404
    return jsonify(user_data)


@bp.get("/problem/<int:contest_id>/<index>")
def get_cf_problem(contest_id: int, index: str):
    """
    Get Codeforces problem information
    ---
    tags:
      - Codeforces
    parameters:
      - in: path
        name: contest_id
        type: integer
        required: true
        description: Contest ID
        example: 1234
      - in: path
        name: index
        type: string
        required: true
        description: Problem index
        example: A
    responses:
      200:
        description: Problem information
        schema:
          type: object
          properties:
            contestId:
              type: integer
            index:
              type: string
            name:
              type: string
            rating:
              type: integer
      404:
        description: Problem not found
    """
    problem_data = get_problem_info(contest_id, index)
    if problem_data is None:
        return jsonify({"error": "Problem not found or API error"}), 404
    return jsonify(problem_data)


@bp.get("/problem/<int:contest_id>/<index>/analyze")
def analyze_problem(contest_id: int, index: str):
    """
    Analyze problem difficulty from solver data
    ---
    tags:
      - Codeforces
    parameters:
      - in: path
        name: contest_id
        type: integer
        required: true
        example: 1234
      - in: path
        name: index
        type: string
        required: true
        example: A
    responses:
      200:
        description: Problem analysis
        schema:
          type: object
          properties:
            contest_id:
              type: integer
            problem_index:
              type: string
            estimated_difficulty:
              type: integer
            solver_count:
              type: integer
            participant_count:
              type: integer
    """
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
    """
    Check if user solved a problem on Codeforces
    ---
    tags:
      - Codeforces
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - handle
            - contest_id
            - index
          properties:
            handle:
              type: string
              example: tourist
              description: Codeforces handle
            contest_id:
              type: integer
              example: 1234
            index:
              type: string
              example: A
    responses:
      200:
        description: Submission check result
        schema:
          type: object
          properties:
            handle:
              type: string
            contest_id:
              type: integer
            index:
              type: string
            solved:
              type: boolean
            submission:
              type: object
              description: Submission details if found
      400:
        description: Missing required fields
    """
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

