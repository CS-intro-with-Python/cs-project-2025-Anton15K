"""Application factory for the Codeforces difficulty estimation backend."""
from __future__ import annotations

from flask import Flask

from .api import api_bp
from .config import get_config
from .extensions import cors, db, login_manager, migrate


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure a Flask application instance."""
    app = Flask(__name__)
    config_object = get_config(config_name)
    app.config.from_object(config_object)

    _register_extensions(app)
    _register_blueprints(app)
    _register_shellcontext(app)

    return app


def _register_extensions(app: Flask) -> None:
    """Initialize Flask extensions."""
    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"


def _register_blueprints(app: Flask) -> None:
    """Register application blueprints."""
    app.register_blueprint(api_bp)


def _register_shellcontext(app: Flask) -> None:
    """Register handy objects in the Flask shell context."""
    from . import models  # noqa: F401  (import side effect registers models)

    @app.shell_context_processor
    def make_shell_context():  # type: ignore[override]
        return {"db": db, **models.__dict__}
