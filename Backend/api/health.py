
from datetime import datetime

from flask import Blueprint, jsonify

bp = Blueprint("health", __name__)


@bp.get("")
def health_check():
    """Return service status without requiring any dependencies.

    Stable contract for monitoring. In the future, add more fields like
    upstream status or git commit hash as needed.
    """
    return jsonify(
        {
            "status": "ok",
            "time": datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0",
        }
    )
