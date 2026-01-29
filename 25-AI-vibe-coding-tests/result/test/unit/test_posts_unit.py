"""
Unit Tests for Post Validation and Serialization
Covers: TC-PST-01 to TC-PST-03 (Unit aspects)

These tests verify:
- Required field validation logic
- Post serialization structure
- Default values for published field
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'context', 'app', 'backend'))

from app import Post, User


@pytest.mark.unit
class TestPostValidation:
    """Unit tests for post validation logic."""

    def test_missing_title_returns_400(self, client, created_user):
        """TC-PST-02-U1: POST with missing title should return 400."""
        response = client.post('/api/posts', json={
            'content': 'Some content',
            'user_id': created_user['id']
        })
        
        assert response.status_code == 400
        assert response.get_json()['error'] == 'Missing required fields'

    def test_missing_content_returns_400(self, client, created_user):
        """TC-PST-02-U2: POST with missing content should return 400."""
        response = client.post('/api/posts', json={
            'title': 'Some title',
            'user_id': created_user['id']
        })
        
        assert response.status_code == 400
        assert response.get_json()['error'] == 'Missing required fields'

    def test_missing_user_id_returns_400(self, client):
        """TC-PST-02-U3: POST with missing user_id should return 400."""
        response = client.post('/api/posts', json={
            'title': 'Some title',
            'content': 'Some content'
        })
        
        assert response.status_code == 400
        assert response.get_json()['error'] == 'Missing required fields'

    def test_empty_body_returns_400(self, client):
        """TC-PST-02-U4: POST with empty body should return 400."""
        response = client.post('/api/posts', json={})
        
        assert response.status_code == 400
        assert response.get_json()['error'] == 'Missing required fields'

    def test_nonexistent_user_returns_404(self, client):
        """TC-PST-03: POST with non-existent user_id should return 404."""
        response = client.post('/api/posts', json={
            'title': 'Test title',
            'content': 'Test content',
            'user_id': 99999
        })
        
        assert response.status_code == 404
        assert response.get_json()['error'] == 'User not found'


@pytest.mark.unit
class TestPostSerialization:
    """Unit tests for post serialization (to_dict method)."""

    def test_post_to_dict_contains_required_fields(self, test_app):
        """TC-PST-01-U1: Post serialization should contain all required fields."""
        with test_app.app_context():
            from app import db
            # Create a user first (required for post)
            user = User(username='testuser', email='test@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
            
            post = Post(
                title='Test Post',
                content='Test content',
                user_id=user.id
            )
            db.session.add(post)
            db.session.commit()
            
            post_dict = post.to_dict()
            
            required_fields = ['id', 'title', 'content', 'published', 'author', 'created_at', 'updated_at']
            for field in required_fields:
                assert field in post_dict, f"Field '{field}' should be in serialized post"

    def test_post_author_is_username(self, test_app):
        """TC-PST-01-U2: Post author should be the username, not user_id."""
        with test_app.app_context():
            from app import db
            user = User(username='authorname', email='author@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
            
            post = Post(title='Test', content='Content', user_id=user.id)
            db.session.add(post)
            db.session.commit()
            
            post_dict = post.to_dict()
            
            assert post_dict['author'] == 'authorname'


@pytest.mark.unit
class TestPostDefaultValues:
    """Unit tests for post default values."""

    def test_published_defaults_to_false(self, client, created_user):
        """TC-PST-01-U3: Post should default to unpublished (draft)."""
        response = client.post('/api/posts', json={
            'title': 'Draft Post',
            'content': 'Some content',
            'user_id': created_user['id']
            # Note: published not specified
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['post']['published'] is False

    def test_published_can_be_set_true(self, client, created_user):
        """TC-PST-01-U4: Post can be created as published."""
        response = client.post('/api/posts', json={
            'title': 'Published Post',
            'content': 'Some content',
            'user_id': created_user['id'],
            'published': True
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['post']['published'] is True
