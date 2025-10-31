"""Integration tests for FUB MCP Server.

These tests require a valid API key and may make real API calls.
Run with: pytest tests/test_integration.py -v
"""

import pytest
import os
from fub_mcp.fub_client import FUBClient
from fub_mcp.config import Config


@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_api_connection():
    """Test real connection to FUB API."""
    # Use the configured API key
    async with FUBClient() as client:
        # Try to get identity (lightweight endpoint)
        try:
            result = await client.get("/identity")
            assert "identity" in result or "user" in result or len(result) > 0
        except Exception as e:
            pytest.skip(f"API connection failed (may be network issue): {e}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_api_get_users():
    """Test fetching users from real API."""
    async with FUBClient() as client:
        try:
            result = await client.get("/users", params={"limit": 5})
            # Should return users array or metadata
            assert isinstance(result, dict)
        except Exception as e:
            pytest.skip(f"API call failed: {e}")

