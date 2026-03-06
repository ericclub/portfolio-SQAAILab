"""
conftest.py - Pytest fixtures for Selenium E2E tests

This module provides shared fixtures for browser automation:
- WebDriver setup with Chrome (headless mode configurable via --headless flag)
- Base URL configuration
- Screenshot on test failure
- Test data cleanup between tests
"""

import pytest
import os
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode (no browser window)"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="http://localhost:5000",
        help="Base URL for the application under test"
    )


@pytest.fixture(scope="session")
def base_url(request):
    """Get the base URL for the application."""
    return request.config.getoption("--base-url")


def _create_chrome_driver(headless: bool):
    """Create Chrome WebDriver with appropriate options."""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Try different approaches to create the driver
    errors = []
    
    # Approach 1: Use selenium's built-in driver manager (Selenium 4.6+)
    # This works without network access if chromedriver is in PATH or cache
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        errors.append(f"selenium default: {str(e)[:100]}")
    
    # Approach 2: Use webdriver_manager if available and working
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        errors.append(f"webdriver_manager: {str(e)[:100]}")
    
    # Approach 3: Look for chromedriver in common locations
    common_paths = [
        r"C:\chromedriver\chromedriver.exe",
        r"C:\Program Files\chromedriver\chromedriver.exe",
        r"C:\tools\chromedriver.exe",
        os.path.expanduser(r"~\chromedriver\chromedriver.exe"),
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            try:
                service = Service(executable_path=path)
                driver = webdriver.Chrome(service=service, options=chrome_options)
                return driver
            except Exception as e:
                errors.append(f"path {path}: {str(e)[:50]}")
    
    # If all approaches failed, raise an error with all details
    raise RuntimeError(
        "Could not create Chrome WebDriver. Attempted methods:\n" +
        "\n".join(f"  - {e}" for e in errors) +
        "\n\nPossible solutions:\n" +
        "  1. Install Chrome browser if not installed\n" +
        "  2. Download ChromeDriver matching your Chrome version\n" +
        "  3. Add chromedriver to PATH or place in a common location\n" +
        "  4. Check network connectivity for webdriver_manager"
    )


@pytest.fixture(scope="function")
def driver(request):
    """
    Create and configure a Chrome WebDriver instance.
    
    The driver is created fresh for each test function to ensure isolation.
    Screenshots are captured on test failure.
    """
    headless = request.config.getoption("--headless")
    
    # Create the WebDriver
    driver = _create_chrome_driver(headless)
    
    # Configure implicit wait
    driver.implicitly_wait(10)
    
    yield driver
    
    # Capture screenshot on failure
    if request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False:
        _capture_screenshot(driver, request.node.name)
    
    # Cleanup
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test result for screenshot on failure."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def _capture_screenshot(driver, test_name: str):
    """Capture a screenshot on test failure."""
    screenshots_dir = Path(__file__).parent / "reports" / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{test_name}_{timestamp}.png"
    filepath = screenshots_dir / filename
    
    try:
        driver.save_screenshot(str(filepath))
        print(f"\nScreenshot saved: {filepath}")
    except Exception as e:
        print(f"\nFailed to capture screenshot: {e}")


@pytest.fixture(scope="function")
def app_page(driver, base_url):
    """
    Navigate to the application and return the driver.
    
    This fixture ensures the page is loaded before tests run.
    """
    driver.get(base_url)
    return driver


# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def unique_user_data():
    """Generate unique user data for each test."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return {
        "username": f"testuser_{timestamp}",
        "email": f"test_{timestamp}@example.com",
        "password": "TestPassword123!"
    }


@pytest.fixture(scope="function")
def unique_post_data():
    """Generate unique post data for each test."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return {
        "title": f"Test Post {timestamp}",
        "content": f"This is test content created at {timestamp}. Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    }
