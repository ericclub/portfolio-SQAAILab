# test_health.py - Integration tests for Health endpoint
"""
Integration tests for the Health API endpoint.
Tests story: HLTH-01 — Check API availability
"""
import pytest


class TestHealthEndpoint:
    """Integration tests for /api/health endpoint."""
    
    @pytest.mark.integration
    @pytest.mark.health
    def test_health_check_returns_200(self, client):
        """
        TC-HLTH-01 (Integration): Health check returns OK response.
        
        Scenario: Health check returns an OK response
        - Given the backend server is running
        - When I send a GET request to /api/health
        - Then the response status code is 200
        - And the response body contains status: "ok" and a non-empty message
        """
        response = client.get('/api/health')
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'ok'
        assert 'message' in data
        assert len(data['message']) > 0
    
    @pytest.mark.integration
    @pytest.mark.health
    def test_health_response_is_json(self, client):
        """Verify health endpoint returns JSON content type."""
        response = client.get('/api/health')
        
        # Check content type
        assert response.content_type == 'application/json'
