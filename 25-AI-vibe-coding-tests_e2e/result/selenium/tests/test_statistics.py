"""
test_statistics.py - E2E Tests for Statistics Tab

Test Cases covered:
- TC-E2E-01: UI loads and displays statistics (smoke test)
- TC-E2E-02: Stats refresh updates displayed values

Story Reference: E2E-01 (Admin UI loads and shows live statistics)
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pages.statistics_page import StatisticsPage


@pytest.mark.smoke
@pytest.mark.e2e
@pytest.mark.statistics
class TestStatisticsDisplay:
    """Tests for statistics display functionality."""
    
    def test_ui_loads_and_shows_stats(self, driver, base_url):
        """
        TC-E2E-01: UI loads and displays statistics (Smoke Test)
        
        Story: E2E-01 - Admin UI loads and shows live statistics
        
        Given the backend server is running at http://localhost:5000
        And the Admin UI index.html is opened in a browser
        When the Statistics tab is active
        Then the UI requests GET /api/stats
        And it renders numeric values for Users, Total Posts, and Published Posts
        
        Acceptance Criteria:
        - Page loads without errors
        - Statistics tab is displayed by default
        - Three stat cards are visible (Users, Total Posts, Published Posts)
        - Each card displays a numeric value (not "Loading error")
        """
        # Navigate to the application
        driver.get(base_url)
        
        # Initialize page object
        stats_page = StatisticsPage(driver)
        
        # Verify statistics section is active (default tab)
        assert stats_page.is_stats_section_active(), \
            "Statistics section should be active by default"
        
        # Verify stats are displayed (not loading/error state)
        assert stats_page.stats_are_displayed(), \
            "Statistics should be displayed with three stat cards"
        
        # Verify no loading error
        assert not stats_page.has_loading_error(), \
            "Should not display loading error"
        
        # Get and verify stat values are valid numbers
        stats = stats_page.get_stat_values()
        
        assert isinstance(stats['users'], int), \
            f"Users count should be an integer, got: {stats['users']}"
        assert isinstance(stats['total_posts'], int), \
            f"Total posts count should be an integer, got: {stats['total_posts']}"
        assert isinstance(stats['published_posts'], int), \
            f"Published posts count should be an integer, got: {stats['published_posts']}"
        
        # Values should be non-negative
        assert stats['users'] >= 0, "Users count should be non-negative"
        assert stats['total_posts'] >= 0, "Total posts count should be non-negative"
        assert stats['published_posts'] >= 0, "Published posts count should be non-negative"
        
        # Published posts should not exceed total posts
        assert stats['published_posts'] <= stats['total_posts'], \
            f"Published posts ({stats['published_posts']}) should not exceed total posts ({stats['total_posts']})"
        
        print(f"\n✅ TC-E2E-01 PASSED: Statistics displayed correctly")
        print(f"   - Users: {stats['users']}")
        print(f"   - Total Posts: {stats['total_posts']}")
        print(f"   - Published Posts: {stats['published_posts']}")


@pytest.mark.e2e
@pytest.mark.statistics
class TestStatisticsRefresh:
    """Tests for statistics refresh functionality."""
    
    def test_refresh_updates_stats(self, driver, base_url):
        """
        TC-E2E-02: Stats refresh updates displayed values
        
        Story: E2E-01 - Admin UI loads and shows live statistics
        
        Given the Statistics tab is active
        When I click the Refresh button
        Then the UI re-requests GET /api/stats
        And the rendered values match the latest API response
        
        Note: This test verifies the refresh mechanism works.
        Since we can't control backend data in pure E2E tests,
        we verify that refresh completes successfully and stats remain valid.
        """
        # Navigate to the application
        driver.get(base_url)
        
        # Initialize page object
        stats_page = StatisticsPage(driver)
        
        # Get initial stats
        initial_stats = stats_page.get_stat_values()
        print(f"\n📊 Initial stats: {initial_stats}")
        
        # Click refresh button
        stats_page.click_refresh()
        
        # Verify stats are still displayed correctly after refresh
        assert stats_page.stats_are_displayed(), \
            "Statistics should still be displayed after refresh"
        
        assert not stats_page.has_loading_error(), \
            "Should not display loading error after refresh"
        
        # Get stats after refresh
        refreshed_stats = stats_page.get_stat_values()
        print(f"📊 Stats after refresh: {refreshed_stats}")
        
        # Verify stats are still valid numbers
        assert isinstance(refreshed_stats['users'], int), \
            "Users count should be an integer after refresh"
        assert isinstance(refreshed_stats['total_posts'], int), \
            "Total posts count should be an integer after refresh"
        assert isinstance(refreshed_stats['published_posts'], int), \
            "Published posts count should be an integer after refresh"
        
        # Values should still be valid
        assert refreshed_stats['users'] >= 0, \
            "Users count should be non-negative after refresh"
        assert refreshed_stats['total_posts'] >= 0, \
            "Total posts count should be non-negative after refresh"
        assert refreshed_stats['published_posts'] <= refreshed_stats['total_posts'], \
            "Published posts should not exceed total posts after refresh"
        
        print(f"✅ TC-E2E-02 PASSED: Refresh mechanism works correctly")
