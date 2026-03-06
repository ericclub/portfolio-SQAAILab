"""
test_user_post_flow.py - E2E Tests for User and Post Creation Flow

Test Cases covered:
- TC-E2E-03: Create user and then create draft post via UI
- TC-E2E-04: Create published post variant

Story Reference: E2E-02 (Admin can create user then create post via UI)
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pages.users_page import UsersPage
from pages.posts_page import PostsPage
from pages.statistics_page import StatisticsPage


@pytest.mark.e2e
@pytest.mark.users
@pytest.mark.posts
class TestUserPostCreationFlow:
    """Tests for the complete user → post creation workflow."""
    
    def test_create_user_and_draft_post(self, driver, base_url, unique_user_data, unique_post_data):
        """
        TC-E2E-03: Create a user and then create a draft post via UI
        
        Story: E2E-02 - Admin can create user then create post via UI
        
        Given the backend server is running
        When I open the Users tab
        And I submit the Create User form with a unique username, email, and password
        Then the UI shows a success message
        And the new user appears in the User List with a visible ID
        
        When I open the Posts tab
        Then the Author dropdown contains the created user
        When I submit the Create Post form with title/content/author and Draft status
        Then the UI shows a success message
        And the new post appears in the Post List with the correct title and Draft badge
        """
        # Navigate to the application
        driver.get(base_url)
        
        # =====================================================================
        # STEP 1: Create a new user
        # =====================================================================
        print(f"\n📝 Creating user: {unique_user_data['username']}")
        
        users_page = UsersPage(driver)
        users_page.navigate_to_users()
        
        # Verify we're on the users tab
        assert users_page.is_users_section_active(), \
            "Users section should be active"
        
        # Get initial user count
        initial_user_count = users_page.get_user_count()
        print(f"   Initial user count: {initial_user_count}")
        
        # Create the user
        users_page.create_user(
            username=unique_user_data['username'],
            email=unique_user_data['email'],
            password=unique_user_data['password']
        )
        
        # Verify success message
        assert users_page.wait_for_success_message(timeout=5), \
            "Success message should be displayed after creating user"
        
        # Refresh the list to ensure we see the new user
        users_page.click_refresh_list()
        
        # Verify user appears in the list
        assert users_page.user_exists_in_list(unique_user_data['username']), \
            f"User '{unique_user_data['username']}' should appear in the user list"
        
        # Verify user count increased
        new_user_count = users_page.get_user_count()
        assert new_user_count > initial_user_count, \
            f"User count should increase (was {initial_user_count}, now {new_user_count})"
        
        print(f"   ✅ User created successfully")
        print(f"   New user count: {new_user_count}")
        
        # =====================================================================
        # STEP 2: Navigate to Posts and verify author dropdown
        # =====================================================================
        print(f"\n📝 Creating draft post: {unique_post_data['title']}")
        
        posts_page = PostsPage(driver)
        posts_page.navigate_to_posts()
        
        # Verify we're on the posts tab
        assert posts_page.is_posts_section_active(), \
            "Posts section should be active"
        
        # Verify the created user appears in the author dropdown
        assert posts_page.author_exists_in_dropdown(unique_user_data['username']), \
            f"User '{unique_user_data['username']}' should appear in the author dropdown"
        
        print(f"   ✅ User appears in author dropdown")
        
        # =====================================================================
        # STEP 3: Create a draft post
        # =====================================================================
        
        # Get initial post count
        initial_post_count = posts_page.get_post_count()
        print(f"   Initial post count: {initial_post_count}")
        
        # Create the post as DRAFT
        posts_page.create_post(
            title=unique_post_data['title'],
            content=unique_post_data['content'],
            author_index=0,  # Select first author (most recently added)
            published=False  # Draft
        )
        
        # Verify success message
        assert posts_page.wait_for_success_message(timeout=5), \
            "Success message should be displayed after creating post"
        
        # Refresh the list
        posts_page.click_refresh_list()
        
        # Verify post appears in the list
        assert posts_page.post_exists_in_list(unique_post_data['title']), \
            f"Post '{unique_post_data['title']}' should appear in the post list"
        
        # Verify post is marked as draft
        assert posts_page.is_post_draft(unique_post_data['title']), \
            f"Post '{unique_post_data['title']}' should be marked as Draft"
        
        # Verify post count increased
        new_post_count = posts_page.get_post_count()
        assert new_post_count > initial_post_count, \
            f"Post count should increase (was {initial_post_count}, now {new_post_count})"
        
        print(f"   ✅ Draft post created successfully")
        print(f"   Post status: Draft")
        print(f"   New post count: {new_post_count}")
        
        print(f"\n✅ TC-E2E-03 PASSED: User and draft post creation flow completed")
    
    def test_create_published_post(self, driver, base_url, unique_user_data, unique_post_data):
        """
        TC-E2E-04: Create a published post via UI
        
        Story: E2E-02 - Admin can create user then create post via UI (Published variant)
        
        Given a user exists (we create one for isolation)
        When I open the Posts tab
        And I submit the Create Post form with title/content/author and Published status
        Then the UI shows a success message
        And the new post appears in the Post List with Published badge
        """
        # Navigate to the application
        driver.get(base_url)
        
        # =====================================================================
        # STEP 1: Create a new user for this test (isolation)
        # =====================================================================
        print(f"\n📝 Creating user for published post test: {unique_user_data['username']}")
        
        users_page = UsersPage(driver)
        users_page.navigate_to_users()
        
        users_page.create_user(
            username=unique_user_data['username'],
            email=unique_user_data['email'],
            password=unique_user_data['password']
        )
        
        assert users_page.wait_for_success_message(timeout=5), \
            "Success message should be displayed after creating user"
        
        print(f"   ✅ User created")
        
        # =====================================================================
        # STEP 2: Create a published post
        # =====================================================================
        # Modify post title to indicate it's published
        published_post_title = f"Published - {unique_post_data['title']}"
        print(f"\n📝 Creating published post: {published_post_title}")
        
        posts_page = PostsPage(driver)
        posts_page.navigate_to_posts()
        
        # Create the post as PUBLISHED
        posts_page.create_post(
            title=published_post_title,
            content=unique_post_data['content'],
            author_index=0,
            published=True  # Published!
        )
        
        # Verify success message
        assert posts_page.wait_for_success_message(timeout=5), \
            "Success message should be displayed after creating post"
        
        # Refresh the list
        posts_page.click_refresh_list()
        
        # Verify post appears in the list
        assert posts_page.post_exists_in_list(published_post_title), \
            f"Post '{published_post_title}' should appear in the post list"
        
        # Verify post is marked as published
        assert posts_page.is_post_published(published_post_title), \
            f"Post '{published_post_title}' should be marked as Published"
        
        print(f"   ✅ Published post created successfully")
        print(f"   Post status: Published")
        
        # =====================================================================
        # STEP 3: Verify statistics reflect the new data
        # =====================================================================
        print(f"\n📊 Verifying statistics updated")
        
        stats_page = StatisticsPage(driver)
        stats_page.navigate_to_stats()
        
        # Refresh stats to ensure we get latest data
        stats_page.click_refresh()
        
        stats = stats_page.get_stat_values()
        
        # Published posts count should be at least 1
        assert stats['published_posts'] >= 1, \
            f"Published posts count should be at least 1, got: {stats['published_posts']}"
        
        print(f"   Users: {stats['users']}")
        print(f"   Total Posts: {stats['total_posts']}")
        print(f"   Published Posts: {stats['published_posts']}")
        
        print(f"\n✅ TC-E2E-04 PASSED: Published post creation flow completed")
