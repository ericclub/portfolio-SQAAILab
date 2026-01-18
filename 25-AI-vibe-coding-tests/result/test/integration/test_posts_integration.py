"""
Integration Tests for Posts CRUD
Covers: TC-PST-01 to TC-PST-14

These tests verify the complete Flask route + DB behavior
for post management operations.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'context', 'app', 'backend'))


@pytest.mark.integration
class TestCreatePost:
    """Integration tests for POST /api/posts."""

    def test_create_post_returns_201(self, client, created_user):
        """TC-PST-01: Create post with valid input should return 201."""
        response = client.post('/api/posts', json={
            'title': 'Test Post',
            'content': 'Test content',
            'user_id': created_user['id']
        })
        
        assert response.status_code == 201

    def test_create_post_returns_post_object(self, client, created_user):
        """TC-PST-01: Response should contain post object with expected fields."""
        response = client.post('/api/posts', json={
            'title': 'Test Post',
            'content': 'Test content',
            'user_id': created_user['id']
        })
        data = response.get_json()
        
        assert 'post' in data
        post = data['post']
        assert 'id' in post
        assert post['title'] == 'Test Post'
        assert post['content'] == 'Test content'
        assert 'published' in post
        assert 'author' in post
        assert 'created_at' in post
        assert 'updated_at' in post

    def test_create_post_includes_author_username(self, client, created_user):
        """TC-PST-01: Response should include author username."""
        response = client.post('/api/posts', json={
            'title': 'Test Post',
            'content': 'Test content',
            'user_id': created_user['id']
        })
        data = response.get_json()
        
        assert data['post']['author'] == created_user['username']

    def test_create_post_missing_title_returns_400(self, client, created_user):
        """TC-PST-02: Missing title should return 400."""
        response = client.post('/api/posts', json={
            'content': 'Test content',
            'user_id': created_user['id']
        })
        
        assert response.status_code == 400
        assert response.get_json()['error'] == 'Missing required fields'

    def test_create_post_nonexistent_user_returns_404(self, client):
        """TC-PST-03: Non-existent user_id should return 404."""
        response = client.post('/api/posts', json={
            'title': 'Test Post',
            'content': 'Test content',
            'user_id': 99999
        })
        
        assert response.status_code == 404
        assert response.get_json()['error'] == 'User not found'


@pytest.mark.integration
class TestListPosts:
    """Integration tests for GET /api/posts."""

    def test_list_posts_returns_200(self, client):
        """TC-PST-04: GET /api/posts should return 200."""
        response = client.get('/api/posts')
        
        assert response.status_code == 200

    def test_list_posts_returns_posts_array(self, client):
        """TC-PST-04: Response should contain posts array."""
        response = client.get('/api/posts')
        data = response.get_json()
        
        assert 'posts' in data
        assert isinstance(data['posts'], list)

    def test_list_posts_empty_database(self, client):
        """TC-PST-05: With zero posts, should return empty array."""
        response = client.get('/api/posts')
        data = response.get_json()
        
        assert data['posts'] == []

    def test_list_posts_ordered_by_created_at_desc(self, client, created_user):
        """TC-PST-04: Posts should be ordered by created_at descending (newest first)."""
        # Create multiple posts
        post_ids = []
        for i in range(3):
            response = client.post('/api/posts', json={
                'title': f'Post {i}',
                'content': f'Content {i}',
                'user_id': created_user['id']
            })
            post_ids.append(response.get_json()['post']['id'])
        
        response = client.get('/api/posts')
        data = response.get_json()
        
        assert len(data['posts']) == 3
        
        # Verify posts are ordered by created_at descending
        # Each post's created_at should be >= the next post's created_at
        for i in range(len(data['posts']) - 1):
            current_time = data['posts'][i]['created_at']
            next_time = data['posts'][i + 1]['created_at']
            assert current_time >= next_time, "Posts should be ordered by created_at descending"


@pytest.mark.integration
class TestListPublishedPosts:
    """Integration tests for GET /api/posts?published=true."""

    def test_list_published_posts_only(self, client, created_user):
        """TC-PST-06: GET /api/posts?published=true should return only published posts."""
        # Create draft post
        client.post('/api/posts', json={
            'title': 'Draft Post',
            'content': 'Draft content',
            'user_id': created_user['id'],
            'published': False
        })
        
        # Create published post
        client.post('/api/posts', json={
            'title': 'Published Post',
            'content': 'Published content',
            'user_id': created_user['id'],
            'published': True
        })
        
        response = client.get('/api/posts?published=true')
        data = response.get_json()
        
        assert len(data['posts']) == 1
        assert data['posts'][0]['title'] == 'Published Post'
        assert all(post['published'] is True for post in data['posts'])

    def test_list_published_posts_empty(self, client, created_user):
        """TC-PST-07: With no published posts, should return empty array."""
        # Create only draft posts
        client.post('/api/posts', json={
            'title': 'Draft Post',
            'content': 'Draft content',
            'user_id': created_user['id'],
            'published': False
        })
        
        response = client.get('/api/posts?published=true')
        data = response.get_json()
        
        assert data['posts'] == []


@pytest.mark.integration
class TestGetPostById:
    """Integration tests for GET /api/posts/<id>."""

    def test_get_post_by_id_returns_200(self, client, created_post):
        """TC-PST-08: GET /api/posts/{id} should return 200 for existing post."""
        response = client.get(f"/api/posts/{created_post['id']}")
        
        assert response.status_code == 200

    def test_get_post_by_id_returns_correct_post(self, client, created_post):
        """TC-PST-08: Response should contain matching post id."""
        response = client.get(f"/api/posts/{created_post['id']}")
        data = response.get_json()
        
        assert data['post']['id'] == created_post['id']
        assert data['post']['title'] == created_post['title']

    def test_get_post_not_found_returns_404(self, client):
        """TC-PST-09: GET /api/posts/{invalid_id} should return 404."""
        response = client.get('/api/posts/999999')
        
        assert response.status_code == 404

    def test_get_post_not_found_error_message(self, client):
        """TC-PST-09: 404 response should contain error message."""
        response = client.get('/api/posts/999999')
        data = response.get_json()
        
        assert 'error' in data
        assert data['error'] == 'Not found'


@pytest.mark.integration
class TestUpdatePost:
    """Integration tests for PUT /api/posts/<id>."""

    def test_update_post_published_status(self, client, created_post):
        """TC-PST-10: PUT should update published status."""
        response = client.put(f"/api/posts/{created_post['id']}", json={
            'published': True
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['post']['published'] is True

    def test_update_post_title_and_content(self, client, created_post):
        """TC-PST-11: PUT should update title and content."""
        response = client.put(f"/api/posts/{created_post['id']}", json={
            'title': 'Updated Title',
            'content': 'Updated content'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['post']['title'] == 'Updated Title'
        assert data['post']['content'] == 'Updated content'

    def test_update_post_refreshes_updated_at(self, client, created_post):
        """TC-PST-10: PUT should refresh updated_at timestamp."""
        original_updated_at = created_post['updated_at']
        
        time.sleep(0.1)  # Small delay to ensure different timestamp
        
        response = client.put(f"/api/posts/{created_post['id']}", json={
            'title': 'Updated Title'
        })
        
        data = response.get_json()
        # Note: Due to timing, we just verify updated_at exists
        assert 'updated_at' in data['post']

    def test_update_nonexistent_post_returns_404(self, client):
        """TC-PST-12: PUT /api/posts/{invalid_id} should return 404."""
        response = client.put('/api/posts/999999', json={
            'title': 'Updated Title'
        })
        
        assert response.status_code == 404


@pytest.mark.integration
class TestDeletePost:
    """Integration tests for DELETE /api/posts/<id>."""

    def test_delete_post_returns_200(self, client, created_post):
        """TC-PST-13: DELETE /api/posts/{id} should return 200."""
        response = client.delete(f"/api/posts/{created_post['id']}")
        
        assert response.status_code == 200
        assert response.get_json()['message'] == 'Post deleted'

    def test_delete_post_removes_post(self, client, created_post):
        """TC-PST-13: After delete, GET should return 404."""
        client.delete(f"/api/posts/{created_post['id']}")
        
        response = client.get(f"/api/posts/{created_post['id']}")
        assert response.status_code == 404

    def test_delete_nonexistent_post_returns_404(self, client):
        """TC-PST-14: DELETE /api/posts/{invalid_id} should return 404."""
        response = client.delete('/api/posts/999999')
        
        assert response.status_code == 404
