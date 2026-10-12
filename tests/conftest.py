import os
import tempfile
import pytest
from app import create_app
from config import TestConfig
from database.init_db import init_db

@pytest.fixture(scope='function')
def app():
    """Create and configure a new Flask app instance for each test with isolated SQLite DB."""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')

    class CustomTestConfig(TestConfig):
        DATABASE_PATH = db_path
        TESTING = True

    application = create_app(CustomTestConfig)

    with application.app_context():
        # Initialize database tables and seed test data
        init_db(db_path=db_path, force=True)

    yield application

    # Teardown: close file descriptor and remove temporary database
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)

@pytest.fixture(scope='function')
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()
