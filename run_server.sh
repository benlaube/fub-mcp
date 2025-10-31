#!/bin/bash
# Script to run the FUB MCP Server in virtual environment

cd "$(dirname "$0")"

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies if needed
if ! python -c "import mcp" 2>/dev/null; then
    echo "Installing requirements..."
    pip install -q -r requirements.txt
fi

# Run the server
echo "Starting FUB MCP Server..."
echo "Press Ctrl+C to stop"
python -m fub_mcp.server

