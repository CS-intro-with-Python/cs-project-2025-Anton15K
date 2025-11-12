"""Flask application factory and API registration.

This is a minimal backend scaffold based on the README. It exposes a
versioned REST API with endpoint stubs and simple data models. No real
persistence or authentication is wired yet; endpoints return example
payloads and document their intended behavior.

Run locally for demo:
    flask --app Backend.app:create_app run --port=5001
"""
from __future__ import annotations

from flask import Flask

from .config import Config
from .extensions import cors, login_manager


API_PREFIX = "/api/v1"


def create_app(config_object: type[Config] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object or Config)

    # Init extensions
    cors.init_app(app, resources={r"*": {"origins": app.config.get("CORS_ORIGINS", "*")}})
    login_manager.init_app(app)

    # Register API blueprints under the versioned prefix
    from .api.health import bp as health_bp
    from .api.auth import bp as auth_bp
    from .api.users import bp as users_bp
    from .api.problems import bp as problems_bp
    from .api.attempts import bp as attempts_bp
    from .api.ratings import bp as ratings_bp

    app.register_blueprint(health_bp, url_prefix=f"{API_PREFIX}/health")
    app.register_blueprint(auth_bp, url_prefix=f"{API_PREFIX}/auth")
    app.register_blueprint(users_bp, url_prefix=f"{API_PREFIX}/users")
    app.register_blueprint(problems_bp, url_prefix=f"{API_PREFIX}/problems")
    app.register_blueprint(attempts_bp, url_prefix=f"{API_PREFIX}/attempts")
    app.register_blueprint(ratings_bp, url_prefix=f"{API_PREFIX}/ratings")

    @app.get("/")
    def index():
        return {
            "name": "CF 2025 API",
            "health": f"{API_PREFIX}/health",
        }

    return app
