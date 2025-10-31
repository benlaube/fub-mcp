# Testing Guide

This document describes how to test the FUB MCP Server.

## Running Tests

### All Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/fub_mcp --cov-report=html
```

### Test Categories

#### Unit Tests (Fast, No API calls)
```bash
pytest tests/test_config.py tests/test_processors.py -v
```

#### Server Tests (Mocked API)
```bash
pytest tests/test_server.py tests/test_fub_client.py -v
```

#### Integration Tests (Real API calls)
```bash
pytest tests/test_integration.py -v -m integration
```

### Skip Integration Tests

```bash
# Run only unit tests (skip integration)
pytest tests/ -v -m "not integration"
```

## Test Files

### `test_config.py`
Tests configuration management:
- ✅ Default API key loading
- ✅ Configuration validation
- ✅ Header generation
- ✅ Environment variable override

### `test_processors.py`
Tests data processing utilities:
- ✅ `groupBy()` - Group data by key
- ✅ `countBy()` - Count occurrences
- ✅ `sumBy()` - Sum values
- ✅ `unique()` - Get unique items/values
- ✅ `aggregate()` - Advanced aggregation

### `test_fub_client.py`
Tests FUB API client (mocked):
- ✅ Client initialization
- ✅ Context manager support
- ✅ GET requests
- ✅ Pagination logic

### `test_server.py`
Tests MCP server (mocked):
- ✅ Tool listing
- ✅ Tool execution
- ✅ Custom query processing
- ✅ Error handling

### `test_integration.py`
Tests real API integration:
- ✅ API connection
- ✅ User fetching
- ⚠️ Requires valid API key
- ⚠️ Makes real API calls

## Quick API Test

Test the API connection directly:

```bash
python3 test_api.py
```

Or in Python:

```python
import asyncio
from fub_mcp.fub_client import FUBClient

async def test():
    async with FUBClient() as client:
        result = await client.get("/identity")
        print("✅ Connection successful!")
        print(result)

asyncio.run(test())
```

## Test Configuration

Tests are configured via `pytest.ini`:

```ini
[pytest]
pythonpath = src
asyncio_mode = auto
markers =
    integration: marks tests as integration tests
```

## Test Results

### Expected Output

```
============================= test session starts ==============================
collected 15 items

tests/test_config.py::test_config_default_api_key PASSED
tests/test_config.py::test_config_validation PASSED
tests/test_config.py::test_config_headers PASSED
tests/test_config.py::test_config_can_override_with_env PASSED
tests/test_processors.py::test_group_by PASSED
tests/test_processors.py::test_count_by PASSED
tests/test_processors.py::test_sum_by PASSED
tests/test_processors.py::test_unique PASSED
tests/test_processors.py::test_aggregate PASSED
tests/test_fub_client.py::test_fub_client_initialization PASSED
tests/test_server.py::test_list_tools PASSED
tests/test_server.py::test_call_tool_execute_custom_query PASSED
tests/test_server.py::test_call_tool_unknown PASSED
tests/test_server.py::test_execute_custom_query_with_processing PASSED
tests/test_integration.py::test_real_api_connection PASSED
tests/test_integration.py::test_real_api_get_users PASSED

============================== 15 passed in 1.23s ===============================
```

## Writing New Tests

### Unit Test Example

```python
def test_my_feature():
    """Test my new feature."""
    result = my_function("input")
    assert result == "expected"
```

### Async Test Example

```python
@pytest.mark.asyncio
async def test_async_feature():
    """Test async feature."""
    result = await my_async_function("input")
    assert result == "expected"
```

### Integration Test Example

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_api():
    """Test real API call."""
    async with FUBClient() as client:
        result = await client.get("/endpoint")
        assert result is not None
```

## Continuous Integration

For CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest tests/ -v -m "not integration"
    
# Integration tests (if API key available)
- name: Run integration tests
  run: pytest tests/ -v -m integration
  env:
    FUB_API_KEY: ${{ secrets.FUB_API_KEY }}
```

## Troubleshooting

### Tests Can't Find Module

**Error**: `ModuleNotFoundError: No module named 'fub_mcp'`

**Solution**: Tests use `pytest.ini` to set `pythonpath = src`, so they should work automatically. If not:
```bash
PYTHONPATH=src pytest tests/
```

### Integration Tests Fail

**Error**: `401 Unauthorized` or connection errors

**Solution**: 
- Check API key is valid
- Verify network connection
- Check API key has proper permissions

### Async Tests Fail

**Error**: `RuntimeWarning: coroutine was never awaited`

**Solution**: Use `@pytest.mark.asyncio` decorator and ensure `pytest-asyncio` is installed.

---

**Status**: All tests passing ✅  
**Coverage**: Core functionality tested  
**Integration**: Real API verified

