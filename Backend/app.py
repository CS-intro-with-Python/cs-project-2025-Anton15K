
from flask import Flask

from .config import Config
from .extensions import cors, login_manager, db


API_PREFIX = "/api/v1"


def create_app(config_object: type[Config] | None = None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_object or Config)

    # Init extensions
    cors.init_app(app, resources={r"*": {"origins": app.config.get("CORS_ORIGINS", "*")}})
    login_manager.init_app(app)
    db.init_app(app)

    # Import models to register them with SQLAlchemy
    from . import models  # noqa: F401
    from .models import User

    # Flask-Login user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register frontend views blueprint
    from .views import bp as views_bp
    app.register_blueprint(views_bp)

    # Register API blueprints under the versioned prefix
    from .api.health import bp as health_bp
    from .api.auth import bp as auth_bp
    from .api.users import bp as users_bp
    from .api.problems import bp as problems_bp
    from .api.attempts import bp as attempts_bp
    from .api.ratings import bp as ratings_bp
    from .api.codeforces import bp as codeforces_bp

    app.register_blueprint(health_bp, url_prefix=f"{API_PREFIX}/health")
    app.register_blueprint(auth_bp, url_prefix=f"{API_PREFIX}/auth")
    app.register_blueprint(users_bp, url_prefix=f"{API_PREFIX}/users")
    app.register_blueprint(problems_bp, url_prefix=f"{API_PREFIX}/problems")
    app.register_blueprint(attempts_bp, url_prefix=f"{API_PREFIX}/attempts")
    app.register_blueprint(ratings_bp, url_prefix=f"{API_PREFIX}/ratings")
    app.register_blueprint(codeforces_bp, url_prefix=f"{API_PREFIX}/codeforces")

    return app


