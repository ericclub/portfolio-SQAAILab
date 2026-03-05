# conftest.py - Shared pytest fixtures for unit and integration tests
import sys
import os
import pytest
from pathlib import Path

# Add the source directory to the path
SRC_PATH = Path(__file__).parent.parent.parent.parent / "10-AI-vibe-coding" / "result" / "src" / "app" / "backend"
sys.path.insert(0, str(SRC_PATH))

from app import app, db, User, Post


@pytest.fixture(scope='function')
def flask_app():
    """Create and configure a new app instance for each test."""
    # Use SQLite in-memory database for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(flask_app):
    """Create a test client for the app."""
    return flask_app.test_client()


@pytest.fixture(scope='function')
def db_session(flask_app):
    """Provide a database session for direct database operations."""
    with flask_app.app_context():
        yield db.session


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'TestPassword123!'
    }


@pytest.fixture
def sample_post_data():
    """Sample post data for testing (requires user_id to be set)."""
    return {
        'title': 'Test Post Title',
        'content': 'This is test content for the post.',
        'published': False
    }


@pytest.fixture
def created_user(client, sample_user_data):
    """Create a user and return the user data with ID."""
    response = client.post('/api/users', json=sample_user_data)
    return response.get_json()['user']


@pytest.fixture
def created_post(client, created_user, sample_post_data):
    """Create a post for the test user and return the post data with ID."""
    post_data = {**sample_post_data, 'user_id': created_user['id']}
    response = client.post('/api/posts', json=post_data)
    return response.get_json()['post']
