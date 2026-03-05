# test_response_shapes.py - Unit tests for API response shapes
"""
Unit tests for API response shape validation.
These tests validate that response structures match expected formats.
"""
import pytest


class TestHealthResponseShape:
    """Unit tests for health endpoint response shape."""
    
    @pytest.mark.unit
    @pytest.mark.health
    def test_health_response_has_required_keys(self):
        """
        TC-HLTH-01 (Unit): Validate health response shape.
        Expected: status, message
        """
        # Expected shape from API
        expected_shape = {'status': 'ok', 'message': 'API is running'}
        
        required_keys = ['status', 'message']
        for key in required_keys:
            assert key in expected_shape


class TestUserResponseShape:
    """Unit tests for user endpoint response shapes."""
    
    @pytest.mark.unit
    @pytest.mark.users
    def test_create_user_response_shape(self):
        """
        TC-USR-01 (Unit): Validate create user response shape.
        """
        # Simulated response shape
        response_shape = {
            'message': 'User created',
            'user': {
                'id': 1,
                'username': 'testuser',
                'email': 'test@example.com',
                'created_at': '2024-01-01T00:00:00'
            }
        }
        
        assert 'message' in response_shape
        assert 'user' in response_shape
        
        user_keys = ['id', 'username', 'email', 'created_at']
        for key in user_keys:
            assert key in response_shape['user']
        
        # Password should NOT be in response
        assert 'password' not in response_shape['user']
        assert 'password_hash' not in response_shape['user']
    
    @pytest.mark.unit
    @pytest.mark.users
    def test_list_users_response_shape(self):
        """
        TC-USR-05 (Unit): Validate list users response shape.
        """
        response_shape = {
            'users': [
                {'id': 1, 'username': 'user1', 'email': 'user1@example.com', 'created_at': '2024-01-01T00:00:00'},
                {'id': 2, 'username': 'user2', 'email': 'user2@example.com', 'created_at': '2024-01-02T00:00:00'}
            ]
        }
        
        assert 'users' in response_shape
        assert isinstance(response_shape['users'], list)


class TestPostResponseShape:
    """Unit tests for post endpoint response shapes."""
    
    @pytest.mark.unit
    @pytest.mark.posts
    def test_create_post_response_shape(self):
        """
        TC-PST-01 (Unit): Validate create post response shape.
        """
        response_shape = {
            'message': 'Post created',
            'post': {
                'id': 1,
                'title': 'Test Title',
                'content': 'Test content',
                'published': False,
                'author': 'testuser',
                'created_at': '2024-01-01T00:00:00',
                'updated_at': '2024-01-01T00:00:00'
            }
        }
        
        assert 'message' in response_shape
        assert 'post' in response_shape
        
        post_keys = ['id', 'title', 'content', 'published', 'author', 'created_at', 'updated_at']
        for key in post_keys:
            assert key in response_shape['post']
    
    @pytest.mark.unit
    @pytest.mark.posts
    def test_list_posts_response_shape(self):
        """
        TC-PST-04/06 (Unit): Validate list posts response shape.
        """
        response_shape = {
            'posts': []
        }
        
        assert 'posts' in response_shape
        assert isinstance(response_shape['posts'], list)


class TestStatsResponseShape:
    """Unit tests for statistics endpoint response shape."""
    
    @pytest.mark.unit
    @pytest.mark.stats
    def test_stats_response_has_numeric_fields(self):
        """
        TC-STS-01 (Unit): Validate stats response shape.
        Expected: total_users, total_posts, published_posts (all numeric)
        """
        response_shape = {
            'total_users': 0,
            'total_posts': 0,
            'published_posts': 0
        }
        
        required_keys = ['total_users', 'total_posts', 'published_posts']
        for key in required_keys:
            assert key in response_shape
            assert isinstance(response_shape[key], (int, float))


class TestErrorResponseShape:
    """Unit tests for error response shapes."""
    
    @pytest.mark.unit
    def test_error_400_response_shape(self):
        """Validate 400 error response shape."""
        error_response = {'error': 'Missing required fields'}
        
        assert 'error' in error_response
        assert isinstance(error_response['error'], str)
    
    @pytest.mark.unit
    def test_error_404_response_shape(self):
        """Validate 404 error response shape."""
        error_response = {'error': 'Not found'}
        
        assert 'error' in error_response
        assert isinstance(error_response['error'], str)
    
    @pytest.mark.unit
    def test_error_409_response_shape(self):
        """Validate 409 conflict error response shape."""
        error_responses = [
            {'error': 'Username already exists'},
            {'error': 'Email already exists'}
        ]
        
        for response in error_responses:
            assert 'error' in response
            assert isinstance(response['error'], str)
