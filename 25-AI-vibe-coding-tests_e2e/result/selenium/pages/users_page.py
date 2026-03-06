"""
users_page.py - Page Object for Users Tab

Handles interactions with the Users section:
- Creating new users
- Viewing user list
- Deleting users
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time


class UsersPage(BasePage):
    """Page object for the Users tab."""
    
    # Locators
    USERS_TAB = "//button[contains(@class, 'tab') and contains(text(), 'Users')]"
    
    # Form elements
    USERNAME_INPUT = "username"
    EMAIL_INPUT = "email"
    PASSWORD_INPUT = "password"
    CREATE_USER_BUTTON = "//button[@type='submit' and contains(text(), 'Create User')]"
    
    # List elements
    USERS_LIST = "usersList"
    USER_LIST_ITEM = ".list-item"
    DELETE_USER_BUTTON = "//button[contains(@class, 'btn-danger') and contains(text(), 'Delete')]"
    
    # Messages
    USER_MESSAGE = "userMessage"
    SUCCESS_MESSAGE = ".message.success"
    ERROR_MESSAGE = ".message.error"
    
    # Refresh
    REFRESH_LIST_BUTTON = "//button[contains(text(), 'Refresh List')]"
    
    def __init__(self, driver: WebDriver):
        """Initialize the Users page object."""
        super().__init__(driver)
    
    def navigate_to_users(self) -> 'UsersPage':
        """Click the Users tab to navigate to this section."""
        self.click_tab("Users")
        time.sleep(0.5)  # Wait for tab transition and data load
        return self
    
    def is_users_section_active(self) -> bool:
        """Check if the Users section is currently displayed."""
        users_section = self.find_element_by_id("users")
        return "active" in users_section.get_attribute("class")
    
    # =========================================================================
    # Create User Form
    # =========================================================================
    
    def enter_username(self, username: str) -> 'UsersPage':
        """Enter a username in the form."""
        self.type_text_by_id(self.USERNAME_INPUT, username)
        return self
    
    def enter_email(self, email: str) -> 'UsersPage':
        """Enter an email in the form."""
        self.type_text_by_id(self.EMAIL_INPUT, email)
        return self
    
    def enter_password(self, password: str) -> 'UsersPage':
        """Enter a password in the form."""
        self.type_text_by_id(self.PASSWORD_INPUT, password)
        return self
    
    def click_create_user(self) -> 'UsersPage':
        """Click the Create User button."""
        button = self.find_element_by_xpath(self.CREATE_USER_BUTTON)
        button.click()
        time.sleep(1)  # Wait for API response
        return self
    
    def create_user(self, username: str, email: str, password: str) -> 'UsersPage':
        """
        Fill out the form and create a new user.
        
        Args:
            username: The username for the new user
            email: The email for the new user
            password: The password for the new user
            
        Returns:
            Self for method chaining
        """
        self.enter_username(username)
        self.enter_email(email)
        self.enter_password(password)
        self.click_create_user()
        return self
    
    # =========================================================================
    # User List
    # =========================================================================
    
    def get_user_list_items(self) -> list:
        """Get all user list item elements."""
        return self.find_elements_by_css(self.USER_LIST_ITEM)
    
    def get_user_count(self) -> int:
        """Get the number of users displayed in the list."""
        items = self.get_user_list_items()
        return len(items)
    
    def user_exists_in_list(self, username: str) -> bool:
        """Check if a user with the given username exists in the list."""
        users_list = self.find_element_by_id(self.USERS_LIST)
        return username in users_list.text
    
    def get_user_id_from_list(self, username: str) -> int:
        """
        Get the ID of a user by their username.
        
        Args:
            username: The username to search for
            
        Returns:
            The user's ID, or -1 if not found
        """
        items = self.get_user_list_items()
        for item in items:
            if username in item.text:
                # Extract ID from text like "ID: 123"
                text = item.text
                if "ID:" in text:
                    try:
                        id_part = text.split("ID:")[1].split()[0].strip()
                        return int(id_part)
                    except (IndexError, ValueError):
                        continue
        return -1
    
    def click_refresh_list(self) -> 'UsersPage':
        """Click the refresh list button."""
        button = self.find_element_by_xpath(self.REFRESH_LIST_BUTTON)
        button.click()
        time.sleep(0.5)
        return self
    
    def delete_user_by_index(self, index: int) -> 'UsersPage':
        """
        Delete a user by their position in the list (0-indexed).
        
        Args:
            index: The position of the user in the list
        """
        items = self.get_user_list_items()
        if index < len(items):
            delete_btn = items[index].find_element(By.XPATH, ".//button[contains(@class, 'btn-danger')]")
            delete_btn.click()
            # Handle confirmation dialog
            self.driver.switch_to.alert.accept()
            time.sleep(0.5)
        return self
    
    # =========================================================================
    # Messages
    # =========================================================================
    
    def get_message_text(self) -> str:
        """Get the current message text."""
        try:
            message_el = self.find_element_by_id(self.USER_MESSAGE)
            return message_el.text
        except Exception:
            return ""
    
    def is_success_message_displayed(self) -> bool:
        """Check if a success message is displayed."""
        try:
            message_el = self.find_element_by_id(self.USER_MESSAGE)
            classes = message_el.get_attribute("class") or ""
            displayed = message_el.get_attribute("style") or ""
            return "success" in classes and "none" not in displayed
        except Exception:
            return False
    
    def is_error_message_displayed(self) -> bool:
        """Check if an error message is displayed."""
        try:
            message_el = self.find_element_by_id(self.USER_MESSAGE)
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
