# test_users.py - Integration tests for Users API endpoints
"""
Integration tests for the Users API endpoints.
Tests stories: USR-01, USR-02, USR-03, USR-04
"""
import pytest


class TestCreateUser:
    """Integration tests for POST /api/users endpoint (USR-01)."""
    
    @pytest.mark.integration
    @pytest.mark.users
    def test_create_user_with_valid_data(self, client, sample_user_data):
        """
        TC-USR-01 (Integration): Create user with valid input.
        
        Scenario: Create user with valid input
        - Given a username and email that do not already exist
        - When I send a POST request to /api/users with username, email, and password
        - Then the response status code is 201
        - And the returned user does not expose the password or password hash
        """
        response = client.post('/api/users', json=sample_user_data)
        
        assert response.status_code == 201
        
        data = response.get_json()
        assert 'user' in data
        assert data['user']['username'] == sample_user_data['username']
        assert data['user']['email'] == sample_user_data['email']
        assert 'id' in data['user']
        assert 'created_at' in data['user']
        
        # Verify password is not exposed
        assert 'password' not in data['user']
        assert 'password_hash' not in data['user']
    
    @pytest.mark.integration
    @pytest.mark.users
    def test_create_user_missing_username(self, client):
        """
        TC-USR-02 (Integration): Reject missing required fields (username).
        
        Scenario: Reject missing required fields
        - Given the request payload is missing username
        - When I send a POST request to /api/users
        - Then the response status code is 400
        """
        response = client.post('/api/users', json={
            'email': 'test@example.com',
            'password': 'Password123!'
        })
        
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'error' in data
        assert 'Missing required fields' in data['error']
    
    @pytest.mark.integration
    @pytest.mark.users
    def test_create_user_missing_email(self, client):
        """
        TC-USR-02 (Integration): Reject missing required fields (email).
        """
        response = client.post('/api/users', json={
            'username': 'testuser',
            'password': 'Password123!'
        })
        
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'error' in data
        assert 'Missing required fields' in data['error']
    
    @pytest.mark.integration
    @pytest.mark.users
    def test_create_user_missing_password(self, client):
        """
        TC-USR-02 (Integration): Reject missing required fields (password).
        """
        response = client.post('/api/users', json={
            'username': 'testuser',
            'email': 'test@example.com'
        })
        
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'error' in data
        assert 'Missing required fields' in data['error']
    
    @pytest.mark.integration
    @pytest.mark.users
    def test_create_user_duplicate_username(self, client, sample_user_data):
        """
        TC-USR-03 (Integration): Reject duplicate username.
        
        Scenario: Reject duplicate username
        - Given a user already exists with the same username
        - When I send a POST request to /api/users using that username
        - Then the response status code is 409
        """
        # Create first user
        client.post('/api/users', json=sample_user_data)
        
        # Try to create second user with same username
        response = client.post('/api/users', json={
            'username': sample_user_data['username'],
            'email': 'different@example.com',
            'password': 'DifferentPass123!'
        })
        
        assert response.status_code == 409
        
        data = response.get_json()
        assert 'error' in data
        assert 'Username already exists' in data['error']
    
    @pytest.mark.integration
    @pytest.mark.users
    def test_create_user_duplicate_email(self, client, sample_user_data):
        """
        TC-USR-04 (Integration): Reject duplicate email.
        
        Scenario: Reject duplicate email
        - Given a user already exists with the same email
        - When I send a POST request to /api/users using that email
        - Then the response status code is 409
        """
        # Create first user
        client.post('/api/users', json=sample_user_data)
        
        # Try to create second user with same email
        response = client.post('/api/users', json={
            'username': 'differentuser',
            'email': sample_user_data['email'],
            'password': 'DifferentPass123!'
        })
        
        assert response.status_code == 409
        
        data = response.get_json()
        assert 'error' in data
        assert 'Email already exists' in data['error']


class TestListUsers:
    """Integration tests for GET /api/users endpoint (USR-02)."""
    
    @pytest.mark.integration
    @pytest.mark.users
    def test_list_users_returns_array(self, client):
        """
        TC-USR-05 (Integration): Retrieve all users.
        
        Scenario: Retrieve all users
        - When I send a GET request to /api/users
        - Then the response status code is 200
        - And the response contains a users array
        """
        response = client.get('/api/users')
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'users' in data
        assert isinstance(data['users'], list)
    
    @pytest.mark.integration
    @pytest.mark.users
    def test_list_users_empty_database(self, client):
        """
        TC-USR-06 (Integration): With zero users in DB.
        """
        response = client.get('/api/users')
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['users'] == []
    
    @pytest.mark.integration
    @pytest.mark.users
    def test_list_users_contains_created_user(self, client, sample_user_data):
        """Verify created user appears in list."""
        # Create a user
        client.post('/api/users', json=sample_user_data)
        
        # List users
        response = client.get('/api/users')
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data['users']) == 1
        assert data['users'][0]['username'] == sample_user_data['username']
    
    @pytest.mark.integration
    @pytest.mark.users
    def test_list_users_contains_required_fields(self, client, created_user):
        """
        TC-USR-05 (Integration): Each user item contains required fields.
        Required: id, username, email, created_at
        """
        response = client.get('/api/users')
        
        data = response.get_json()
        user = data['users'][0]
        
        assert 'id' in user
        assert 'username' in user
        assert 'email' in user
        assert 'created_at' in user


class TestGetUserById:
    """Integration tests for GET /api/users/<id> endpoint (USR-03)."""
    
    @pytest.mark.integration
    @pytest.mark.users
    def test_get_user_by_valid_id(self, client, created_user):
        """
        TC-USR-07 (Integration): Retrieve user details by valid ID.
        
        Scenario: Retrieve user details by valid ID
        - Given a user exists with ID X
        - When I send a GET request to /api/users/X
        - Then the response status code is 200
        """
        user_id = created_user['id']
        
        response = client.get(f'/api/users/{user_id}')
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'user' in data
        assert data['user']['id'] == user_id
    
    @pytest.mark.integration
    @pytest.mark.users
    def test_get_user_not_found(self, client):
        """
        TC-USR-08 (Integration): User does not exist.
        
        Scenario: User does not exist
        - Given no user exists with ID X
        - When I send a GET request to /api/users/X
        - Then the response status code is 404
        """
        response = client.get('/api/users/999999')
        
        assert response.status_code == 404
        
        data = response.get_json()
        assert 'error' in data


class TestDeleteUser:
    """Integration tests for DELETE /api/users/<id> endpoint (USR-04)."""
    
    @pytest.mark.integration
    @pytest.mark.users
    def test_delete_user_success(self, client, created_user):
        """
        TC-USR-09 (Integration): Delete a user.
        
        Scenario: Delete a user
        - Given a user exists with ID X
        - When I send a DELETE request to /api/users/X
        - Then the response status code is 200
        """
        user_id = created_user['id']
        
        # Delete user
        response = client.delete(f'/api/users/{user_id}')
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'message' in data
        assert 'deleted' in data['message'].lower()
        
        # Verify user is deleted
        get_response = client.get(f'/api/users/{user_id}')
        assert get_response.status_code == 404
    
    @pytest.mark.integration
    @pytest.mark.users
    def test_delete_user_cascade_posts(self, client, created_user, sample_post_data):
        """
        TC-USR-10 (Integration): Cascade delete user posts.
        
        Scenario: Cascade delete user posts
        - Given a user exists with ID X and they have posts
        - When I delete the user with DELETE /api/users/X
        - Then the user's posts are removed from the database
        """
        user_id = created_user['id']
        
        # Create a post for the user
        post_data = {**sample_post_data, 'user_id': user_id}
        post_response = client.post('/api/posts', json=post_data)
        post_id = post_response.get_json()['post']['id']
        
        # Delete user
        client.delete(f'/api/users/{user_id}')
        
        # Verify post is also deleted
        get_post_response = client.get(f'/api/posts/{post_id}')
        assert get_post_response.status_code == 404
    
    @pytest.mark.integration
    @pytest.mark.users
    def test_delete_user_not_found(self, client):
        """
        TC-USR-11 (Integration): Delete a non-existent user.
        
        Scenario: Delete a non-existent user
        - Given no user exists with ID X
        - When I send a DELETE request to /api/users/X
        - Then the response status code is 404
        """
        response = client.delete('/api/users/999999')
        
        assert response.status_code == 404
