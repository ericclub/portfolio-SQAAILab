# test_error_handling.py - Integration tests for error handling
"""
Integration tests for error handling behavior.
Tests NFR-01, NFR-03: JSON responses, HTTP codes, and error handling
"""
import pytest


class TestErrorHandling:
    """Integration tests for error handling (NFR-01, NFR-03)."""
    
    @pytest.mark.integration
    def test_404_returns_json(self, client):
        """
        NFR-01 (Integration): 404 errors return JSON response.
        """
        response = client.get('/api/nonexistent/endpoint')
        
        assert response.status_code == 404
        assert response.content_type == 'application/json'
        
        data = response.get_json()
        assert 'error' in data
    
    @pytest.mark.integration
    def test_400_returns_json(self, client):
        """
        NFR-01 (Integration): 400 errors return JSON response.
        """
        response = client.post('/api/users', json={})
        
        assert response.status_code == 400
        assert response.content_type == 'application/json'
        
        data = response.get_json()
        assert 'error' in data
    
    @pytest.mark.integration
    def test_409_returns_json(self, client, sample_user_data):
        """
        NFR-01 (Integration): 409 conflict errors return JSON response.
        """
        # Create first user
        client.post('/api/users', json=sample_user_data)
        
        # Try to create duplicate
        response = client.post('/api/users', json=sample_user_data)
        
        assert response.status_code == 409
        assert response.content_type == 'application/json'
        
        data = response.get_json()
        assert 'error' in data
    
    @pytest.mark.integration
    def test_successful_response_is_json(self, client):
        """
        NFR-01 (Integration): Successful responses are JSON.
        """
        response = client.get('/api/health')
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    @pytest.mark.integration
    def test_create_response_includes_message(self, client, sample_user_data):
        """Verify create responses include a message field."""
        response = client.post('/api/users', json=sample_user_data)
        
        assert response.status_code == 201
        
        data = response.get_json()
        assert 'message' in data
    
    @pytest.mark.integration
    def test_delete_response_includes_message(self, client, created_user):
        """Verify delete responses include a message field."""
        response = client.delete(f'/api/users/{created_user["id"]}')
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'message' in data
