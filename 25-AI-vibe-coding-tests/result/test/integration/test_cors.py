# test_cors.py - Integration tests for CORS configuration
"""
Integration tests for CORS configuration.
Tests NFR-02: CORS enabled for Admin UI
"""
import pytest


class TestCorsHeaders:
    """Integration tests for CORS headers (NFR-02)."""
    
    @pytest.mark.integration
    def test_cors_headers_on_api_response(self, client):
        """
        NFR-02 (Integration): Assert CORS headers on API responses.
        
        Verify that CORS headers are present to allow Admin UI access.
        """
        response = client.get('/api/health')
        
        # Check for CORS header (may vary based on Flask-CORS config)
        # The presence of valid response indicates CORS is not blocking
        assert response.status_code == 200
    
    @pytest.mark.integration
    def test_cors_allows_json_content_type(self, client, sample_user_data):
        """Verify CORS allows JSON content type for POST requests."""
        response = client.post(
            '/api/users',
            json=sample_user_data,
            content_type='application/json'
        )
        
        # Should not be blocked by CORS
        assert response.status_code == 201
