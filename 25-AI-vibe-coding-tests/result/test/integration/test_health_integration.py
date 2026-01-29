"""
Integration Tests for Health Endpoint
Covers: TC-HLTH-01, TC-HLTH-02

These tests verify the complete HTTP request/response cycle
for the health endpoint.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'context', 'app', 'backend'))


@pytest.mark.integration
class TestHealthEndpointIntegration:
    """Integration tests for the /api/health endpoint."""

    def test_health_check_returns_200(self, client):
        """TC-HLTH-01: GET /api/health should return 200 status code."""
        response = client.get('/api/health')
        
        assert response.status_code == 200

    def test_health_check_returns_json(self, client):
        """TC-HLTH-01: GET /api/health should return JSON content."""
        response = client.get('/api/health')
        
        assert response.content_type == 'application/json'

    def test_health_check_returns_ok_status(self, client):
        """TC-HLTH-01: GET /api/health should return status='ok'."""
        response = client.get('/api/health')
        data = response.get_json()
        
        assert data['status'] == 'ok'
        assert 'message' in data
        assert len(data['message']) > 0

    def test_health_check_response_format(self, client):
        """TC-HLTH-01: Verify complete response format."""
        response = client.get('/api/health')
        data = response.get_json()
        
        assert response.status_code == 200
        assert data == {'status': 'ok', 'message': 'API is running'}
