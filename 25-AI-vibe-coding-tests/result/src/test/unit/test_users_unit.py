"""
Unit Tests for User Validation and Serialization
Covers: TC-USR-01 to TC-USR-04 (Unit aspects)

These tests verify:
- Required field validation logic
- User serialization (password not exposed)
- Response structure validation
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'context', 'app', 'backend'))

from app import User


@pytest.mark.unit
class TestUserValidation:
    """Unit tests for user validation logic."""

    def test_missing_username_returns_400(self, client):
        """TC-USR-02-U1: POST with missing username should return 400."""
        response = client.post('/api/users', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 400
        assert response.get_json()['error'] == 'Missing required fields'

    def test_missing_email_returns_400(self, client):
        """TC-USR-02-U2: POST with missing email should return 400."""
        response = client.post('/api/users', json={
            'username': 'testuser',
            'password': 'password123'
        })
        
        assert response.status_code == 400
        assert response.get_json()['error'] == 'Missing required fields'

    def test_missing_password_returns_400(self, client):
        """TC-USR-02-U3: POST with missing password should return 400."""
        response = client.post('/api/users', json={
            'username': 'testuser',
            'email': 'test@example.com'
        })
        
        assert response.status_code == 400
        assert response.get_json()['error'] == 'Missing required fields'

    def test_empty_body_returns_400(self, client):
        """TC-USR-02-U4: POST with empty body should return 400."""
        response = client.post('/api/users', json={})
        
        assert response.status_code == 400
        assert response.get_json()['error'] == 'Missing required fields'

    def test_null_body_returns_400(self, client):
        """TC-USR-02-U5: POST with null body should return 400."""
        response = client.post('/api/users', 
                               data=None,
                               content_type='application/json')
        
        assert response.status_code == 400


@pytest.mark.unit
class TestUserSerialization:
    """Unit tests for user serialization (to_dict method)."""

    def test_user_to_dict_excludes_password(self, test_app):
        """TC-USR-01-U1: User serialization should not include password."""
        with test_app.app_context():
            from app import db
            user = User(username='testuser', email='test@example.com')
            user.set_password('securepassword')
            db.session.add(user)
            db.session.commit()
            
            user_dict = user.to_dict()
            
            assert 'password' not in user_dict, "Password should not be in serialized user"
            assert 'password_hash' not in user_dict, "Password hash should not be in serialized user"

    def test_user_to_dict_contains_required_fields(self, test_app):
        """TC-USR-01-U2: User serialization should contain id, username, email, created_at."""
        with test_app.app_context():
            from app import db
            user = User(username='testuser', email='test@example.com')
            user.set_password('securepassword')
            db.session.add(user)
            db.session.commit()
            
            user_dict = user.to_dict()
            
            assert 'id' in user_dict
            assert 'username' in user_dict
            assert 'email' in user_dict
            assert 'created_at' in user_dict

    def test_user_response_does_not_expose_password(self, client, sample_user_data):
        """TC-USR-01-U3: API response should not expose password or hash."""
        response = client.post('/api/users', json=sample_user_data)
        data = response.get_json()
        
        assert 'password' not in data.get('user', {}), "Password should not be in response"
        assert 'password_hash' not in data.get('user', {}), "Password hash should not be in response"


@pytest.mark.unit
class TestUserPasswordHashing:
    """Unit tests for password hashing functionality."""

    def test_password_is_hashed(self, test_app):
        """Password should be stored as a hash, not plain text."""
        with test_app.app_context():
            user = User(username='testuser', email='test@example.com')
            plain_password = 'mysecretpassword'
            user.set_password(plain_password)
            
            assert user.password_hash != plain_password
            assert len(user.password_hash) > len(plain_password)

    def test_check_password_works(self, test_app):
        """check_password should validate the correct password."""
        with test_app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('correctpassword')
            
            assert user.check_password('correctpassword') is True
            assert user.check_password('wrongpassword') is False
