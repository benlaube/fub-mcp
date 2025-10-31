"""Configuration management for FUB MCP Server."""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration settings for the FUB MCP Server."""
    
    # API key must be provided via environment variable
    FUB_API_KEY: str = os.getenv("FUB_API_KEY", "")
    FUB_API_BASE: str = "https://api.followupboss.com/v1"
    FUB_API_SOURCE: str = "FUB_MCP_Server_Python"
    
    # Rate limiting
    RATE_LIMIT_DELAY_MS: int = 50  # Delay between API calls
    
    # Query limits
    MAX_PAGE_SIZE: int = 100
    MAX_RESULT_SIZE_MB: int = 10  # Maximum result size in MB
    
    # Processing
    ENABLE_CUSTOM_PROCESSING: bool = True
    RESTRICTED_PROCESSING: bool = True  # Use RestrictedPython for safety
    
    # Caching
    ENABLE_CACHING: bool = True  # Enable response caching
    CACHE_MAX_SIZE: int = 1000  # Maximum number of cache entries
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.FUB_API_KEY:
            raise ValueError(
                "FUB_API_KEY environment variable is required. "
                "Set it in .env file or environment variables."
            )
        return True
    
    @classmethod
    def get_headers(cls) -> dict:
        """Get default headers for API requests."""
        return {
            "Content-Type": "application/json",
            "X-System": cls.FUB_API_SOURCE,
            "X-System-Key": cls.FUB_API_KEY,
        }

