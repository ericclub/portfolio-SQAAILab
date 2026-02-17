"""Pytest fixtures and configuration for LLM RAG tests."""
import pytest
import requests
from openai import OpenAI
from config import Config


@pytest.fixture(scope="session")
def lm_studio_client():
    """Create OpenAI client configured for LM Studio."""
    return OpenAI(
        base_url=Config.LM_STUDIO_BASE_URL,
        api_key="not-needed"  # LM Studio doesn't require API key
    )


@pytest.fixture(scope="session")
def api_base_url():
    """Return the LM Studio API base URL."""
    return Config.LM_STUDIO_BASE_URL


@pytest.fixture(scope="function")
def session():
    """Create requests session with timeout."""
    s = requests.Session()
    s.timeout = Config.TEST_TIMEOUT
    return s


@pytest.fixture(scope="session")
def config():
    """Return configuration object."""
    return Config
