# Follow Up Boss MCP Server - Build Plan

## Executive Summary

This document outlines a comprehensive plan to build a Python-based MCP (Model Context Protocol) server framework for interacting with Follow Up Boss (FUB)'s API, leveraging existing resources and frameworks.

## Discovery Findings

### Existing Resources Found

#### 1. **Existing JavaScript Implementation** ✅
- **Repository**: [nsd97/fub-mcp](https://github.com/nsd97/fub-mcp)
- **Language**: JavaScript/Node.js
- **Version**: 4.0.0
- **Status**: Actively maintained
- **Architecture**: Uses `@modelcontextprotocol/sdk` (v0.5.0)
- **Key Features**:
  - Single powerful `execute_custom_query` tool (replaced 42+ individual tools)
  - Read-only operations for data safety
  - Intelligent pagination and data processing
  - Custom JavaScript processing for flexible reporting
  - Comprehensive API coverage

#### 2. **FUB API Documentation** ✅
- **URL**: https://docs.followupboss.com/reference/getting-started
- **API Base**: https://api.followupboss.com/v1
- **Authentication**: API Key (Basic Auth)
- **Coverage**: Comprehensive REST API with endpoints for:
  - People/Contacts
  - Events/Activities
  - Calls, Notes, Tasks
  - Deals, Pipelines, Stages
  - Users, Teams, Groups
  - Custom Fields, Smart Lists
  - And more...

#### 3. **Python Client Library** ✅
- **Package**: `follow-up-boss` on PyPI
- **Features**: 
  - Complete API coverage
  - Type safety
  - Async support
  - Full documentation

#### 4. **MCP Server Frameworks**

**Python SDK (Official)**:
- **Repository**: https://github.com/modelcontextprotocol/python-sdk
- **Status**: Official Python SDK for MCP
- **Type**: Server and client SDK

**Other Frameworks Found**:
- **Spiceflow**: TypeScript-based API framework with MCP support
- **MCP-Use**: Comprehensive framework with React hooks
- **MCP-Startup-Framework**: Cloudflare Workers-based

## Recommended Approach

### Option 1: Python Implementation Using Official MCP SDK (Recommended)

**Why**: 
- Native Python implementation
- Uses official MCP Python SDK
- Can leverage `follow-up-boss` Python library
- Easier to maintain alongside existing JS version

**Architecture**:
```
Python MCP Server
├── Official MCP Python SDK (@modelcontextprotocol/python-sdk)
├── follow-up-boss Python client library
├── FastAPI/Flask for HTTP (optional, for webhooks)
└── Custom tool implementations
```

**Key Components**:
1. **MCP Server Core**: Using official Python SDK
2. **FUB API Client**: Using `follow-up-boss` library or direct `requests`/`httpx`
3. **Tool Definitions**: MCP tools that map to FUB API endpoints
4. **Data Processing**: Python utilities for aggregating/processing data

### Option 2: Fork/Adapt Existing JS Implementation

**Why**:
- Leverages existing, proven implementation
- Faster initial development
- Can convert incrementally to Python

**Approach**:
- Study the existing `nsd97/fub-mcp` implementation
- Port the architecture and logic to Python
- Adapt the single `execute_custom_query` tool philosophy

## Detailed Build Plan

### Phase 1: Project Setup and Foundation

#### 1.1 Project Structure
```
fub-mcp-python/
├── src/
│   ├── fub_mcp/
│   │   ├── __init__.py
│   │   ├── server.py          # Main MCP server
│   │   ├── fub_client.py       # FUB API client wrapper
│   │   ├── tools.py            # Tool definitions
│   │   ├── processors.py       # Data processing utilities
│   │   └── config.py           # Configuration management
│   └── __init__.py
├── tests/
│   ├── test_server.py
│   ├── test_fub_client.py
│   └── test_tools.py
├── examples/
│   ├── basic_usage.py
│   └── custom_reports.py
├── requirements.txt
├── setup.py
├── README.md
├── LICENSE
└── .env.example
```

#### 1.2 Dependencies
```python
# requirements.txt
mcp>=0.9.0                    # Official MCP Python SDK
follow-up-boss>=0.1.0         # FUB Python client (or use requests/httpx)
pydantic>=2.0.0              # Data validation
python-dotenv>=1.0.0          # Environment variables
asyncio                        # Async support
httpx>=0.24.0                 # HTTP client (if not using follow-up-boss)
```

### Phase 2: Core Implementation

#### 2.1 MCP Server Setup
**File**: `src/fub_mcp/server.py`

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
import asyncio

# Create MCP server instance
server = Server("fub-mcp")

# Register tools
# Register resources (if needed)
# Handle requests
```

**Key Features**:
- Use official `mcp` Python SDK
- Implement stdio transport for Claude Desktop
- Register tool handlers
- Error handling and logging

#### 2.2 FUB API Client
**File**: `src/fub_mcp/fub_client.py`

**Option A**: Use `follow-up-boss` library
```python
from follow_up_boss import FollowUpBoss

class FUBClient:
    def __init__(self, api_key: str):
        self.client = FollowUpBoss(api_key=api_key)
    
    async def get_people(self, **params):
        return await self.client.get_people(**params)
```

**Option B**: Direct HTTP client
```python
import httpx

class FUBClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.followupboss.com/v1"
        self.client = httpx.AsyncClient(
            auth=(api_key, ""),
            headers={"X-System": "FUB_MCP_Server"}
        )
```

**Key Features**:
- Async HTTP requests
- Automatic pagination
- Error handling and retries
- Rate limiting
- Date filtering utilities

#### 2.3 Tool Implementation
**File**: `src/fub_mcp/tools.py`

**Philosophy**: Follow the existing JS implementation's approach
- Primary tool: `execute_custom_query` (single powerful tool)
- Legacy tools (optional): Individual endpoint tools

**Main Tool Structure**:
```python
@server.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="execute_custom_query",
            description="Execute custom queries against FUB API...",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "endpoints": {"type": "array"},
                    "dateRange": {"type": "object"},
                    "processing": {"type": "string"}  # Python code for processing
                }
            }
        )
    ]
```

#### 2.4 Data Processing Utilities
**File**: `src/fub_mcp/processors.py`

**Key Functions**:
```python
def group_by(data: List[Dict], key: str) -> Dict[str, List]:
    """Group data by a key"""
    pass

def count_by(data: List[Dict], key: str) -> Dict[str, int]:
    """Count occurrences by key"""
    pass

def sum_by(data: List[Dict], key: str) -> float:
    """Sum values by key"""
    pass

def filter_by_date_range(data: List[Dict], date_field: str, start: str, end: str):
    """Filter data by date range"""
    pass
```

**Note**: Support Python code execution in sandboxed environment for custom processing

### Phase 3: Tool Implementation

#### 3.1 Primary Tool: `execute_custom_query`

**Features**:
- Fetch from multiple endpoints
- Apply date filtering
- Execute custom Python processing code
- Handle large datasets with pagination
- Return structured results

**Example Usage**:
```python
{
    "description": "Team performance report for June 2025",
    "endpoints": [
        {"endpoint": "/people", "params": {}, "dateField": "created"},
        {"endpoint": "/calls", "params": {}, "dateField": "created"},
        {"endpoint": "/events", "params": {}, "dateField": "occurred"}
    ],
    "dateRange": {
        "start": "2025-06-01",
        "end": "2025-06-30"
    },
    "processing": """
# Python processing code
people_by_user = utils.group_by(data['people'], 'assignedUserId')
return {
    'summary': {
        'total_leads': len(data['people']),
        'total_calls': len(data['calls'])
    },
    'by_user': people_by_user
}
    """
}
```

#### 3.2 Legacy Tools (Optional)

If implementing individual tools, create handlers for:
- `get_people`, `get_person`, `search_people`
- `get_calls`, `get_call`
- `get_events`, `get_event`
- `get_deals`, `get_deal`
- `get_tasks`, `get_task`
- `get_users`, `get_user`
- And others as needed

### Phase 4: Advanced Features

#### 4.1 Error Handling
- API error translation
- Rate limit handling
- Retry logic with exponential backoff
- Graceful degradation

#### 4.2 Security
- Environment variable management for API keys
- Sandboxed code execution
- Input validation
- Read-only mode enforcement

#### 4.3 Performance
- Async/await throughout
- Connection pooling
- Response caching (for reference data)
- Progress tracking for large queries

#### 4.4 Logging and Monitoring
- Structured logging
- Query performance metrics
- Error tracking

### Phase 5: Testing and Documentation

#### 5.1 Testing Strategy
```python
# Unit tests
- Test FUB client methods
- Test data processors
- Test tool handlers

# Integration tests
- Test end-to-end queries
- Test error scenarios
- Test rate limiting

# Example test
async def test_execute_custom_query():
    result = await server.handle_tool_call({
        "name": "execute_custom_query",
        "arguments": {...}
    })
    assert result.success
```

#### 5.2 Documentation
- README with installation instructions
- API reference
- Example queries and use cases
- Configuration guide
- Troubleshooting guide

### Phase 6: Deployment and Distribution

#### 6.1 Package Distribution
```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="fub-mcp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mcp>=0.9.0",
        "follow-up-boss>=0.1.0",  # or httpx
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "fub-mcp=fub_mcp.server:main",
        ],
    },
)
```

#### 6.2 Configuration for Claude Desktop
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

## Implementation Timeline

### Week 1: Foundation
- [ ] Set up project structure
- [ ] Install dependencies
- [ ] Create basic MCP server skeleton
- [ ] Implement FUB API client (basic)

### Week 2: Core Tools
- [ ] Implement `execute_custom_query` tool
- [ ] Add data processing utilities
- [ ] Implement pagination logic
- [ ] Add date filtering

### Week 3: Advanced Features
- [ ] Add error handling and retries
- [ ] Implement code sandboxing for processing
- [ ] Add logging and monitoring
- [ ] Performance optimizations

### Week 4: Polish
- [ ] Write tests
- [ ] Create documentation
- [ ] Add example queries
- [ ] Package for distribution

## Key Differences from JS Implementation

1. **Language**: Python vs JavaScript
2. **Processing Code**: Python instead of JavaScript for custom processing
3. **Async Model**: Python's `asyncio` vs Node.js callbacks
4. **Type Safety**: Can use Pydantic for validation
5. **Sandboxing**: Need different approach (restricted Python execution)

## Resources to Reference

1. **Existing JS Implementation**: https://github.com/nsd97/fub-mcp
   - Study the architecture and tool design
   - Understand the `execute_custom_query` philosophy
   - Review error handling patterns

2. **FUB API Documentation**: https://docs.followupboss.com/reference/getting-started
   - API endpoints and parameters
   - Authentication method
   - Rate limits and best practices

3. **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
   - Official SDK documentation
   - Example implementations
   - Best practices

4. **Python Client Library**: `follow-up-boss` on PyPI
   - Can simplify API interactions
   - Type-safe client

## Risk Mitigation

1. **API Changes**: FUB may update their API
   - Solution: Use versioned client, monitor API changes

2. **Code Execution Security**: Running user-provided Python code
   - Solution: Use restricted execution environment (restrictedpython, PySandbox)

3. **Rate Limiting**: FUB has API rate limits
   - Solution: Implement intelligent rate limiting and caching

4. **Large Dataset Handling**: Memory issues with large queries
   - Solution: Streaming processing, pagination, result size limits

## Success Criteria

1. ✅ Successfully connects to FUB API
2. ✅ Implements `execute_custom_query` tool
3. ✅ Handles pagination correctly
4. ✅ Processes data with custom Python code
5. ✅ Returns accurate results
6. ✅ Works with Claude Desktop
7. ✅ Comprehensive error handling
8. ✅ Well-documented and tested

## Next Steps

1. **Immediate**: Set up project structure and dependencies
2. **Short-term**: Implement basic MCP server and FUB client
3. **Medium-term**: Build `execute_custom_query` tool
4. **Long-term**: Add advanced features, testing, documentation

---

**Created**: 2025-01-31
**Status**: Planning Phase
**Next Review**: After initial implementation

