"""
Pytest configuration and fixtures for unit and integration tests.
Provides test client, database setup, and common fixtures.
"""

import pytest
import sys
import os

# Add the context/src/app/backend to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'context', 'src', 'app', 'backend'))

from app import app, db, User, Post

@pytest.fixture(scope='function')
def test_app():
    """Create and configure a test application instance."""
    # Configure the app for testing with SQLite in-memory database
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(test_app):
    """Create a test client for the application."""
    return test_app.test_client()


@pytest.fixture(scope='function')
def db_session(test_app):
    """Provide a database session for tests."""
    with test_app.app_context():
        yield db


@pytest.fixture
def sample_user_data():
    """Provide sample user data for tests."""
    return {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'securepassword123'
    }


@pytest.fixture
def sample_post_data():
    """Provide sample post data for tests."""
    return {
        'title': 'Test Post Title',
        'content': 'This is the test post content.',
        'published': False
    }


@pytest.fixture
def created_user(client, sample_user_data):
    """Create and return a user via the API."""
    response = client.post('/api/users', json=sample_user_data)
    return response.get_json()['user']


@pytest.fixture
def created_post(client, created_user, sample_post_data):
    """Create and return a post via the API."""
    post_data = {**sample_post_data, 'user_id': created_user['id']}
    response = client.post('/api/posts', json=post_data)
    return response.get_json()['post']
