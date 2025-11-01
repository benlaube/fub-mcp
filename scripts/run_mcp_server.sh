#!/bin/bash
# Wrapper script to run MCP server with correct PYTHONPATH for Cursor

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Set PYTHONPATH to include src directory
export PYTHONPATH="$PWD/src:$PYTHONPATH"

# Run the server
exec python -m fub_mcp.server

