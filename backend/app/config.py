"""Application configuration objects."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Type

BASE_DIR = Path(__file__).resolve().parent.parent


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@db:5432/codeforces",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_MASK_SWAGGER = False
    RESTX_SWAGGER_UI_DOC_EXPANSION = "list"
    PROPAGATE_EXCEPTIONS = True
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:5173")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "change-me-too")


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        "sqlite:///:memory:",
    )
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    DEBUG = False


CONFIG_BY_NAME: dict[str, Type[BaseConfig]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(config_name: str | None) -> Type[BaseConfig]:
    """Return the config class matching the provided name."""
    if not config_name:
        config_name = os.environ.get("FLASK_ENV", "development")
    config_name = config_name.lower()
    return CONFIG_BY_NAME.get(config_name, DevelopmentConfig)
