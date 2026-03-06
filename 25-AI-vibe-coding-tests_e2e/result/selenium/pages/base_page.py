"""
base_page.py - Base Page Object with common methods

Provides shared functionality for all page objects:
- Element waiting and finding
- Click and input actions
- Common assertions
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import List, Optional


class BasePage:
    """Base class for all page objects."""
    
    DEFAULT_TIMEOUT = 10
    
    def __init__(self, driver: WebDriver):
        """Initialize the page object with a WebDriver instance."""
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)
    
    # =========================================================================
    # Navigation
    # =========================================================================
    
    def navigate_to(self, url: str) -> None:
        """Navigate to a URL."""
        self.driver.get(url)
    
    def get_current_url(self) -> str:
        """Get the current page URL."""
        return self.driver.current_url
    
    def get_title(self) -> str:
        """Get the page title."""
        return self.driver.title
    
    def refresh(self) -> None:
        """Refresh the current page."""
        self.driver.refresh()
    
    # =========================================================================
    # Element Finding
    # =========================================================================
    
    def find_element(self, by: By, value: str) -> WebElement:
        """Find a single element."""
        return self.driver.find_element(by, value)
    
    def find_elements(self, by: By, value: str) -> List[WebElement]:
        """Find multiple elements."""
        return self.driver.find_elements(by, value)
    
    def find_element_by_id(self, element_id: str) -> WebElement:
        """Find an element by its ID."""
        return self.find_element(By.ID, element_id)
    
    def find_element_by_css(self, css_selector: str) -> WebElement:
        """Find an element by CSS selector."""
        return self.find_element(By.CSS_SELECTOR, css_selector)
    
    def find_elements_by_css(self, css_selector: str) -> List[WebElement]:
        """Find elements by CSS selector."""
        return self.find_elements(By.CSS_SELECTOR, css_selector)
    
    def find_element_by_xpath(self, xpath: str) -> WebElement:
        """Find an element by XPath."""
        return self.find_element(By.XPATH, xpath)
    
    # =========================================================================
    # Waiting
    # =========================================================================
    
    def wait_for_element(self, by: By, value: str, timeout: int = None) -> WebElement:
        """Wait for an element to be present and visible."""
        timeout = timeout or self.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located((by, value)))
    
    def wait_for_element_by_id(self, element_id: str, timeout: int = None) -> WebElement:
        """Wait for an element by ID to be visible."""
        return self.wait_for_element(By.ID, element_id, timeout)
    
    def wait_for_element_by_css(self, css_selector: str, timeout: int = None) -> WebElement:
        """Wait for an element by CSS selector to be visible."""
        return self.wait_for_element(By.CSS_SELECTOR, css_selector, timeout)
    
    def wait_for_element_clickable(self, by: By, value: str, timeout: int = None) -> WebElement:
        """Wait for an element to be clickable."""
        timeout = timeout or self.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, value)))
    
    def wait_for_text_in_element(self, by: By, value: str, text: str, timeout: int = None) -> bool:
        """Wait for specific text to appear in an element."""
        timeout = timeout or self.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, timeout)
        try:
            return wait.until(EC.text_to_be_present_in_element((by, value), text))
        except TimeoutException:
            return False
    
    def wait_for_element_to_disappear(self, by: By, value: str, timeout: int = None) -> bool:
        """Wait for an element to disappear."""
        timeout = timeout or self.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, timeout)
        try:
            return wait.until(EC.invisibility_of_element_located((by, value)))
        except TimeoutException:
            return False
    
    # =========================================================================
    # Actions
    # =========================================================================
    
    def click(self, element: WebElement) -> None:
        """Click an element."""
        element.click()
    
    def click_by_css(self, css_selector: str) -> None:
        """Find and click an element by CSS selector."""
        element = self.wait_for_element_clickable(By.CSS_SELECTOR, css_selector)
        element.click()
    
    def click_by_id(self, element_id: str) -> None:
        """Find and click an element by ID."""
        element = self.wait_for_element_clickable(By.ID, element_id)
        element.click()
    
    def type_text(self, element: WebElement, text: str, clear_first: bool = True) -> None:
        """Type text into an input element."""
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def type_text_by_id(self, element_id: str, text: str, clear_first: bool = True) -> None:
        """Find an element by ID and type text into it."""
        element = self.wait_for_element_by_id(element_id)
        self.type_text(element, text, clear_first)
    
    def get_text(self, element: WebElement) -> str:
        """Get the text content of an element."""
        return element.text
    
    def get_text_by_css(self, css_selector: str) -> str:
        """Get text from an element found by CSS selector."""
        element = self.wait_for_element_by_css(css_selector)
        return element.text
    
    def get_attribute(self, element: WebElement, attribute: str) -> Optional[str]:
        """Get an attribute value from an element."""
        return element.get_attribute(attribute)
    
    # =========================================================================
    # Assertions / Checks
    # =========================================================================
    
    def is_element_present(self, by: By, value: str) -> bool:
        """Check if an element is present on the page."""
        elements = self.driver.find_elements(by, value)
        return len(elements) > 0
    
    def is_element_visible(self, by: By, value: str) -> bool:
        """Check if an element is visible on the page."""
        try:
            element = self.driver.find_element(by, value)
            return element.is_displayed()
        except Exception:
            return False
    
    def element_contains_text(self, element: WebElement, text: str) -> bool:
        """Check if an element contains specific text."""
        return text in element.text
    
    # =========================================================================
    # Tab Navigation (specific to this app)
    # =========================================================================
    
    def click_tab(self, tab_text: str) -> None:
        """Click a navigation tab by its text content."""
        tabs = self.find_elements_by_css(".tab")
        for tab in tabs:
            if tab_text.lower() in tab.text.lower():
                tab.click()
                return
        raise ValueError(f"Tab with text '{tab_text}' not found")
    
    def is_tab_active(self, tab_text: str) -> bool:
        """Check if a specific tab is currently active."""
        tabs = self.find_elements_by_css(".tab.active")
        for tab in tabs:
            if tab_text.lower() in tab.text.lower():
                return True
        return False
