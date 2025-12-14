

import os


class Config:
    ENV = os.getenv("FLASK_ENV", "productions")
    DEBUG = ENV != "production"
    TESTING = True

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "1234567890")
    JSON_SORT_KEYS = False

    # CORS
    _CORS_ORIGINS_STR = os.getenv("CORS_ORIGINS", "*")
    if _CORS_ORIGINS_STR == "*":
        CORS_ORIGINS = "*"
    else:
        CORS_ORIGINS = [origin.strip() for origin in _CORS_ORIGINS_STR.split(",") if origin.strip()]

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 86400 * 7))
    JWT_ALGORITHM = "HS256"
    JWT_TOKEN_LOCATION = ["headers"]

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://cs2025:cs2025pass@localhost:5432/cs2025"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://cs2025:cs2025pass@localhost:5432/cs2025"
    )
