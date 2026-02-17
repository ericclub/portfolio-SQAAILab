"""Test configuration for LLM RAG automated tests."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration settings for LLM RAG tests."""
    
    # LM Studio settings
    LM_STUDIO_HOST = os.getenv("LM_STUDIO_HOST", "192.168.2.100")
    LM_STUDIO_PORT = int(os.getenv("LM_STUDIO_PORT", "1234"))
    LM_STUDIO_BASE_URL = os.getenv(
        "LM_STUDIO_BASE_URL",
        f"http://{LM_STUDIO_HOST}:{LM_STUDIO_PORT}/v1"
    )
    
    # Test settings
    TEST_TIMEOUT = int(os.getenv("TEST_TIMEOUT", "60"))
    EXPECTED_MODEL_NAME = os.getenv("EXPECTED_MODEL_NAME", "mistral")
    
    # Performance thresholds
    MAX_RESPONSE_TIME_SECONDS = int(os.getenv("MAX_RESPONSE_TIME_SECONDS", "30"))
    MIN_TOKENS_PER_SECOND = int(os.getenv("MIN_TOKENS_PER_SECOND", "5"))
