"""Tests for MCP server."""

import pytest
from unittest.mock import AsyncMock, patch
from fub_mcp.server import list_tools, call_tool, execute_custom_query


@pytest.mark.asyncio
async def test_list_tools():
    """Test tool listing."""
    tools = await list_tools()
    assert len(tools) >= 1  # Should have at least execute_custom_query
    assert any(t.name == "execute_custom_query" for t in tools)
    # Check for individual tools
    assert any(t.name == "get_people" for t in tools)
    assert any(t.name == "get_calls" for t in tools)
    assert any(t.name == "get_user" for t in tools)


@pytest.mark.asyncio
async def test_call_tool_execute_custom_query():
    """Test calling execute_custom_query tool."""
    args = {
        "description": "Test query",
        "endpoints": [
            {"endpoint": "/people", "params": {}}
        ]
    }
    
    with patch("fub_mcp.server.FUBClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.fetch_all_pages = AsyncMock(return_value=[{"id": 1}])
        mock_client_class.return_value = mock_client
        
        result = await call_tool("execute_custom_query", args)
        assert len(result) == 1
        assert result[0].type == "text"
        
        # Parse JSON response
        import json
        response_data = json.loads(result[0].text)
        assert response_data["success"] is True
        assert response_data["query"] == "Test query"


@pytest.mark.asyncio
async def test_call_tool_unknown():
    """Test calling unknown tool."""
    result = await call_tool("unknown_tool", {})
    assert len(result) == 1
    assert result[0].type == "text"
    # Should return error response, not raise exception
    import json
    response_data = json.loads(result[0].text)
    assert response_data.get("error") is True
    assert "unknown_tool" in response_data.get("message", "").lower() or "unknown" in response_data.get("message", "").lower()


@pytest.mark.asyncio
async def test_execute_custom_query_with_processing():
    """Test execute_custom_query with custom processing."""
    args = {
        "description": "Test with processing",
        "endpoints": [
            {"endpoint": "/people", "params": {}}
        ],
        "processing": "result = {'total': len(data['people'])}"
    }
    
    with patch("fub_mcp.server.FUBClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.fetch_all_pages = AsyncMock(return_value=[{"id": 1}, {"id": 2}])
        mock_client_class.return_value = mock_client
        
        result = await execute_custom_query(args)
        assert len(result) == 1
        
        import json
        response_data = json.loads(result[0].text)
        assert response_data["success"] is True
        assert "results" in response_data


@pytest.mark.asyncio
async def test_call_tool_get_people():
    """Test calling get_people individual tool."""
    with patch("fub_mcp.server.FUBClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value={"people": [{"id": 1, "name": "Test"}]})
        mock_client_class.return_value = mock_client
        
        result = await call_tool("get_people", {"limit": 10})
        assert len(result) == 1
        assert result[0].type == "text"
        
        import json
        response_data = json.loads(result[0].text)
        assert "people" in response_data


@pytest.mark.asyncio
async def test_call_tool_get_person():
    """Test calling get_person individual tool."""
    with patch("fub_mcp.server.FUBClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get_person = AsyncMock(return_value={"id": "123", "name": "Test Person"})
        mock_client_class.return_value = mock_client
        
        result = await call_tool("get_person", {"personId": "123"})
        assert len(result) == 1
        assert result[0].type == "text"
        
        import json
        response_data = json.loads(result[0].text)
        assert response_data["id"] == "123"

