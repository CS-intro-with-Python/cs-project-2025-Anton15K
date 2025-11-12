"""Problem-related endpoints (stubs).

Purpose:
- List Codeforces problems known to the system.
- Create placeholder problems for local testing.
- Retrieve a single problem by id.
- Provide an estimated rating for a problem (mocked for now).

Future behavior:
- Persist problems and compute ratings from solver statistics.
- Sync metadata from Codeforces API.
"""
from __future__ import annotations

from flask_restx import Namespace, Resource, fields

ns = Namespace("problems", description="Problem catalog and rating estimates")

problem_model = ns.model(
    "Problem",
    {
        "id": fields.Integer(example=1),
        "cf_id": fields.String(example="1234A", description="Codeforces problem identifier"),
        "title": fields.String(example="Watermelon"),
        "estimated_rating": fields.Integer(example=1200),
        "created_at": fields.String(example="2025-01-01T00:00:00Z"),
    },
)

create_problem_req = ns.model(
    "CreateProblemRequest",
    {
        "cf_id": fields.String(required=True),
        "title": fields.String(required=True),
    },
)

estimate_model = ns.model(
    "Estimate",
    {
        "problem_id": fields.Integer(example=1),
        "cf_id": fields.String(example="1234A"),
        "estimated_rating": fields.Integer(example=1350),
        "method": fields.String(example="solver-rating-distribution"),
        "note": fields.String(example="Mocked estimate for scaffold"),
    },
)

list_model = ns.model(
    "ProblemList",
    {
        "items": fields.List(fields.Nested(problem_model)),
        "total": fields.Integer(example=1),
    },
)


@ns.route("")
class ProblemsCollection(Resource):
    @ns.marshal_with(list_model)
    @ns.doc(description="Return a paginated list of problems. Pagination params may be added later.")
    def get(self):
        items = [
            {
                "id": 1,
                "cf_id": "1234A",
                "title": "Watermelon",
                "estimated_rating": 1200,
                "created_at": "2025-01-01T00:00:00Z",
            }
        ]
        return {"items": items, "total": len(items)}

    @ns.expect(create_problem_req, validate=True)
    @ns.marshal_with(problem_model, code=201)
    @ns.doc(description="Create a placeholder problem entry. Future: store in DB, deduplicate by cf_id.")
    def post(self):
        payload = ns.payload or {}
        return {
            "id": 2,
            "cf_id": payload.get("cf_id", "9999Z"),
            "title": payload.get("title", "Demo Problem"),
            "estimated_rating": 1200,
            "created_at": "2025-01-02T00:00:00Z",
        }, 201


@ns.route("/<int:problem_id>")
@ns.param("problem_id", "Internal problem id")
class ProblemResource(Resource):
    @ns.marshal_with(problem_model)
    @ns.doc(description="Retrieve a problem by internal id.")
    def get(self, problem_id: int):
        return {
            "id": problem_id,
            "cf_id": "1234A",
            "title": "Watermelon",
            "estimated_rating": 1200,
            "created_at": "2025-01-01T00:00:00Z",
        }


@ns.route("/<int:problem_id>/estimate")
@ns.param("problem_id", "Internal problem id")
class ProblemEstimateResource(Resource):
    @ns.marshal_with(estimate_model)
    @ns.doc(
        description=(
            "Return a mocked rating estimate for the given problem. In the future, "
            "this will analyze solver ratings/time and user performance data."
        )
    )
    def get(self, problem_id: int):
        return {
            "problem_id": problem_id,
            "cf_id": "1234A",
            "estimated_rating": 1350,
            "method": "solver-rating-distribution",
            "note": "Mocked estimate for scaffold",
        }
