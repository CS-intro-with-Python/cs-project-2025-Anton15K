

import os


class Config:
    ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = ENV != "production"
    TESTING = False

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    JSON_SORT_KEYS = False

    # CORS (permissive for now; lock down later)
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://cs2025:cs2025pass@localhost:5432/cs2025"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://cs2025:cs2025pass@localhost:5432/cs2025"
    )
