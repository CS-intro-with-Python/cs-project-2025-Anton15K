

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

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 86400 * 7))  # 7 days
    JWT_ALGORITHM = "HS256"

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
