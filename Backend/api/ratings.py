"""Rating adjustment endpoints (stubs).

Purpose:
- Allow users to submit feedback after solving a problem to adjust its estimated difficulty.

Future behavior:
- Persist adjustments, recalculate aggregate estimated rating per problem,
  and personalize estimates per user based on performance history.
"""
from __future__ import annotations

from flask_restx import Namespace, Resource, fields

ns = Namespace("ratings", description="Adjust and review problem ratings")

adjust_req = ns.model(
    "RatingAdjustmentRequest",
    {
        "problem_id": fields.Integer(required=True),
        "delta": fields.Integer(required=True, description="Positive to increase difficulty, negative to decrease"),
        "note": fields.String(required=False, description="Optional comment explaining the adjustment"),
    },
)

adjust_resp = ns.model(
    "RatingAdjustmentResponse",
    {
        "problem_id": fields.Integer(example=1),
        "previous_estimate": fields.Integer(example=1300),
        "new_estimate": fields.Integer(example=1310),
        "applied_delta": fields.Integer(example=+10),
        "message": fields.String(example="Adjustment recorded (mocked)"),
    },
)


@ns.route("/adjust")
class AdjustRating(Resource):
    @ns.expect(adjust_req, validate=True)
    @ns.marshal_with(adjust_resp)
    @ns.doc(description="Apply a user-provided adjustment to a problem's estimated rating (mocked logic).")
    def post(self):
        payload = ns.payload or {}
        prev = 1300
        delta = int(payload.get("delta", 0))
        new_estimate = prev + delta
        return {
            "problem_id": payload.get("problem_id", 1),
            "previous_estimate": prev,
            "new_estimate": new_estimate,
            "applied_delta": delta,
            "message": "Adjustment recorded (mocked)",
        }
