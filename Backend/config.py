

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


class TestConfig(Config):
    TESTING = True
    DEBUG = True
