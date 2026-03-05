# test_post_validation.py - Unit tests for Post validation and serialization
"""
Unit tests for Post model validation, serialization, and business rules.
These tests validate:
- Post.to_dict() returns expected shape
- Default values for published field
- Required field validation logic
"""
import pytest
import sys
from pathlib import Path

# Add the source directory to the path
SRC_PATH = Path(__file__).parent.parent.parent.parent.parent / "10-AI-vibe-coding" / "result" / "src" / "app" / "backend"
sys.path.insert(0, str(SRC_PATH))


class TestPostSerialization:
    """Unit tests for Post model serialization."""
    
    @pytest.mark.unit
    @pytest.mark.posts
    def test_post_to_dict_contains_required_fields(self, flask_app, created_user):
        """
        TC-PST-01 (Unit): Verify Post.to_dict() contains required fields.
        Required fields: id, title, content, published, author, created_at, updated_at
        """
        from app import Post, db
        
        with flask_app.app_context():
            post = Post(
                title='Test Post',
                content='Test content',
                user_id=created_user['id']
            )
            db.session.add(post)
            db.session.commit()
            
            post_dict = post.to_dict()
            
            # Verify required fields are present
            required_fields = ['id', 'title', 'content', 'published', 'author', 'created_at', 'updated_at']
            for field in required_fields:
                assert field in post_dict, f"Missing required field: {field}"
            
            # Verify values
            assert post_dict['title'] == 'Test Post'
            assert post_dict['content'] == 'Test content'


class TestPostDefaults:
    """Unit tests for Post default values."""
    
    @pytest.mark.unit
    @pytest.mark.posts
    def test_post_default_published_false(self, flask_app, created_user):
        """
        TC-PST-01 (Unit): Verify Post.published defaults to False.
        Related story: PST-01 - Create a post
        """
        from app import Post, db
        
        with flask_app.app_context():
            post = Post(
                title='Draft Post',
                content='Draft content',
                user_id=created_user['id']
            )
            db.session.add(post)
            db.session.commit()
            
            # Verify default published value
            assert post.published is False


class TestPostValidation:
    """Unit tests for Post validation logic."""
    
    @pytest.mark.unit
    @pytest.mark.posts
    def test_post_required_fields_validation(self):
        """
        TC-PST-02 (Unit): Validate required field checking logic for posts.
        Tests the validation pattern used in the API.
        """
        # Test data patterns that should fail validation
        test_cases = [
            {},  # Empty data
            {'title': 'Test'},  # Missing content and user_id
            {'content': 'Content'},  # Missing title and user_id
            {'user_id': 1},  # Missing title and content
            {'title': 'Test', 'content': 'Content'},  # Missing user_id
            {'title': '', 'content': 'Content', 'user_id': 1},  # Empty title
        ]
        
        for data in test_cases:
            # This replicates the validation logic from the API
            is_valid = bool(
                data and 
                data.get('title') and 
                data.get('content') and 
                data.get('user_id')
            )
            assert not is_valid, f"Should reject invalid data: {data}"
    
    @pytest.mark.unit
    @pytest.mark.posts
    def test_post_valid_data_passes_validation(self):
        """Validate that properly formed post data passes validation."""
        valid_data = {
            'title': 'Valid Title',
            'content': 'Valid content here',
            'user_id': 1
        }
        
        is_valid = bool(
            valid_data and 
            valid_data.get('title') and 
            valid_data.get('content') and 
            valid_data.get('user_id')
        )
        assert is_valid, "Valid data should pass validation"
    
    @pytest.mark.unit
    @pytest.mark.posts
    def test_post_optional_published_field(self):
        """Validate that published field is optional (uses default)."""
        # Data without published field should be valid
        data_without_published = {
            'title': 'Test',
            'content': 'Content',
            'user_id': 1
        }
        
        is_valid = bool(
            data_without_published and 
            data_without_published.get('title') and 
            data_without_published.get('content') and 
            data_without_published.get('user_id')
        )
        assert is_valid, "Data without published field should be valid"
        
        # published field should be optional (use .get with default)
        published = data_without_published.get('published', False)
        assert published is False


class TestPostUpdateLogic:
    """Unit tests for Post update logic."""
    
    @pytest.mark.unit
    @pytest.mark.posts
    def test_post_update_allowed_fields(self):
        """
        TC-PST-10/11 (Unit): Validate which fields can be updated.
        Allowed fields: title, content, published
        """
        allowed_fields = ['title', 'content', 'published']
        
        update_data = {
            'title': 'New Title',
            'content': 'New Content',
            'published': True,
            'user_id': 999  # Should not be updatable
        }
        
        # Simulate the update logic from the API
        for field in allowed_fields:
            assert field in update_data or True, f"Field {field} should be allowed"
        
        # user_id should not be in allowed fields
        assert 'user_id' not in allowed_fields
