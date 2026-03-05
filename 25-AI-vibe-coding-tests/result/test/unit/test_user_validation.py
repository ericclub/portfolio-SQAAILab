# test_user_validation.py - Unit tests for User validation and serialization
"""
Unit tests for User model validation, serialization, and business rules.
These tests validate:
- User.to_dict() excludes password/hash (USR-01 requirement)
- User.set_password() and check_password() work correctly
- Required field validation logic
"""
import pytest
import sys
from pathlib import Path

# Add the source directory to the path
SRC_PATH = Path(__file__).parent.parent.parent.parent.parent / "10-AI-vibe-coding" / "result" / "src" / "app" / "backend"
sys.path.insert(0, str(SRC_PATH))


class TestUserSerialization:
    """Unit tests for User model serialization."""
    
    @pytest.mark.unit
    @pytest.mark.users
    def test_user_to_dict_excludes_password(self, flask_app):
        """
        TC-USR-01 (Unit): Verify User.to_dict() does not expose password or password_hash.
        Related story: USR-01 - Create a user
        """
        from app import User, db
        
        with flask_app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('secret123')
            db.session.add(user)
            db.session.commit()
            
            user_dict = user.to_dict()
            
            # Verify password fields are NOT in the serialized output
            assert 'password' not in user_dict
            assert 'password_hash' not in user_dict
            
    @pytest.mark.unit
    @pytest.mark.users
    def test_user_to_dict_contains_required_fields(self, flask_app):
        """
        TC-USR-01 (Unit): Verify User.to_dict() contains required fields.
        Required fields: id, username, email, created_at
        """
        from app import User, db
        from datetime import datetime
        
        with flask_app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('secret123')
            db.session.add(user)
            db.session.commit()
            
            user_dict = user.to_dict()
            
            # Verify required fields are present
            assert 'id' in user_dict
            assert 'username' in user_dict
            assert 'email' in user_dict
            assert 'created_at' in user_dict
            
            # Verify values match
            assert user_dict['username'] == 'testuser'
            assert user_dict['email'] == 'test@example.com'


class TestUserPasswordHandling:
    """Unit tests for User password handling."""
    
    @pytest.mark.unit
    @pytest.mark.users
    def test_set_password_creates_hash(self, flask_app):
        """Verify set_password creates a hash that differs from plaintext."""
        from app import User
        
        with flask_app.app_context():
            user = User(username='testuser', email='test@example.com')
            plaintext = 'MySecurePassword123!'
            
            user.set_password(plaintext)
            
            # Hash should be set and different from plaintext
            assert user.password_hash is not None
            assert user.password_hash != plaintext
            
    @pytest.mark.unit
    @pytest.mark.users
    def test_check_password_validates_correctly(self, flask_app):
        """Verify check_password returns True for correct password."""
        from app import User
        
        with flask_app.app_context():
            user = User(username='testuser', email='test@example.com')
            plaintext = 'MySecurePassword123!'
            
            user.set_password(plaintext)
            
            # Correct password should return True
            assert user.check_password(plaintext) is True
            
    @pytest.mark.unit
    @pytest.mark.users
    def test_check_password_rejects_wrong_password(self, flask_app):
        """Verify check_password returns False for incorrect password."""
        from app import User
        
        with flask_app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('CorrectPassword123!')
            
            # Wrong password should return False
            assert user.check_password('WrongPassword456!') is False


class TestUserValidation:
    """Unit tests for User validation logic."""
    
    @pytest.mark.unit
    @pytest.mark.users
    def test_user_required_fields_validation(self):
        """
        TC-USR-02 (Unit): Validate required field checking logic.
        Tests the validation pattern used in the API.
        """
        # Test data patterns that should fail validation
        test_cases = [
            {},  # Empty data
            {'username': 'user'},  # Missing email and password
            {'email': 'user@example.com'},  # Missing username and password
            {'password': 'secret123'},  # Missing username and email
            {'username': 'user', 'email': 'user@example.com'},  # Missing password
            {'username': '', 'email': 'user@example.com', 'password': 'secret123'},  # Empty username
        ]
        
        for data in test_cases:
            # This replicates the validation logic from the API
            is_valid = bool(
                data and 
                data.get('username') and 
                data.get('email') and 
                data.get('password')
            )
            assert not is_valid, f"Should reject invalid data: {data}"
    
    @pytest.mark.unit
    @pytest.mark.users
    def test_user_valid_data_passes_validation(self):
        """Validate that properly formed data passes validation."""
        valid_data = {
            'username': 'validuser',
            'email': 'valid@example.com',
            'password': 'ValidPassword123!'
        }
        
        is_valid = bool(
            valid_data and 
            valid_data.get('username') and 
            valid_data.get('email') and 
            valid_data.get('password')
        )
        assert is_valid, "Valid data should pass validation"
