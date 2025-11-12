"""App extensions registry.

This module holds singletons for extensions so they can be imported
without causing circular imports. The actual initialization happens
inside the application factory in app.create_app().

Only minimal setup is done; no external services are required
at this stage.
"""

from flask_cors import CORS
from flask_login import LoginManager

# CORS for browser clients (permissive for now)
cors = CORS()

# Session-based auth manager (future use)
login_manager = LoginManager()
login_manager.login_view = "auth_login"  # Endpoint name placeholder
