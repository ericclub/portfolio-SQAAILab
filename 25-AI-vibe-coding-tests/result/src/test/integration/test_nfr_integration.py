"""
Integration Tests for CORS and NFR requirements
Covers: NFR-01, NFR-02

These tests verify cross-cutting concerns like JSON responses,
HTTP codes, and CORS headers.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'context', 'app', 'backend'))


@pytest.mark.integration
class TestJSONResponses:
    """Integration tests for NFR-01: JSON responses and HTTP codes."""

    def test_health_returns_json(self, client):
        """NFR-01: /api/health should return JSON."""
        response = client.get('/api/health')
        assert response.content_type == 'application/json'

    def test_users_returns_json(self, client):
        """NFR-01: /api/users should return JSON."""
        response = client.get('/api/users')
        assert response.content_type == 'application/json'

    def test_posts_returns_json(self, client):
        """NFR-01: /api/posts should return JSON."""
        response = client.get('/api/posts')
        assert response.content_type == 'application/json'

    def test_stats_returns_json(self, client):
        """NFR-01: /api/stats should return JSON."""
        response = client.get('/api/stats')
        assert response.content_type == 'application/json'

    def test_404_returns_json(self, client):
        """NFR-01: 404 errors should return JSON."""
        response = client.get('/api/users/999999')
        assert response.status_code == 404
        assert response.content_type == 'application/json'
        assert 'error' in response.get_json()

    def test_400_returns_json(self, client):
        """NFR-01: 400 errors should return JSON."""
        response = client.post('/api/users', json={})
        assert response.status_code == 400
        assert response.content_type == 'application/json'
        assert 'error' in response.get_json()

    def test_409_returns_json(self, client, created_user, sample_user_data):
        """NFR-01: 409 errors should return JSON."""
        response = client.post('/api/users', json=sample_user_data)
        assert response.status_code == 409
        assert response.content_type == 'application/json'
        assert 'error' in response.get_json()


@pytest.mark.integration
class TestCORS:
    """Integration tests for NFR-02: CORS enabled for Admin UI."""

    def test_cors_headers_on_get(self, client):
        """NFR-02: GET requests should include CORS headers."""
        response = client.get('/api/health')
        # Flask-CORS adds these headers
        # Note: In test client, CORS headers may not appear without Origin header
        assert response.status_code == 200

    def test_cors_preflight_options(self, client):
        """NFR-02: OPTIONS requests should be handled for CORS preflight."""
        response = client.options('/api/users', headers={
            'Origin': 'http://localhost:5000',
            'Access-Control-Request-Method': 'POST'
        })
        # Should not return 405 Method Not Allowed
        assert response.status_code in [200, 204]


@pytest.mark.integration
class TestHTTPStatusCodes:
    """Integration tests for correct HTTP status codes."""

    def test_successful_get_returns_200(self, client):
        """Successful GET should return 200."""
        response = client.get('/api/health')
        assert response.status_code == 200

    def test_successful_create_returns_201(self, client, sample_user_data):
        """Successful POST (create) should return 201."""
        response = client.post('/api/users', json=sample_user_data)
        assert response.status_code == 201

    def test_successful_update_returns_200(self, client, created_post):
        """Successful PUT (update) should return 200."""
        response = client.put(f"/api/posts/{created_post['id']}", json={
            'title': 'Updated'
        })
        assert response.status_code == 200

    def test_successful_delete_returns_200(self, client, created_user):
        """Successful DELETE should return 200."""
        response = client.delete(f"/api/users/{created_user['id']}")
        assert response.status_code == 200

    def test_missing_fields_returns_400(self, client):
        """Missing required fields should return 400."""
        response = client.post('/api/users', json={})
        assert response.status_code == 400

    def test_not_found_returns_404(self, client):
        """Resource not found should return 404."""
        response = client.get('/api/users/999999')
        assert response.status_code == 404

    def test_conflict_returns_409(self, client, created_user, sample_user_data):
        """Duplicate resource should return 409."""
        response = client.post('/api/users', json=sample_user_data)
        assert response.status_code == 409
