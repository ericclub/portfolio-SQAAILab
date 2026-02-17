"""
Unit Tests for Statistics Aggregation
Covers: TC-STS-01 (Unit aspect)

These tests verify the statistics response structure.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'context', 'app', 'backend'))


@pytest.mark.unit
class TestStatsResponseStructure:
    """Unit tests for statistics response structure."""

    def test_stats_response_contains_total_users(self, client):
        """TC-STS-01-U1: Stats response should contain 'total_users' key."""
        response = client.get('/api/stats')
        data = response.get_json()
        
        assert 'total_users' in data
        assert isinstance(data['total_users'], int)

    def test_stats_response_contains_total_posts(self, client):
        """TC-STS-01-U2: Stats response should contain 'total_posts' key."""
        response = client.get('/api/stats')
        data = response.get_json()
        
        assert 'total_posts' in data
        assert isinstance(data['total_posts'], int)

    def test_stats_response_contains_published_posts(self, client):
        """TC-STS-01-U3: Stats response should contain 'published_posts' key."""
        response = client.get('/api/stats')
        data = response.get_json()
        
        assert 'published_posts' in data
        assert isinstance(data['published_posts'], int)

    def test_stats_response_shape(self, client):
        """TC-STS-01-U4: Stats response should have exactly the expected keys."""
        response = client.get('/api/stats')
        data = response.get_json()
        
        expected_keys = {'total_users', 'total_posts', 'published_posts'}
        actual_keys = set(data.keys())
        
        assert actual_keys == expected_keys, f"Expected keys {expected_keys}, got {actual_keys}"

    def test_stats_values_are_non_negative(self, client):
        """TC-STS-01-U5: All stats values should be non-negative."""
        response = client.get('/api/stats')
        data = response.get_json()
        
        assert data['total_users'] >= 0
        assert data['total_posts'] >= 0
        assert data['published_posts'] >= 0
