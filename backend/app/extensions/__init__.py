"""Shared Flask extensions are instantiated here."""
from __future__ import annotations

from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
