"""
Integration Tests for Users CRUD
Covers: TC-USR-01 to TC-USR-11

These tests verify the complete Flask route + DB behavior
for user management operations.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'context', 'app', 'backend'))


@pytest.mark.integration
class TestCreateUser:
    """Integration tests for POST /api/users."""

    def test_create_user_returns_201(self, client, sample_user_data):
        """TC-USR-01: Create user with valid input should return 201."""
        response = client.post('/api/users', json=sample_user_data)
        
        assert response.status_code == 201

    def test_create_user_returns_user_object(self, client, sample_user_data):
        """TC-USR-01: Response should contain user object with expected fields."""
        response = client.post('/api/users', json=sample_user_data)
        data = response.get_json()
        
        assert 'user' in data
        user = data['user']
        assert 'id' in user
        assert user['username'] == sample_user_data['username']
        assert user['email'] == sample_user_data['email']
        assert 'created_at' in user

    def test_create_user_does_not_expose_password(self, client, sample_user_data):
        """TC-USR-01: Response should not expose password or hash."""
        response = client.post('/api/users', json=sample_user_data)
        data = response.get_json()
        
        assert 'password' not in data['user']
        assert 'password_hash' not in data['user']

    def test_create_user_missing_fields_returns_400(self, client):
        """TC-USR-02: Missing required fields should return 400."""
        response = client.post('/api/users', json={
            'username': 'testuser',
            'email': 'test@example.com'
            # missing password
        })
        
        assert response.status_code == 400
        assert response.get_json()['error'] == 'Missing required fields'

    def test_create_user_duplicate_username_returns_409(self, client, sample_user_data):
        """TC-USR-03: Duplicate username should return 409."""
        # Create first user
        client.post('/api/users', json=sample_user_data)
        
        # Try to create second user with same username
        response = client.post('/api/users', json={
            'username': sample_user_data['username'],
            'email': 'different@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 409
        assert response.get_json()['error'] == 'Username already exists'

    def test_create_user_duplicate_email_returns_409(self, client, sample_user_data):
        """TC-USR-04: Duplicate email should return 409."""
        # Create first user
        client.post('/api/users', json=sample_user_data)
        
        # Try to create second user with same email
        response = client.post('/api/users', json={
            'username': 'differentuser',
            'email': sample_user_data['email'],
            'password': 'password123'
        })
        
        assert response.status_code == 409
        assert response.get_json()['error'] == 'Email already exists'


@pytest.mark.integration
class TestListUsers:
    """Integration tests for GET /api/users."""

    def test_list_users_returns_200(self, client):
        """TC-USR-05: GET /api/users should return 200."""
        response = client.get('/api/users')
        
        assert response.status_code == 200

    def test_list_users_returns_users_array(self, client):
        """TC-USR-05: Response should contain users array."""
        response = client.get('/api/users')
        data = response.get_json()
        
        assert 'users' in data
        assert isinstance(data['users'], list)

    def test_list_users_empty_database(self, client):
        """TC-USR-06: With zero users, should return empty array."""
        response = client.get('/api/users')
        data = response.get_json()
        
        assert data['users'] == []

    def test_list_users_with_users(self, client, sample_user_data):
        """TC-USR-05: After creating users, they should appear in the list."""
        # Create a user
        client.post('/api/users', json=sample_user_data)
        
        response = client.get('/api/users')
        data = response.get_json()
        
        assert len(data['users']) == 1
        assert data['users'][0]['username'] == sample_user_data['username']

    def test_list_users_contains_required_fields(self, client, created_user):
        """TC-USR-05: Each user should contain id, username, email, created_at."""
        response = client.get('/api/users')
        data = response.get_json()
        
        user = data['users'][0]
        assert 'id' in user
        assert 'username' in user
        assert 'email' in user
        assert 'created_at' in user


@pytest.mark.integration
class TestGetUserById:
    """Integration tests for GET /api/users/<id>."""

    def test_get_user_by_id_returns_200(self, client, created_user):
        """TC-USR-07: GET /api/users/{id} should return 200 for existing user."""
        response = client.get(f"/api/users/{created_user['id']}")
        
        assert response.status_code == 200

    def test_get_user_by_id_returns_correct_user(self, client, created_user):
        """TC-USR-07: Response should contain matching user id."""
        response = client.get(f"/api/users/{created_user['id']}")
        data = response.get_json()
        
        assert data['user']['id'] == created_user['id']
        assert data['user']['username'] == created_user['username']

    def test_get_user_not_found_returns_404(self, client):
        """TC-USR-08: GET /api/users/{invalid_id} should return 404."""
        response = client.get('/api/users/999999')
        
        assert response.status_code == 404

    def test_get_user_not_found_error_message(self, client):
        """TC-USR-08: 404 response should contain error message."""
        response = client.get('/api/users/999999')
        data = response.get_json()
        
        assert 'error' in data
        assert data['error'] == 'Not found'


@pytest.mark.integration
class TestDeleteUser:
    """Integration tests for DELETE /api/users/<id>."""

    def test_delete_user_returns_200(self, client, created_user):
        """TC-USR-09: DELETE /api/users/{id} should return 200."""
        response = client.delete(f"/api/users/{created_user['id']}")
        
        assert response.status_code == 200
        assert response.get_json()['message'] == 'User deleted'

    def test_delete_user_removes_user(self, client, created_user):
        """TC-USR-09: After delete, GET should return 404."""
        client.delete(f"/api/users/{created_user['id']}")
        
        response = client.get(f"/api/users/{created_user['id']}")
        assert response.status_code == 404

    def test_delete_user_cascades_posts(self, client, created_user):
        """TC-USR-10: Deleting user should also delete their posts."""
        # Create a post for the user
        post_response = client.post('/api/posts', json={
            'title': 'Test Post',
            'content': 'Test Content',
            'user_id': created_user['id']
        })
        post_id = post_response.get_json()['post']['id']
        
        # Delete the user
        client.delete(f"/api/users/{created_user['id']}")
        
        # Post should also be deleted
        response = client.get(f"/api/posts/{post_id}")
        assert response.status_code == 404

    def test_delete_nonexistent_user_returns_404(self, client):
        """TC-USR-11: DELETE /api/users/{invalid_id} should return 404."""
        response = client.delete('/api/users/999999')
        
        assert response.status_code == 404
