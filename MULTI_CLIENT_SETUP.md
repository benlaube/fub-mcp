# Multi-Client Setup Guide

This MCP server works with **any AI client** that supports the Model Context Protocol (MCP). The server uses standard stdio transport, which is compatible with all MCP clients.

## Supported AI Clients

✅ **Claude Desktop** (Anthropic)  
✅ **Cline** (VS Code extension)  
✅ **Continue.dev** (VS Code extension)  
✅ **MCP Inspector** (Debugging tool)  
✅ **Any MCP-compatible client**

## Why This Works Everywhere

The server uses **stdio transport**, which is the standard MCP communication method. This means:

- No special client-specific code needed
- Works with any tool that can spawn processes and communicate via stdin/stdout
- Standard JSON-RPC protocol over stdio
- Compatible with the official MCP specification

## Configuration by Client

### 1. Claude Desktop

**Configuration File Location:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Configuration:**
```json
{
  "mcpServers": {
    "fub-mcp": {
      "command": "python",
      "args": ["-m", "fub_mcp.server"],
      "env": {
        "FUB_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Or if installed as package:**
```json
{
  "mcpServers": {
    "fub-mcp": {
      "command": "fub-mcp"
    }
  }
}
```

### 2. Cline (VS Code Extension)

**Configuration File**: `.cline/mcp.json` in your workspace root

```json
{
  "mcpServers": {
    "fub-mcp": {
      "command": "python",
      "args": ["-m", "fub_mcp.server"],
      "env": {
        "FUB_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### 3. Continue.dev

**Configuration File**: `.continue/config.json` in your workspace root

```json
{
  "mcpServers": {
    "fub-mcp": {
      "command": "python",
      "args": ["-m", "fub_mcp.server"],
      "env": {
        "FUB_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### 4. Generic MCP Client

For any other MCP client, configure it to:

1. **Command**: `python` (or `python3`)
2. **Arguments**: `["-m", "fub_mcp.server"]`
3. **Environment Variables**: 
   - `FUB_API_KEY=your_api_key_here`

**Or use environment file:**
- Create `.env` file with `FUB_API_KEY=your_api_key_here`

### 5. Programmatic Usage (Python)

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "fub_mcp.server"],
        env={"FUB_API_KEY": "fka_0E1RFmwuRHSgSd771KQY7ps2q4HgUUNV8H"}
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")
            
            # Call tool
            result = await session.call_tool(
                "execute_custom_query",
                {
                    "description": "Get total people count",
                    "endpoints": [{"endpoint": "/people"}]
                }
            )
            print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## API Key Configuration

The server includes a default API key for convenience, but you can override it:

### Option 1: Environment Variable
```bash
export FUB_API_KEY="your-api-key-here"
```

### Option 2: .env File
```bash
echo "FUB_API_KEY=your-api-key-here" > .env
```

### Option 3: Client Configuration
Set in the client's MCP server configuration (shown above).

## Verification

### Test the Server Directly

```bash
# Test that the server starts
python -m fub_mcp.server

# Should output initialization messages to stderr
```

### Test with MCP Inspector

```bash
# Install MCP Inspector (if available)
npm install -g @modelcontextprotocol/inspector

# Run inspector
mcp-inspector python -m fub_mcp.server
```

### Test API Connection

```python
# Quick test script
import asyncio
from fub_mcp.fub_client import FUBClient

async def test():
    async with FUBClient() as client:
        result = await client.get("/identity")
        print("✅ API connection successful!")
        print(result)

asyncio.run(test())
```

## Troubleshooting

### Server Won't Start

**Issue**: "FUB_API_KEY environment variable is required"

**Solution**: 
- Set `FUB_API_KEY` in environment or `.env` file
- Or configure in client's MCP server settings
- The default key should work automatically

### Client Can't Connect

**Issue**: Client shows "connection failed" or "server not responding"

**Solutions**:
1. Verify Python path is correct (`python` vs `python3`)
2. Check that dependencies are installed: `pip install -r requirements.txt`
3. Test server manually: `python -m fub_mcp.server`
4. Check client logs for error messages

### Import Errors

**Issue**: "Module not found: fub_mcp"

**Solutions**:
1. Install in development mode: `pip install -e .`
2. Or ensure you're running from project root with `PYTHONPATH=src`
3. Or use full module path: `python -m src.fub_mcp.server`

### API Errors

**Issue**: "401 Unauthorized" or API errors

**Solutions**:
1. Verify API key is correct
2. Check API key permissions in Follow Up Boss
3. Test API key directly: `curl -u "API_KEY:" https://api.followupboss.com/v1/identity`

## Architecture Notes

### Why stdio Works Everywhere

The MCP protocol specifies stdio as the standard transport:

1. **Universal**: Every OS supports stdin/stdout
2. **Simple**: No network configuration needed
3. **Secure**: Communication stays local
4. **Standard**: Part of the official MCP spec

### Server Lifecycle

1. Client spawns process: `python -m fub_mcp.server`
2. Server reads from stdin (JSON-RPC requests)
3. Server writes to stdout (JSON-RPC responses)
4. Server logs to stderr (for debugging)
5. Process exits when client disconnects

### Client Requirements

Any MCP client must:
- Be able to spawn processes
- Read from process stdout
- Write to process stdin
- Handle JSON-RPC protocol
- Support stdio transport

All major MCP clients meet these requirements.

## Next Steps

1. **Choose your AI client** from the list above
2. **Configure the server** using the appropriate config file
3. **Restart your AI client** to load the MCP server
4. **Start using it!** Ask questions like:
   - "Show me all leads from June 2025"
   - "What's the team performance for this month?"
   - "Analyze lead sources"

---

**Default API Key**: Configured automatically  
**Status**: Ready for use with any MCP client  
**Transport**: stdio (universal compatibility)

