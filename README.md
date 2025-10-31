# Follow Up Boss MCP Server

A powerful Model Context Protocol (MCP) server for seamless integration with the **Follow Up Boss** real estate CRM API. This Python-based MCP server enables AI assistants to intelligently interact with your **Follow Up Boss** data, providing comprehensive access to contacts, leads, deals, and more.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![Follow Up Boss](https://img.shields.io/badge/Follow%20Up%20Boss-API%20v1-orange.svg)](https://followupboss.com)

> 🚀 **Production Ready**: Full CRUD operations, intelligent caching, duplicate detection, and automatic pagination for **Follow Up Boss** CRM data.

## What is Follow Up Boss?

**Follow Up Boss** is a leading real estate CRM platform that helps agents and teams manage their leads, contacts, and transactions. This MCP server provides programmatic access to your **Follow Up Boss** account, allowing AI assistants to query, analyze, and manage your CRM data efficiently.

## Key Features

### 🎯 Complete Follow Up Boss Integration
- **32 MCP Tools** for comprehensive **Follow Up Boss** API access
- **Full CRUD Operations**: Create, Read, Update, Delete contacts and custom fields
- **Smart Querying**: Custom queries with Python-based data processing
- **Duplicate Detection**: FUB-compliant duplicate checking for **Follow Up Boss** contacts
- **Intelligent Caching**: 4.6x faster repeated queries with automatic cache invalidation
- **Automatic Pagination**: Seamlessly handle large **Follow Up Boss** datasets (1,000+ records)
- **Rate Limiting**: Built-in protection against API throttling

### 📊 Data Management
- **Contacts/People**: Full management of **Follow Up Boss** contacts
- **Custom Fields**: Create and manage custom fields on **Follow Up Boss** contacts
- **Calls & Events**: Access call logs and activity events from **Follow Up Boss**
- **Deals & Tasks**: Track deals and tasks within **Follow Up Boss**
- **Pipelines & Stages**: Work with **Follow Up Boss** sales pipelines
- **Users & Teams**: Manage **Follow Up Boss** team members

### 🔧 Advanced Capabilities
- **Custom Processing**: Execute Python code for data aggregation and analysis
- **Date Filtering**: Built-in support for date range queries
- **Async Performance**: High-performance async/await architecture
- **Safe Execution**: Sandboxed code execution environment
- **Multi-Client Support**: Works with Claude Desktop, Cline, Continue.dev, and any MCP-compatible client

## Installation

### Prerequisites

- Python 3.9 or higher
- A **Follow Up Boss** account with API access
- Your **Follow Up Boss** API key ([Get it here](https://docs.followupboss.com/reference/getting-started))

### Quick Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/benlaube/fub-mcp.git
   cd fub-mcp
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your Follow Up Boss API key**:
   ```bash
   cp env.example .env
   # Edit .env and add your FUB_API_KEY from Follow Up Boss
   ```

## Configuration

This MCP server works with **any AI client** that supports the Model Context Protocol. Configure it once and use it with multiple AI assistants.

### For Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "follow-up-boss": {
      "command": "python",
      "args": ["-m", "fub_mcp.server"],
      "cwd": "/path/to/fub-mcp",
      "env": {
        "PYTHONPATH": "/path/to/fub-mcp/src",
        "FUB_API_KEY": "your-follow-up-boss-api-key"
      }
    }
  }
}
```

### For Other MCP Clients

See [MULTI_CLIENT_SETUP.md](MULTI_CLIENT_SETUP.md) for detailed setup instructions for:
- **Cline** (VS Code Extension)
- **Continue.dev**
- **Other MCP-compatible clients**

## Usage Examples

### Query Follow Up Boss Contacts

```json
{
  "tool": "get_people",
  "arguments": {
    "limit": 100,
    "sort": "-created"
  }
}
```

### Create a New Contact in Follow Up Boss

```json
{
  "tool": "create_person",
  "arguments": {
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-123-4567",
    "source": "Website"
  }
}
```

### Check for Duplicate Contacts

```json
{
  "tool": "check_duplicates",
  "arguments": {
    "email": "john.doe@example.com",
    "phone": "+1-555-123-4567",
    "firstName": "John",
    "lastName": "Doe"
  }
}
```

### Custom Follow Up Boss Query with Processing

```json
{
  "tool": "execute_custom_query",
  "arguments": {
    "description": "Team performance report",
    "endpoints": [
      {"endpoint": "/people", "dateField": "created"},
      {"endpoint": "/calls", "dateField": "created"}
    ],
    "dateRange": {
      "start": "2025-01-01",
      "end": "2025-01-31"
    },
    "processing": "result = {'total_leads': len(data['people']), 'total_calls': len(data['calls'])}"
  }
}
```

## Available Tools (32 Total)

### Follow Up Boss Contact Management
- `get_people` - List contacts from **Follow Up Boss**
- `get_person` - Get specific contact details
- `create_person` - Create new **Follow Up Boss** contact
- `update_person` - Update existing contact
- `delete_person` - Delete contact
- `search_people` - Search **Follow Up Boss** contacts
- `check_duplicates` - Find duplicate contacts

### Follow Up Boss Custom Fields
- `get_custom_fields` - List all custom fields
- `get_custom_field` - Get specific custom field
- `create_custom_field` - Create new custom field
- `update_custom_field` - Update custom field
- `delete_custom_field` - Delete custom field

### Follow Up Boss Activity Data
- `get_calls`, `get_call` - Phone call records
- `get_events`, `get_event` - Activity events
- `get_notes`, `get_note` - Contact notes
- `get_appointments`, `get_appointment` - Scheduled appointments

### Follow Up Boss Sales Data
- `get_deals`, `get_deal` - Deal tracking
- `get_tasks`, `get_task` - Task management
- `get_pipelines`, `get_pipeline` - Sales pipelines
- `get_stages`, `get_stage` - Pipeline stages

### Follow Up Boss User Management
- `get_users`, `get_user` - Team members
- `get_me` - Current user info

### Advanced Querying
- `execute_custom_query` - Custom queries with Python processing

See [AVAILABLE_TOOLS.md](AVAILABLE_TOOLS.md) for complete documentation and [CRUD_GUIDE.md](CRUD_GUIDE.md) for detailed CRUD examples.

## Performance & Efficiency

### Intelligent Caching
- **4.6x faster** repeated queries
- Automatic cache invalidation on data changes
- Configurable cache size (default: 1,000 entries)

### Efficient Memory Usage
- **100 contacts**: ~169 KB
- **1,000 contacts**: ~1.65 MB
- Minimal memory footprint for large datasets

### Smart Pagination
- Automatically handles **Follow Up Boss** API limit (100 records per request)
- Seamlessly fetches 1,000+ records with proper rate limiting
- No timeouts or throttling issues

## Follow Up Boss API Integration

This server implements the complete **Follow Up Boss** API v1 specification:
- Full REST API support
- Automatic rate limiting and retry logic
- Comprehensive error handling
- Secure authentication via API keys

For more information about the **Follow Up Boss** API, visit: [Follow Up Boss API Documentation](https://docs.followupboss.com/reference/getting-started)

## Testing

The server includes comprehensive tests covering all **Follow Up Boss** integration points:

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test category
pytest tests/test_crud.py
```

**Test Results**: 26/26 tests passing ✅

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[MULTI_CLIENT_SETUP.md](MULTI_CLIENT_SETUP.md)** - Setup for different AI clients
- **[CRUD_GUIDE.md](CRUD_GUIDE.md)** - Complete CRUD operations guide
- **[DUPLICATE_CHECK_GUIDE.md](DUPLICATE_CHECK_GUIDE.md)** - Duplicate detection guide
- **[CACHING_STRATEGY.md](CACHING_STRATEGY.md)** - Caching implementation details
- **[AVAILABLE_TOOLS.md](AVAILABLE_TOOLS.md)** - Complete tool reference
- **[TESTING.md](TESTING.md)** - Testing guide

## Security & Best Practices

### API Key Security
- ✅ API keys stored in environment variables only
- ✅ Never commit API keys to version control
- ✅ Secure authentication with **Follow Up Boss** API

### Data Protection
- ✅ Sandboxed code execution for custom queries
- ✅ Input validation on all operations
- ✅ Rate limiting to protect **Follow Up Boss** API
- ✅ Comprehensive error handling

## Contributing

Contributions to improve **Follow Up Boss** MCP server are welcome! Please feel free to submit issues or pull requests.

## Support

For issues related to:
- **This MCP Server**: [Open an issue](https://github.com/benlaube/fub-mcp/issues)
- **Follow Up Boss API**: [FUB Support](https://support.followupboss.com/)
- **Model Context Protocol**: [MCP Documentation](https://modelcontextprotocol.io/)

## License

MIT License - See [LICENSE](LICENSE) file for details

## Acknowledgments

- Built for **Follow Up Boss** CRM platform
- Powered by [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- Inspired by [JavaScript implementation](https://github.com/nsd97/fub-mcp)
- **Follow Up Boss** API documentation: [docs.followupboss.com](https://docs.followupboss.com/)

---

**Made with ❤️ for the Follow Up Boss community**

*Follow Up Boss® is a registered trademark of Follow Up Boss, LLC. This project is not officially affiliated with or endorsed by Follow Up Boss.*
