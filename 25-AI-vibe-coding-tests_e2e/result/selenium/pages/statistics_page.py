"""
statistics_page.py - Page Object for Statistics Tab

Handles interactions with the Statistics section:
- Reading stat values (users, total posts, published posts)
- Refreshing statistics
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time


class StatisticsPage(BasePage):
    """Page object for the Statistics tab."""
    
    # Locators
    STATS_TAB = "//button[contains(@class, 'tab') and contains(text(), 'Statistics')]"
    STATS_CONTAINER = "statsContainer"
    STAT_CARDS = ".stat-card"
    STAT_NUMBER = ".stat-number"
    STAT_LABEL = ".stat-label"
    REFRESH_BUTTON = "//button[contains(text(), 'Refresh')]"
    LOADING_INDICATOR = ".loading"
    ERROR_STATE = ".empty-state"
    
    def __init__(self, driver: WebDriver):
        """Initialize the Statistics page object."""
        super().__init__(driver)
    
    def navigate_to_stats(self) -> 'StatisticsPage':
        """Click the Statistics tab to navigate to this section."""
        self.click_tab("Statistics")
        # Wait for stats to load
        self._wait_for_stats_loaded()
        return self
    
    def _wait_for_stats_loaded(self, timeout: int = 10) -> None:
        """Wait for statistics to be loaded (loading indicator disappears)."""
        # Wait for stat cards to appear or error state
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, self.STAT_CARDS)) > 0
                or len(d.find_elements(By.CSS_SELECTOR, self.ERROR_STATE)) > 0
            )
        except Exception:
            pass  # Continue even if timeout - test will validate state
    
    def is_stats_section_active(self) -> bool:
        """Check if the Statistics section is currently displayed."""
        stats_section = self.find_element_by_id("stats")
        return "active" in stats_section.get_attribute("class")
    
    def get_stats_cards(self) -> list:
        """Get all stat card elements."""
        return self.find_elements_by_css(self.STAT_CARDS)
    
    def get_stat_values(self) -> dict:
        """
        Get all statistics values from the cards.
        
        Returns:
            dict: {
                'users': int,
                'total_posts': int,
                'published_posts': int
            }
        """
        stats = {
            'users': 0,
            'total_posts': 0,
            'published_posts': 0
        }
        
        cards = self.get_stats_cards()
        for card in cards:
            try:
                number_el = card.find_element(By.CSS_SELECTOR, self.STAT_NUMBER)
                label_el = card.find_element(By.CSS_SELECTOR, self.STAT_LABEL)
                
                value = int(number_el.text)
                label = label_el.text.lower()
                
                if 'user' in label:
                    stats['users'] = value
                elif 'total' in label or ('post' in label and 'published' not in label):
                    stats['total_posts'] = value
                elif 'published' in label:
                    stats['published_posts'] = value
            except (ValueError, Exception):
                continue
        
        return stats
    
    def get_users_count(self) -> int:
        """Get the number of users from statistics."""
        return self.get_stat_values()['users']
    
    def get_total_posts_count(self) -> int:
        """Get the total number of posts from statistics."""
        return self.get_stat_values()['total_posts']
    
    def get_published_posts_count(self) -> int:
        """Get the number of published posts from statistics."""
        return self.get_stat_values()['published_posts']
    
    def click_refresh(self) -> 'StatisticsPage':
        """Click the refresh button to reload statistics."""
        refresh_btn = self.find_element_by_xpath(self.REFRESH_BUTTON)
        refresh_btn.click()
        # Give time for API call
        time.sleep(0.5)
        self._wait_for_stats_loaded()
        return self
    
    def has_loading_error(self) -> bool:
        """Check if there's a loading error displayed."""
        try:
            container = self.find_element_by_id(self.STATS_CONTAINER)
            return "error" in container.text.lower()
        except Exception:
            return False
    
    def stats_are_displayed(self) -> bool:
        """Check if statistics are properly displayed (not loading or error)."""
        cards = self.get_stats_cards()
        if len(cards) != 3:
            return False
        
        # Check each card has a valid number
        for card in cards:
            try:
                number_el = card.find_element(By.CSS_SELECTOR, self.STAT_NUMBER)
                int(number_el.text)  # Should be a valid integer
            except (ValueError, Exception):
                return False
        
        return True
