# test_posts.py - Integration tests for Posts API endpoints
"""
Integration tests for the Posts API endpoints.
Tests stories: PST-01, PST-02, PST-03, PST-04, PST-05, PST-06
"""
import pytest
import time


class TestCreatePost:
    """Integration tests for POST /api/posts endpoint (PST-01)."""
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_create_post_with_valid_data(self, client, created_user, sample_post_data):
        """
        TC-PST-01 (Integration): Create post with valid input.
        
        Scenario: Create post with valid input
        - Given a user exists with ID U
        - When I send a POST request to /api/posts with title, content, and user_id = U
        - Then the response status code is 201
        """
        post_data = {**sample_post_data, 'user_id': created_user['id']}
        
        response = client.post('/api/posts', json=post_data)
        
        assert response.status_code == 201
        
        data = response.get_json()
        assert 'post' in data
        assert data['post']['title'] == sample_post_data['title']
        assert data['post']['content'] == sample_post_data['content']
        assert data['post']['author'] == created_user['username']
        assert 'id' in data['post']
        assert 'created_at' in data['post']
        assert 'updated_at' in data['post']
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_create_post_missing_title(self, client, created_user):
        """
        TC-PST-02 (Integration): Reject missing required fields (title).
        
        Scenario: Reject missing required fields
        - Given the request payload is missing title
        - When I send a POST request to /api/posts
        - Then the response status code is 400
        """
        response = client.post('/api/posts', json={
            'content': 'Test content',
            'user_id': created_user['id']
        })
        
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'error' in data
        assert 'Missing required fields' in data['error']
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_create_post_missing_content(self, client, created_user):
        """
        TC-PST-02 (Integration): Reject missing required fields (content).
        """
        response = client.post('/api/posts', json={
            'title': 'Test Title',
            'user_id': created_user['id']
        })
        
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'error' in data
        assert 'Missing required fields' in data['error']
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_create_post_missing_user_id(self, client):
        """
        TC-PST-02 (Integration): Reject missing required fields (user_id).
        """
        response = client.post('/api/posts', json={
            'title': 'Test Title',
            'content': 'Test content'
        })
        
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'error' in data
        assert 'Missing required fields' in data['error']
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_create_post_user_not_found(self, client):
        """
        TC-PST-03 (Integration): Reject unknown author.
        
        Scenario: Reject unknown author
        - Given no user exists with ID U
        - When I send a POST request to /api/posts with user_id = U
        - Then the response status code is 404
        """
        response = client.post('/api/posts', json={
            'title': 'Test Title',
            'content': 'Test content',
            'user_id': 999999
        })
        
        assert response.status_code == 404
        
        data = response.get_json()
        assert 'error' in data
        assert 'User not found' in data['error']
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_create_post_default_published_false(self, client, created_user):
        """Verify post defaults to unpublished (draft)."""
        response = client.post('/api/posts', json={
            'title': 'Draft Post',
            'content': 'Draft content',
            'user_id': created_user['id']
        })
        
        assert response.status_code == 201
        
        data = response.get_json()
        assert data['post']['published'] is False


class TestListPosts:
    """Integration tests for GET /api/posts endpoint (PST-02, PST-03)."""
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_list_all_posts(self, client):
        """
        TC-PST-04/05 (Integration): Retrieve all posts.
        
        Scenario: Retrieve all posts
        - When I send a GET request to /api/posts
        - Then the response status code is 200
        - And the response contains a posts array
        """
        response = client.get('/api/posts')
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'posts' in data
        assert isinstance(data['posts'], list)
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_list_posts_empty_database(self, client):
        """
        TC-PST-05 (Integration): With zero posts.
        """
        response = client.get('/api/posts')
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['posts'] == []
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_list_posts_ordered_by_created_at_desc(self, client, created_user):
        """
        TC-PST-04 (Integration): Posts are ordered by created_at descending.
        """
        # Create first post
        client.post('/api/posts', json={
            'title': 'First Post',
            'content': 'First content',
            'user_id': created_user['id']
        })
        
        # Delay to ensure different timestamps (1.1 seconds for SQLite resolution)
        time.sleep(1.1)
        
        # Create second post
        client.post('/api/posts', json={
            'title': 'Second Post',
            'content': 'Second content',
            'user_id': created_user['id']
        })
        
        # Get posts
        response = client.get('/api/posts')
        data = response.get_json()
        
        # Newest first
        assert data['posts'][0]['title'] == 'Second Post'
        assert data['posts'][1]['title'] == 'First Post'
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_list_published_posts_only(self, client, created_user):
        """
        TC-PST-06 (Integration): Filter to published posts only.
        
        Scenario: Filter to published posts
        - Given there are both draft and published posts
        - When I send a GET request to /api/posts?published=true
        - Then every returned post has published = true
        """
        # Create a draft post
        client.post('/api/posts', json={
            'title': 'Draft Post',
            'content': 'Draft content',
            'user_id': created_user['id'],
            'published': False
        })
        
        # Create a published post
        client.post('/api/posts', json={
            'title': 'Published Post',
            'content': 'Published content',
            'user_id': created_user['id'],
            'published': True
        })
        
        # Get only published posts
        response = client.get('/api/posts?published=true')
        data = response.get_json()
        
        # Should only have published post
        assert len(data['posts']) == 1
        assert data['posts'][0]['title'] == 'Published Post'
        assert data['posts'][0]['published'] is True
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_list_published_posts_empty(self, client, created_user):
        """
        TC-PST-07 (Integration): If no published posts exist.
        """
        # Create only draft posts
        client.post('/api/posts', json={
            'title': 'Draft Post',
            'content': 'Draft content',
            'user_id': created_user['id'],
            'published': False
        })
        
        # Get only published posts
        response = client.get('/api/posts?published=true')
        data = response.get_json()
        
        assert data['posts'] == []


class TestGetPostById:
    """Integration tests for GET /api/posts/<id> endpoint (PST-04)."""
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_get_post_by_valid_id(self, client, created_post):
        """
        TC-PST-08 (Integration): Retrieve post details by valid ID.
        
        Scenario: Retrieve post details by valid ID
        - Given a post exists with ID P
        - When I send a GET request to /api/posts/P
        - Then the response status code is 200
        """
        post_id = created_post['id']
        
        response = client.get(f'/api/posts/{post_id}')
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'post' in data
        assert data['post']['id'] == post_id
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_get_post_not_found(self, client):
        """
        TC-PST-09 (Integration): Post does not exist.
        
        Scenario: Post does not exist
        - Given no post exists with ID P
        - When I send a GET request to /api/posts/P
        - Then the response status code is 404
        """
        response = client.get('/api/posts/999999')
        
        assert response.status_code == 404
        
        data = response.get_json()
        assert 'error' in data


class TestUpdatePost:
    """Integration tests for PUT /api/posts/<id> endpoint (PST-05)."""
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_update_post_publish(self, client, created_post):
        """
        TC-PST-10 (Integration): Update post to published.
        
        Scenario: Update one or more fields
        - Given a post exists with ID P
        - When I send a PUT request to /api/posts/P with published: true
        - Then the response status code is 200
        - And the returned post reflects the updated fields
        """
        post_id = created_post['id']
        
        response = client.put(f'/api/posts/{post_id}', json={'published': True})
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['post']['published'] is True
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_update_post_title_and_content(self, client, created_post):
        """
        TC-PST-11 (Integration): Update title and content.
        """
        post_id = created_post['id']
        
        response = client.put(f'/api/posts/{post_id}', json={
            'title': 'Updated Title',
            'content': 'Updated content'
        })
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['post']['title'] == 'Updated Title'
        assert data['post']['content'] == 'Updated content'
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_update_post_refreshes_updated_at(self, client, created_post):
        """Verify updated_at is refreshed on update."""
        post_id = created_post['id']
        original_updated_at = created_post['updated_at']
        
        # Delay to ensure different timestamp (1.1 seconds for SQLite resolution)
        time.sleep(1.1)
        
        response = client.put(f'/api/posts/{post_id}', json={'title': 'New Title'})
        
        data = response.get_json()
        # updated_at should be different (refreshed)
        assert data['post']['updated_at'] != original_updated_at
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_update_post_not_found(self, client):
        """
        TC-PST-12 (Integration): Update non-existent post.
        
        Scenario: Update non-existent post
        - Given no post exists with ID P
        - When I send a PUT request to /api/posts/P
        - Then the response status code is 404
        """
        response = client.put('/api/posts/999999', json={'title': 'New Title'})
        
        assert response.status_code == 404


class TestDeletePost:
    """Integration tests for DELETE /api/posts/<id> endpoint (PST-06)."""
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_delete_post_success(self, client, created_post):
        """
        TC-PST-13 (Integration): Delete a post.
        
        Scenario: Delete a post
        - Given a post exists with ID P
        - When I send a DELETE request to /api/posts/P
        - Then the response status code is 200
        """
        post_id = created_post['id']
        
        # Delete post
        response = client.delete(f'/api/posts/{post_id}')
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'message' in data
        assert 'deleted' in data['message'].lower()
        
        # Verify post is deleted
        get_response = client.get(f'/api/posts/{post_id}')
        assert get_response.status_code == 404
    
    @pytest.mark.integration
    @pytest.mark.posts
    def test_delete_post_not_found(self, client):
        """
        TC-PST-14 (Integration): Delete non-existent post.
        
        Scenario: Delete non-existent post
        - Given no post exists with ID P
        - When I send a DELETE request to /api/posts/P
        - Then the response status code is 404
        """
        response = client.delete('/api/posts/999999')
        
        assert response.status_code == 404
