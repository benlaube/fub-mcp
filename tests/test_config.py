"""Tests for configuration management."""

import os
import pytest
from fub_mcp.config import Config


def test_config_default_api_key():
    """Test that default API key is set."""
    assert Config.FUB_API_KEY == "fka_0E1RFmwuRHSgSd771KQY7ps2q4HgUUNV8H"


def test_config_validation():
    """Test configuration validation."""
    # Should pass with default key
    assert Config.validate() is True


def test_config_headers():
    """Test header generation."""
    headers = Config.get_headers()
    assert "Content-Type" in headers
    assert "X-System" in headers
    assert "X-System-Key" in headers
    assert headers["X-System"] == "FUB_MCP_Server_Python"


def test_config_can_override_with_env(monkeypatch):
    """Test that API key can be overridden with environment variable."""
    monkeypatch.setenv("FUB_API_KEY", "test-key-123")
    # Need to reload the module to pick up the change
    import importlib
    import fub_mcp.config
    importlib.reload(fub_mcp.config)
    assert fub_mcp.config.Config.FUB_API_KEY == "test-key-123"

