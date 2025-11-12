"""Health check endpoints.

Purpose:
- Provide a quick way to verify the API service is up and reachable.
- Used by uptime checks, load balancers, and CI smoke tests.

Behavior (future):
- May expand to include dependency checks (DB, cache) and version info.
"""
from __future__ import annotations

from datetime import datetime

from flask_restx import Namespace, Resource, fields

ns = Namespace("health", description="Service health and diagnostics")

health_model = ns.model(
    "Health",
    {
        "status": fields.String(example="ok", description="Service status indicator"),
        "time": fields.DateTime(dt_format="iso8601", description="Server time (UTC)"),
        "version": fields.String(example="1.0.0", description="API semantic version"),
    },
)


@ns.route("")
class HealthResource(Resource):
    @ns.doc("health_check", description="Simple health check endpoint")
    @ns.marshal_with(health_model)
    def get(self):
        """Return service status without requiring any dependencies.

        Stable contract for monitoring. In the future, add more fields like
        upstream status or git commit hash as needed.
        """
        return {
            "status": "ok",
            "time": datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0",
        }
