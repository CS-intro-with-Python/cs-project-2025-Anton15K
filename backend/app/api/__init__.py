"""API blueprint and namespace registration."""

from __future__ import annotations

from flask import Blueprint
from flask_restx import Api

from .health import ns as health_ns

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(
    api_bp,
    version="1.0",
    title="Codeforces Difficulty Estimator API",
    description="REST API for problem difficulty estimation and user attempts.",
    doc="/docs",
)

api.add_namespace(health_ns)
