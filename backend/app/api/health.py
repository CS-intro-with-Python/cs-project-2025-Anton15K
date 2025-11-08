"""Health check endpoints."""

from __future__ import annotations

from flask_restx import Namespace, Resource

ns = Namespace("health", description="Health monitoring endpoints")


@ns.route("/ping")
class HealthPingResource(Resource):
    """Simple health check endpoint."""

    @ns.doc(description="Return a basic heartbeat response")
    def get(self) -> dict[str, str]:
        return {"status": "ok"}
