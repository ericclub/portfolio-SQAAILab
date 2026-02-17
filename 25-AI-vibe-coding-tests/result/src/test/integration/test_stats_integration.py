"""
Integration Tests for Statistics Endpoint
Covers: TC-STS-01 to TC-STS-03

These tests verify the complete Flask route + DB behavior
for statistics retrieval.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'context', 'app', 'backend'))


@pytest.mark.integration
class TestStatsEndpoint:
    """Integration tests for GET /api/stats."""

    def test_get_stats_returns_200(self, client):
        """TC-STS-01: GET /api/stats should return 200."""
        response = client.get('/api/stats')
        
        assert response.status_code == 200

    def test_get_stats_returns_json(self, client):
        """TC-STS-01: GET /api/stats should return JSON content."""
        response = client.get('/api/stats')
        
        assert response.content_type == 'application/json'

    def test_get_stats_empty_database(self, client):
        """TC-STS-01: With empty DB, should return zeros."""
        response = client.get('/api/stats')
        data = response.get_json()
        
        assert data['total_users'] == 0
        assert data['total_posts'] == 0
        assert data['published_posts'] == 0

    def test_get_stats_reflects_user_count(self, client, sample_user_data):
        """TC-STS-02: Stats should reflect correct user count."""
        # Create 2 users
        client.post('/api/users', json=sample_user_data)
        client.post('/api/users', json={
            'username': 'user2',
            'email': 'user2@example.com',
            'password': 'password123'
        })
        
        response = client.get('/api/stats')
        data = response.get_json()
        
        assert data['total_users'] == 2

    def test_get_stats_reflects_post_counts(self, client, created_user):
        """TC-STS-02: Stats should reflect correct post counts (total and published)."""
        # Create 3 posts: 2 published, 1 draft
        client.post('/api/posts', json={
            'title': 'Published 1',
            'content': 'Content',
            'user_id': created_user['id'],
            'published': True
        })
        client.post('/api/posts', json={
            'title': 'Published 2',
            'content': 'Content',
            'user_id': created_user['id'],
            'published': True
        })
        client.post('/api/posts', json={
            'title': 'Draft',
            'content': 'Content',
            'user_id': created_user['id'],
            'published': False
        })
        
        response = client.get('/api/stats')
        data = response.get_json()
        
        assert data['total_posts'] == 3
        assert data['published_posts'] == 2

    def test_get_stats_cascade_delete_impact(self, client, sample_user_data):
        """TC-STS-03: Stats should decrease when user+posts are deleted."""
        # Create user
        user_response = client.post('/api/users', json=sample_user_data)
        user_id = user_response.get_json()['user']['id']
        
        # Create post
        client.post('/api/posts', json={
            'title': 'Test Post',
            'content': 'Content',
            'user_id': user_id,
            'published': True
        })
        
        # Verify initial stats
        response = client.get('/api/stats')
        data = response.get_json()
        assert data['total_users'] == 1
        assert data['total_posts'] == 1
        assert data['published_posts'] == 1
        
        # Delete user (cascades to posts)
        client.delete(f'/api/users/{user_id}')
        
        # Verify updated stats
        response = client.get('/api/stats')
        data = response.get_json()
        assert data['total_users'] == 0
        assert data['total_posts'] == 0
        assert data['published_posts'] == 0


@pytest.mark.integration
class TestStatsDataIntegrity:
    """Integration tests for stats data accuracy."""

    def test_stats_published_never_exceeds_total(self, client, created_user):
        """Published posts should never exceed total posts."""
        # Create mixed posts
        for i in range(5):
            client.post('/api/posts', json={
                'title': f'Post {i}',
                'content': 'Content',
                'user_id': created_user['id'],
                'published': i % 2 == 0  # Alternate published/draft
            })
        
        response = client.get('/api/stats')
        data = response.get_json()
        
        assert data['published_posts'] <= data['total_posts']
