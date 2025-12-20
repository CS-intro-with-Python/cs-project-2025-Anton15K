import os

import pytest
from Backend.app import create_app
from Backend.extensions import db as _db
from Backend.config import TestConfig
from Backend.extensions import create_access_token

@pytest.fixture(scope="session")
def app():
    """Create application for the tests."""
    app = create_app(TestConfig)
    
    # Create an app context for the session
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()

@pytest.fixture(scope="session")
def db(app):
    """Create database for the tests."""
    with app.app_context():
        _db.drop_all()
        _db.create_all()
        yield _db
        _db.drop_all()

@pytest.fixture(autouse=True)
def clean_db(db):
    """Clean database before each test."""
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        continue
    db.drop_all()
    db.create_all()
    yield
    db.session.remove()

@pytest.fixture(scope="function")
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope="function")
def token_factory(app):
    """Factory to create JWT tokens for testing."""
    def _create_token(user_id=1, claims=None):
        with app.app_context():
            return create_access_token(user_id, claims or {})
    return _create_token
