"""
posts_page.py - Page Object for Posts Tab

Handles interactions with the Posts section:
- Creating new posts
- Viewing post list
- Selecting author from dropdown
- Verifying published/draft status
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time


class PostsPage(BasePage):
    """Page object for the Posts tab."""
    
    # Locators
    POSTS_TAB = "//button[contains(@class, 'tab') and contains(text(), 'Posts')]"
    
    # Form elements
    TITLE_INPUT = "postTitle"
    CONTENT_INPUT = "postContent"
    USER_ID_SELECT = "postUserId"
    PUBLISHED_SELECT = "postPublished"
    CREATE_POST_BUTTON = "//button[@type='submit' and contains(text(), 'Create Post')]"
    
    # List elements
    POSTS_LIST = "postsList"
    POST_LIST_ITEM = ".list-item"
    BADGE_PUBLISHED = ".badge-success"
    BADGE_DRAFT = ".badge-secondary"
    DELETE_POST_BUTTON = "//button[contains(@class, 'btn-danger')]"
    
    # Messages
    POST_MESSAGE = "postMessage"
    SUCCESS_MESSAGE = ".message.success"
    ERROR_MESSAGE = ".message.error"
    
    # Refresh
    REFRESH_LIST_BUTTON = "//button[contains(text(), 'Refresh List')]"
    
    def __init__(self, driver: WebDriver):
        """Initialize the Posts page object."""
        super().__init__(driver)
    
    def navigate_to_posts(self) -> 'PostsPage':
        """Click the Posts tab to navigate to this section."""
        self.click_tab("Posts")
        time.sleep(1)  # Wait for tab transition and user dropdown to load
        return self
    
    def is_posts_section_active(self) -> bool:
        """Check if the Posts section is currently displayed."""
        posts_section = self.find_element_by_id("posts")
        return "active" in posts_section.get_attribute("class")
    
    # =========================================================================
    # Create Post Form
    # =========================================================================
    
    def enter_title(self, title: str) -> 'PostsPage':
        """Enter a title in the form."""
        self.type_text_by_id(self.TITLE_INPUT, title)
        return self
    
    def enter_content(self, content: str) -> 'PostsPage':
        """Enter content in the form."""
        self.type_text_by_id(self.CONTENT_INPUT, content)
        return self
    
    def select_author_by_index(self, index: int = 0) -> 'PostsPage':
        """
        Select an author from the dropdown by index.
        
        Args:
            index: The index of the author in the dropdown (0-indexed)
        """
        select_el = self.find_element_by_id(self.USER_ID_SELECT)
        select = Select(select_el)
        select.select_by_index(index)
        return self
    
    def select_author_by_value(self, user_id: int) -> 'PostsPage':
        """
        Select an author from the dropdown by user ID.
        
        Args:
            user_id: The ID of the user to select
        """
        select_el = self.find_element_by_id(self.USER_ID_SELECT)
        select = Select(select_el)
        select.select_by_value(str(user_id))
        return self
    
    def get_available_authors(self) -> list:
        """Get a list of available authors from the dropdown."""
        select_el = self.find_element_by_id(self.USER_ID_SELECT)
        select = Select(select_el)
        return [option.text for option in select.options]
    
    def author_exists_in_dropdown(self, username: str) -> bool:
        """Check if a specific author exists in the dropdown."""
        authors = self.get_available_authors()
        return any(username in author for author in authors)
    
    def set_status_draft(self) -> 'PostsPage':
        """Set the post status to Draft."""
        select_el = self.find_element_by_id(self.PUBLISHED_SELECT)
        select = Select(select_el)
        select.select_by_value("false")
        return self
    
    def set_status_published(self) -> 'PostsPage':
        """Set the post status to Published."""
        select_el = self.find_element_by_id(self.PUBLISHED_SELECT)
        select = Select(select_el)
        select.select_by_value("true")
        return self
    
    def click_create_post(self) -> 'PostsPage':
        """Click the Create Post button."""
        button = self.find_element_by_xpath(self.CREATE_POST_BUTTON)
        button.click()
        time.sleep(1)  # Wait for API response
        return self
    
    def create_post(self, title: str, content: str, author_index: int = 0, published: bool = False) -> 'PostsPage':
        """
        Fill out the form and create a new post.
        
        Args:
            title: The post title
            content: The post content
            author_index: Index of the author in the dropdown (0-indexed)
            published: Whether the post should be published (default: draft)
            
        Returns:
            Self for method chaining
        """
        self.enter_title(title)
        self.enter_content(content)
        self.select_author_by_index(author_index)
        
        if published:
            self.set_status_published()
        else:
            self.set_status_draft()
        
        self.click_create_post()
        return self
    
    # =========================================================================
    # Post List
    # =========================================================================
    
    def get_post_list_items(self) -> list:
        """Get all post list item elements."""
        posts_list = self.find_element_by_id(self.POSTS_LIST)
        return posts_list.find_elements(By.CSS_SELECTOR, self.POST_LIST_ITEM)
    
    def get_post_count(self) -> int:
        """Get the number of posts displayed in the list."""
        items = self.get_post_list_items()
        return len(items)
    
    def post_exists_in_list(self, title: str) -> bool:
        """Check if a post with the given title exists in the list."""
        posts_list = self.find_element_by_id(self.POSTS_LIST)
        return title in posts_list.text
    
    def get_post_status(self, title: str) -> str:
        """
        Get the status (Published/Draft) of a post by title.
        
        Args:
            title: The post title to search for
            
        Returns:
            'published', 'draft', or 'unknown'
        """
        items = self.get_post_list_items()
        for item in items:
            if title in item.text:
                # Check for badge classes
                try:
                    badge = item.find_element(By.CSS_SELECTOR, ".badge")
                    badge_classes = badge.get_attribute("class") or ""
                    if "badge-success" in badge_classes:
                        return "published"
                    elif "badge-secondary" in badge_classes:
                        return "draft"
                except Exception:
                    pass
        return "unknown"
    
    def is_post_published(self, title: str) -> bool:
        """Check if a specific post is published."""
        return self.get_post_status(title) == "published"
    
    def is_post_draft(self, title: str) -> bool:
        """Check if a specific post is a draft."""
        return self.get_post_status(title) == "draft"
    
    def click_refresh_list(self) -> 'PostsPage':
        """Click the refresh list button."""
        # Find the refresh button within the posts section
        posts_section = self.find_element_by_id("posts")
        buttons = posts_section.find_elements(By.XPATH, ".//button[contains(text(), 'Refresh')]")
        if buttons:
            buttons[0].click()
            time.sleep(0.5)
        return self
    
    # =========================================================================
    # Messages
    # =========================================================================
    
    def get_message_text(self) -> str:
        """Get the current message text."""
        try:
            message_el = self.find_element_by_id(self.POST_MESSAGE)
            return message_el.text
        except Exception:
            return ""
    
    def is_success_message_displayed(self) -> bool:
        """Check if a success message is displayed."""
        try:
            message_el = self.find_element_by_id(self.POST_MESSAGE)
            classes = message_el.get_attribute("class") or ""
            displayed = message_el.get_attribute("style") or ""
            return "success" in classes and "none" not in displayed
        except Exception:
            return False
    
    def is_error_message_displayed(self) -> bool:
        """Check if an error message is displayed."""
        try:
            message_el = self.find_element_by_id(self.POST_MESSAGE)
            classes = message_el.get_attribute("class") or ""
            displayed = message_el.get_attribute("style") or ""
            return "error" in classes and "none" not in displayed
        except Exception:
            return False
    
    def wait_for_success_message(self, timeout: int = 5) -> bool:
        """Wait for a success message to appear."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: self.is_success_message_displayed()
            )
            return True
        except Exception:
            return False
