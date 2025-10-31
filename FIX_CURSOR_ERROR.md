# Fix for Cursor MCP Server Error

## Problem

Cursor IDE is showing an error when trying to connect to the FUB MCP server (likely lines 52-59 reference in the error).

## Solution

The server has been fixed and configured properly. Here's what was done:

### 1. ✅ Installed Package in Development Mode

The package is now installed in the venv with `pip install -e .`, making the `fub_mcp` module directly importable.

### 2. ✅ Added Error Handling

The server now has proper error handling and will provide better error messages if something goes wrong.

### 3. ✅ Created Wrapper Script

Created `run_mcp_server.sh` as a backup option that ensures proper PYTHONPATH.

## Cursor Configuration

Use this configuration in Cursor's MCP settings:

```json
{
  "mcpServers": {
    "fub-mcp": {
      "command": "/Users/benlaube/fub-mcp/venv/bin/python",
      "args": ["-m", "fub_mcp.server"],
      "cwd": "/Users/benlaube/fub-mcp"
    }
  }
}
```

## Verification Steps

1. **Test server import**:
   ```bash
   cd /Users/benlaube/fub-mcp
   source venv/bin/activate
   python -c "from fub_mcp.server import server; print('✅ OK')"
   ```

2. **Test server startup**:
   ```bash
   python -m fub_mcp.server &
   # Should start without errors
   kill %1
   ```

3. **Test API connection**:
   ```bash
   python test_api.py
   # Should show: ✅ API connection successful!
   ```

## If Error Persists

### Check 1: Verify Installation
```bash
cd /Users/benlaube/fub-mcp
source venv/bin/activate
pip install -e .
python -c "import fub_mcp; print(fub_mcp.__file__)"
```

### Check 2: Verify Python Path
```bash
which python  # Should show: /Users/benlaube/fub-mcp/venv/bin/python
```

### Check 3: Test Server Manually
```bash
cd /Users/benlaube/fub-mcp
source venv/bin/activate
python -m fub_mcp.server
```
(Server will wait for connections - press Ctrl+C to stop)

### Alternative: Use Wrapper Script

If direct Python command doesn't work, use the wrapper:

```json
{
  "mcpServers": {
    "fub-mcp": {
      "command": "/Users/benlaube/fub-mcp/run_mcp_server.sh",
      "cwd": "/Users/benlaube/fub-mcp"
    }
  }
}
```

## Common Errors and Fixes

### "Module not found: fub_mcp"
**Fix**: Run `pip install -e .` in the venv

### "Server failed to start"
**Fix**: Check that venv is activated and dependencies are installed

### "Configuration error: FUB_API_KEY required"
**Fix**: The default key should work, but you can add it to env in config

## Status

✅ Server is properly configured  
✅ Package installed in development mode  
✅ Error handling improved  
✅ Ready for Cursor IDE

---

**Configuration file**: `cursor_mcp_config.json` (reference only - use Cursor settings UI)

