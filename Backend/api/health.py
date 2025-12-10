
from datetime import datetime

from flask import Blueprint, jsonify

bp = Blueprint("health", __name__)


@bp.get("")
def health_check():
    """
    Check service health status
    ---
    tags:
      - Health
    responses:
      200:
        description: Service is healthy
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
            time:
              type: string
              format: date-time
              example: "2025-01-01T12:00:00Z"
            version:
              type: string
              example: "1.0.0"
    """
    return jsonify(
        {
            "status": "ok",
            "time": datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0",
        }
    )

