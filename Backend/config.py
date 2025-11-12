"""Minimal configuration for the Flask app.

Intentionally lightweight: no external services required. The default
DB is in-memory SQLite purely to allow SQLAlchemy model declarations
without additional setup. Replace these values as the project evolves.
"""
from __future__ import annotations

import os


class Config:
    # Core
    ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = ENV != "production"
    TESTING = False

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    JSON_SORT_KEYS = False

    # CORS (permissive for now; lock down later)
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

    # Database (in-memory by default; not used yet)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///:memory:")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
