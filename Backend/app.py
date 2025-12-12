
from flask import Flask
from flasgger import Swagger

from .config import Config
from .extensions import cors, login_manager, db


API_PREFIX = "/api/v1"

# Swagger configuration
SWAGGER_CONFIG = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/api/docs/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs/",
}

SWAGGER_TEMPLATE = {
    "info": {
        "title": "Codeforces Training API",
        "description": "API for the Codeforces competitive programming training platform. "
                       "Manage users, problems, attempts, and ratings with Codeforces integration.",
    },
    "host": "localhost:5001",
    "basePath": "/api/v1",
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'",
        }
    },
    "tags": [
        {"name": "Health", "description": "Health check endpoints"},
        {"name": "Auth", "description": "Authentication endpoints (register, login, logout)"},
        {"name": "Users", "description": "User management endpoints"},
        {"name": "Problems", "description": "Problem management and rating estimation"},
        {"name": "Attempts", "description": "Attempt tracking for problem solving"},
        {"name": "Ratings", "description": "Rating calculations and adjustments"},
        {"name": "Codeforces", "description": "Codeforces API integration"},
    ],
}


def create_app(config_object: type[Config] | None = None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_object or Config)
    app.config["SWAGGER"] = {"title": "Codeforces Training API", "uiversion": 3}

    # Init extensions
    cors.init_app(app, resources={r"*": {"origins": app.config.get("CORS_ORIGINS", "*")}}, supports_credentials=True)
    login_manager.init_app(app)
    db.init_app(app)

    # Initialize Swagger
    Swagger(app, config=SWAGGER_CONFIG, template=SWAGGER_TEMPLATE)

    # Import models to register them with SQLAlchemy
    from . import models
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


