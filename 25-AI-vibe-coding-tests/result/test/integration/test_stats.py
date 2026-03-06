# test_stats.py - Integration tests for Statistics API endpoint
"""
Integration tests for the Statistics API endpoint.
Tests story: STS-01 — View global statistics
"""
import pytest


class TestStatisticsEndpoint:
    """Integration tests for /api/stats endpoint."""
    
    @pytest.mark.integration
    @pytest.mark.stats
    def test_stats_returns_200(self, client):
        """
        TC-STS-01 (Integration): Retrieve global statistics.
        
        Scenario: Retrieve global statistics
        - When I send a GET request to /api/stats
        - Then the response status code is 200
        - And the response contains numeric fields total_users, total_posts, published_posts
        """
        response = client.get('/api/stats')
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'total_users' in data
        assert 'total_posts' in data
        assert 'published_posts' in data
        
        # All values should be numeric
        assert isinstance(data['total_users'], int)
        assert isinstance(data['total_posts'], int)
        assert isinstance(data['published_posts'], int)
    
    @pytest.mark.integration
    @pytest.mark.stats
    def test_stats_empty_database(self, client):
        """
        TC-STS-01 (Integration): With empty DB, expect zeros.
        """
        response = client.get('/api/stats')
        
        data = response.get_json()
        
        assert data['total_users'] == 0
        assert data['total_posts'] == 0
        assert data['published_posts'] == 0
    
    @pytest.mark.integration
    @pytest.mark.stats
    def test_stats_reflect_created_data(self, client, sample_user_data, sample_post_data):
        """
        TC-STS-02 (Integration): Stats reflect current data.
        
        Scenario: Stats reflect current data
        - Given I create users/posts
        - When I request /api/stats
        - Then the returned totals match the database state
        """
        # Create 2 users
        user1 = client.post('/api/users', json=sample_user_data).get_json()['user']
        client.post('/api/users', json={
            'username': 'user2',
            'email': 'user2@example.com',
            'password': 'Password123!'
        })
        
        # Create 3 posts (2 published)
        client.post('/api/posts', json={
            **sample_post_data,
            'user_id': user1['id'],
            'published': True
        })
        client.post('/api/posts', json={
            'title': 'Post 2',
            'content': 'Content 2',
            'user_id': user1['id'],
            'published': True
        })
        client.post('/api/posts', json={
            'title': 'Post 3 (Draft)',
            'content': 'Content 3',
            'user_id': user1['id'],
            'published': False
        })
        
        # Check stats
        response = client.get('/api/stats')
        data = response.get_json()
        
        assert data['total_users'] == 2
        assert data['total_posts'] == 3
        assert data['published_posts'] == 2
    
    @pytest.mark.integration
    @pytest.mark.stats
    def test_stats_cascade_impact(self, client, sample_user_data, sample_post_data):
        """
        TC-STS-03 (Integration): Cascade impact on stats.
        
        Scenario: Create user+post; delete user; expect counts decreased accordingly.
        """
        # Create user and post
        user = client.post('/api/users', json=sample_user_data).get_json()['user']
        client.post('/api/posts', json={
            **sample_post_data,
            'user_id': user['id']
        })
        
        # Initial stats
        initial_stats = client.get('/api/stats').get_json()
        assert initial_stats['total_users'] == 1
        assert initial_stats['total_posts'] == 1
        
        # Delete user (should cascade delete posts)
        client.delete(f'/api/users/{user["id"]}')
        
        # Check stats after delete
        final_stats = client.get('/api/stats').get_json()
        assert final_stats['total_users'] == 0
        assert final_stats['total_posts'] == 0
    
    @pytest.mark.integration
    @pytest.mark.stats
    def test_stats_update_on_post_publish(self, client, created_user, sample_post_data):
        """Verify published_posts updates when post is published."""
        # Create draft post
        post = client.post('/api/posts', json={
            **sample_post_data,
            'user_id': created_user['id'],
            'published': False
        }).get_json()['post']
        
        # Check initial published count
        initial_stats = client.get('/api/stats').get_json()
        assert initial_stats['published_posts'] == 0
        
        # Publish the post
        client.put(f'/api/posts/{post["id"]}', json={'published': True})
        
        # Check updated published count
        final_stats = client.get('/api/stats').get_json()
        assert final_stats['published_posts'] == 1
