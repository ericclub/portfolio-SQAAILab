"""
Unit Tests for Health Endpoint
Covers: TC-HLTH-01 (Unit aspect)

These tests verify the health handler returns the expected JSON shape
without requiring actual HTTP requests.
"""

import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'context', 'app', 'backend'))


@pytest.mark.unit
class TestHealthEndpointUnit:
    """Unit tests for the health endpoint response structure."""

    def test_health_response_contains_status_key(self, client):
        """TC-HLTH-01-U1: Health response should contain 'status' key."""
        response = client.get('/api/health')
        data = response.get_json()
        
        assert 'status' in data, "Response should contain 'status' key"
        assert data['status'] == 'ok', "Status should be 'ok'"

    def test_health_response_contains_message_key(self, client):
        """TC-HLTH-01-U2: Health response should contain non-empty 'message' key."""
        response = client.get('/api/health')
        data = response.get_json()
        
        assert 'message' in data, "Response should contain 'message' key"
        assert len(data['message']) > 0, "Message should not be empty"

    def test_health_response_json_shape(self, client):
        """TC-HLTH-01-U3: Health response should have exactly the expected keys."""
        response = client.get('/api/health')
        data = response.get_json()
        
        expected_keys = {'status', 'message'}
        actual_keys = set(data.keys())
        
        assert actual_keys == expected_keys, f"Expected keys {expected_keys}, got {actual_keys}"
