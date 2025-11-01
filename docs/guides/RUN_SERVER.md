# Running the FUB MCP Server

## Quick Start

### Option 1: Use the Run Script (Easiest)

```bash
./run_server.sh
```

This script will:
- Create venv if it doesn't exist
- Install dependencies automatically
- Activate venv and run the server

### Option 2: Manual Setup

```bash
# Create virtual environment (first time only)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Run the server
python -m fub_mcp.server
```

## Server Behavior

The MCP server:
- Runs continuously, waiting for MCP client connections
- Communicates via stdin/stdout (stdio transport)
- Logs to stderr
- Stops when the client disconnects or you press Ctrl+C

## For AI Client Configuration

When configuring your AI client (Claude Desktop, Cline, etc.), use:

```json
{
  "mcpServers": {
    "fub-mcp": {
      "command": "venv/bin/python",
      "args": ["-m", "fub_mcp.server"],
      "cwd": "/Users/benlaube/fub-mcp"
    }
  }
}
```

**Or use absolute paths:**
```json
{
  "mcpServers": {
    "fub-mcp": {
      "command": "/Users/benlaube/fub-mcp/venv/bin/python",
      "args": ["-m", "fub_mcp.server"]
    }
  }
}
```

## Testing the Server

### Test API Connection
```bash
source venv/bin/activate
python test_api.py
```

### Run All Tests
```bash
source venv/bin/activate
pytest tests/ -v
```

## Troubleshooting

### "No module named 'fub_mcp'"
Make sure you're:
1. In the project directory
2. Virtual environment is activated
3. Dependencies are installed: `pip install -r requirements.txt`

### "Command not found: venv/bin/python"
Use absolute path or ensure you're in the project directory.

### Server Won't Start
Check:
1. Python version: `python3 --version` (needs 3.9+)
2. Dependencies installed: `pip list | grep mcp`
3. API key configured (has default)

---

**Current Setup**: Virtual environment created and ready ✅

