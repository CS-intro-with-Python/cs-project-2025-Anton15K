
from flask_cors import CORS
from flask_login import LoginManager

# CORS for browser clients (permissive for now)
cors = CORS()

# Session-based auth manager (future use)
login_manager = LoginManager()
login_manager.login_view = "auth_login"  # Endpoint name placeholder
