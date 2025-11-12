"""App extensions registry.

This module holds singletons for extensions so they can be imported
without causing circular imports. The actual initialization happens
inside the application factory in app.create_app().

Only minimal setup is done; no external services are required
at this stage.
"""
from __future__ import annotations

from flask_cors import CORS
from flask_login import LoginManager
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

# Database ORM (not used yet; configured to in-memory by default in app)
db = SQLAlchemy()

# REST API with Swagger UI via Flask-RESTX
api = Api(
    version="1.0",
    title="CS 2025 API",
    description=(
        "REST API for estimating Codeforces problem difficulty. "
        "This is an initial scaffold with endpoint stubs and models."
    ),
    doc="/docs",  # Swagger UI mounted under the API blueprint
)

# CORS for browser clients (permissive for now)
cors = CORS()

# Session-based auth manager (future use)
login_manager = LoginManager()
login_manager.login_view = "auth_login"  # Endpoint name placeholder
