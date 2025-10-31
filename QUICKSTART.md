# Quick Start Guide

Get up and running with the FUB MCP Server in 5 minutes.

## Prerequisites

- Python 3.9+
- Follow Up Boss API key

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your API key**:
   ```bash
   export FUB_API_KEY="your-api-key-here"
   ```
   
   Or create a `.env` file:
   ```bash
   echo "FUB_API_KEY=your-api-key-here" > .env
   ```

## Test the Server

Run the server directly to test:

```bash
python -m fub_mcp.server
```

The server communicates via stdio, so you won't see much output. To test with Claude Desktop, configure it as shown in the main README.

## Example Query

Once configured in Claude Desktop, you can ask:

> "Show me all leads from June 2025 and how many calls each agent made"

The AI will automatically use the `execute_custom_query` tool to:
1. Fetch people created in June 2025
2. Fetch calls from June 2025
3. Process the data to show leads and calls per agent

## Common Queries

### Get Total Leads Count
```
"Get the total number of people in the system"
```

### Team Performance Report
```
"Show me team performance for June 2025 with leads and calls per agent"
```

### Lead Sources Analysis
```
"Analyze lead sources for the last 30 days"
```

### Activity Summary
```
"Show me all events and calls for the current month"
```

## Troubleshooting

### "FUB_API_KEY not found"
Make sure you've set the environment variable or created a `.env` file.

### "Module not found"
Install dependencies: `pip install -r requirements.txt`

### Server not responding
- Check that Python 3.9+ is being used
- Verify API key is correct
- Check Claude Desktop configuration

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [BUILD_PLAN.md](BUILD_PLAN.md) for architecture details
- See [examples/basic_usage.py](examples/basic_usage.py) for code examples

