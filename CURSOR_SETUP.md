# Cursor IDE MCP Server Setup

## Configuration

Cursor IDE uses MCP servers configured through its settings. The package is installed in development mode, so it can be imported directly.

### Option 1: Cursor Settings (Recommended)

1. Open Cursor Settings (Cmd+, on Mac)
2. Search for "MCP" or navigate to MCP Settings
3. Add the following configuration:

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

**Note**: The package is installed in the venv with `pip install -e .`, so the module is importable.

### Option 2: Configuration File

If Cursor uses a config file, create or update:

**Location**: `~/.cursor/mcp.json` or `.cursor/mcp.json` in project root

```json
{
  "mcpServers": {
    "fub-mcp": {
      "command": "/Users/benlaube/fub-mcp/venv/bin/python",
      "args": ["-m", "fub_mcp.server"],
      "cwd": "/path/to/fub-mcp",
      "env": {
        "FUB_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Troubleshooting

### Error: "Cannot find module fub_mcp"

**Solution**: Ensure you're using the absolute path to the venv Python:
```json
{
  "command": "/Users/benlaube/fub-mcp/venv/bin/python",
  "args": ["-m", "fub_mcp.server"],
  "cwd": "/Users/benlaube/fub-mcp"
}
```

### Error: "Server failed to start"

**Solution**: 
1. Test the server manually:
   ```bash
   cd /Users/benlaube/fub-mcp
   source venv/bin/activate
   python -m fub_mcp.server
   ```
2. Check that all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

### Error: "Configuration error: FUB_API_KEY required"

**Solution**: The default API key should work, but if not, add it to env:
```json
{
  "env": {
    "FUB_API_KEY": "your_api_key_here"
  }
}
```

## Verification

To verify the server works:

```bash
cd /Users/benlaube/fub-mcp
source venv/bin/activate
python test_api.py
```

If this succeeds, the server is working correctly.

## Using the Server in Cursor

Once configured, you can use the MCP server in Cursor by asking questions like:

- "Get the most recent contact from FUB"
- "Show me all leads from June 2025"
- "What's the team performance this month?"

The AI will automatically use the `execute_custom_query` tool to fetch and process data.

