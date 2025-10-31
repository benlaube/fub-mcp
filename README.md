# Follow Up Boss MCP Server (Python)

A Python implementation of the Model Context Protocol (MCP) server for interacting with Follow Up Boss CRM API. This server provides intelligent access to FUB data through a single, powerful tool and individual endpoint tools.

> ✅ **CRUD CAPABILITIES**: Full Create, Read, Update, Delete operations for People/Contacts and Custom Fields.

## Features

- 🎯 **One Powerful Tool**: `execute_custom_query` - fetch and process data from any FUB API endpoint
- 📊 **Flexible Processing**: Custom Python code for data aggregation and analysis
- 🔄 **Intelligent Pagination**: Automatically handles large datasets
- 📅 **Date Filtering**: Built-in support for date range queries
- 🚀 **Async Performance**: Built on async/await for optimal performance
- 🛡️ **Safe Execution**: Sandboxed code execution environment
- ✏️ **Full CRUD**: Create, Update, Delete operations for People/Contacts
- 🏷️ **Custom Fields**: Manage custom fields on contacts

## Installation

### Prerequisites

- Python 3.9 or higher
- Follow Up Boss API key

### Setup

1. **Clone or navigate to the repository**:
   ```bash
   cd fub-mcp
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API key**:
   ```bash
   cp .env.example .env
   # Edit .env and add your FUB_API_KEY
   ```

## Configuration

This MCP server works with **any AI client** that supports MCP! See [MULTI_CLIENT_SETUP.md](MULTI_CLIENT_SETUP.md) for detailed setup instructions for different clients.

### Quick Setup (Any Client)

The server includes a default API key, so you can start using it immediately. Just configure your AI client:

**Example Configuration** (works with Claude Desktop, Cline, Continue.dev, etc.):
```json
{
  "mcpServers": {
    "fub-mcp": {
      "command": "python",
      "args": ["-m", "fub_mcp.server"]
    }
  }
}
```

**Or override the API key**:
```json
{
  "mcpServers": {
    "fub-mcp": {
      "command": "python",
      "args": ["-m", "fub_mcp.server"],
      "env": {
        "FUB_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Client-Specific Setup

- **Claude Desktop**: See [MULTI_CLIENT_SETUP.md](MULTI_CLIENT_SETUP.md#1-claude-desktop)
- **Cline**: See [MULTI_CLIENT_SETUP.md](MULTI_CLIENT_SETUP.md#2-cline-vs-code-extension)
- **Continue.dev**: See [MULTI_CLIENT_SETUP.md](MULTI_CLIENT_SETUP.md#3-continuedev)
- **Other Clients**: See [MULTI_CLIENT_SETUP.md](MULTI_CLIENT_SETUP.md#4-generic-mcp-client)

## Usage

### Basic Query

The `execute_custom_query` tool allows you to fetch and process data from multiple FUB API endpoints.

**Example**: Get all people and their counts
```json
{
  "description": "Get total number of people",
  "endpoints": [
    {
      "endpoint": "/people",
      "params": {}
    }
  ]
}
```

### Query with Date Range

**Example**: Get all calls in June 2025
```json
{
  "description": "Get all calls in June 2025",
  "endpoints": [
    {
      "endpoint": "/calls",
      "dateField": "created"
    }
  ],
  "dateRange": {
    "start": "2025-06-01",
    "end": "2025-06-30"
  }
}
```

### Query with Custom Processing

**Example**: Team performance report
```json
{
  "description": "Team performance report for June 2025",
  "endpoints": [
    {
      "endpoint": "/people",
      "dateField": "created"
    },
    {
      "endpoint": "/calls",
      "dateField": "created"
    },
    {
      "endpoint": "/events",
      "dateField": "occurred"
    }
  ],
  "dateRange": {
    "start": "2025-06-01",
    "end": "2025-06-30"
  },
  "processing": """
# Group people by assigned user
people_by_user = utils.groupBy(data['people'], 'assignedUserId')

# Count calls by user
calls_by_user = utils.countBy(data['calls'], 'userId')

# Build report
result = {
    'summary': {
        'total_leads': len(data['people']),
        'total_calls': len(data['calls']),
        'total_events': len(data['events'])
    },
    'by_user': {
        user_id: {
            'leads': len(people_by_user.get(user_id, [])),
            'calls': calls_by_user.get(user_id, 0)
        }
        for user_id in set(list(people_by_user.keys()) + list(calls_by_user.keys()))
    }
}
"""
}
```

## Available Utilities

When writing processing code, you have access to the `utils` object with these methods:

- `utils.groupBy(data, key)` - Group data by a key
- `utils.countBy(data, key)` - Count occurrences by key
- `utils.sumBy(data, key)` - Sum values by key
- `utils.unique(data, key)` - Get unique items or values
- `utils.aggregate(data, group_key, agg_key, operation)` - Aggregate data (sum, avg, count, min, max)
- `utils.dateRange(start, end)` - Create a date range filter function

## Available Tools

The server provides **28 tools** for interacting with Follow Up Boss:

### CRUD Operations
- `create_person` - Create new contacts
- `update_person` - Update existing contacts  
- `delete_person` - Delete contacts (permanent)
- `get_person` - Get contact details
- `get_people` - List contacts
- `search_people` - Search contacts

### Custom Fields
- `get_custom_fields` - Get all custom fields
- `get_custom_field` - Get specific custom field

### Read Operations
- `get_calls`, `get_call` - Phone calls
- `get_events`, `get_event` - Activities
- `get_deals`, `get_deal` - Deals
- `get_tasks`, `get_task` - Tasks
- `get_users`, `get_user`, `get_me` - Users
- `get_notes`, `get_note` - Notes
- `get_appointments`, `get_appointment` - Appointments
- `get_pipelines`, `get_pipeline` - Pipelines
- `get_stages`, `get_stage` - Stages

### Advanced
- `execute_custom_query` - Custom reporting with Python processing

See [CRUD_GUIDE.md](CRUD_GUIDE.md) for detailed CRUD examples and [AVAILABLE_TOOLS.md](AVAILABLE_TOOLS.md) for the complete tool list.

## Response Format

The tool returns a JSON response with:

```json
{
  "success": true,
  "query": "Description of the query",
  "executedAt": "2025-01-31T12:00:00",
  "dateRange": {...},
  "performance": {
    "totalRecordsFetched": 1234,
    "processingTimeMs": 150,
    "totalTimeMs": 2000,
    "endpoints": [...]
  },
  "results": {...}
}
```

## Error Handling

The server handles errors gracefully:

- Invalid endpoints return error messages
- Processing code errors include helpful recommendations
- API errors are translated to readable messages
- Rate limiting is handled automatically

## Development

### Running Tests

```bash
pytest tests/
```

### Running the Server Directly

```bash
python -m fub_mcp.server
```

### Project Structure

```
fub-mcp/
├── src/
│   └── fub_mcp/
│       ├── __init__.py
│       ├── server.py          # Main MCP server
│       ├── fub_client.py      # FUB API client
│       ├── processors.py       # Data processing utilities
│       └── config.py          # Configuration
├── tests/
├── examples/
├── requirements.txt
├── setup.py
└── README.md
```

## Security

- **Read-only operations**: No data modification capabilities
- **API key protection**: Stored in environment variables
- **Sandboxed execution**: Processing code runs in restricted environment
- **Rate limiting**: Built-in delays to respect API limits

## Limitations

- Result size limit: 10 MB (configurable)
- Processing code is restricted to safe operations
- Read-only mode - no data modification

## Troubleshooting

### "FUB_API_KEY environment variable is required"

Make sure you've set the `FUB_API_KEY` in your `.env` file or environment variables.

### "Unknown tool: execute_custom_query"

Ensure you're using the correct tool name. The tool is named exactly `execute_custom_query`.

### Processing code errors

Check your Python syntax. Use the utility functions (`utils.groupBy`, etc.) for common operations.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Acknowledgments

- Inspired by the [JavaScript implementation](https://github.com/nsd97/fub-mcp)
- Built with the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- API documentation: [Follow Up Boss API](https://docs.followupboss.com/reference/getting-started)

---

**Version**: 0.1.0  
**Status**: Early Development

