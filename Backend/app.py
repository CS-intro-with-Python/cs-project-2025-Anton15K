"""Flask application factory and API registration.

This is a minimal backend scaffold based on the README. It exposes a
versioned REST API with endpoint stubs and simple data models. No real
persistence or authentication is wired yet; endpoints return example
payloads and document their intended behavior.

Run locally for demo:
    flask --app Backend.app:create_app run --port=5001

Swagger UI:
    http://localhost:5001/api/v1/docs
"""
from __future__ import annotations

from flask import Flask, Blueprint

from .config import Config
from .extensions import api, cors, db, login_manager
from .models import Attempt, Problem, RatingAdjustment, User  # noqa: F401


API_PREFIX = "/api/v1"


def create_app(config_object: type[Config] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object or Config)

    # Init extensions
    cors.init_app(app, resources={r"*": {"origins": app.config.get("CORS_ORIGINS", "*")}})
    db.init_app(app)
    login_manager.init_app(app)

    # Mount RESTX Api on a blueprint to keep prefix clean
    api_bp = Blueprint("api", __name__, url_prefix=API_PREFIX)
    api.init_app(api_bp)
    app.register_blueprint(api_bp)

    # Register namespaces
    from .api.health import ns as health_ns
    from .api.auth import ns as auth_ns
    from .api.users import ns as users_ns
    from .api.problems import ns as problems_ns
    from .api.attempts import ns as attempts_ns
    from .api.ratings import ns as ratings_ns

    api.add_namespace(health_ns)
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(users_ns, path="/users")
    api.add_namespace(problems_ns, path="/problems")
    api.add_namespace(attempts_ns, path="/attempts")
    api.add_namespace(ratings_ns, path="/ratings")

    @app.get("/")
    def index():  # pragma: no cover - trivial
        return {
            "name": "CS 2025 API",
            "docs": f"{API_PREFIX}/docs",
            "health": f"{API_PREFIX}/health",
        }

    return app
