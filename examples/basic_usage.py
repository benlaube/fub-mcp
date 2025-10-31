"""
Basic usage example for FUB MCP Server.

This example demonstrates how to use the execute_custom_query tool
programmatically (for testing purposes).
"""

import asyncio
import json
from fub_mcp.server import execute_custom_query


async def example_simple_query():
    """Example: Simple query to get people count."""
    args = {
        "description": "Get total number of people",
        "endpoints": [
            {
                "endpoint": "/people",
                "params": {}
            }
        ]
    }
    
    result = await execute_custom_query(args)
    print(json.dumps(json.loads(result[0].text), indent=2))


async def example_date_range_query():
    """Example: Query with date range filtering."""
    args = {
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
    
    result = await execute_custom_query(args)
    print(json.dumps(json.loads(result[0].text), indent=2))


async def example_processed_query():
    """Example: Query with custom processing."""
    args = {
        "description": "Team performance summary",
        "endpoints": [
            {
                "endpoint": "/people",
                "dateField": "created"
            },
            {
                "endpoint": "/calls",
                "dateField": "created"
            }
        ],
        "dateRange": {
            "start": "2025-06-01",
            "end": "2025-06-30"
        },
        "processing": """
# Count people by assigned user
people_by_user = utils.countBy(data['people'], 'assignedUserId')

# Count calls by user
calls_by_user = utils.countBy(data['calls'], 'userId')

# Build summary
result = {
    'total_leads': len(data['people']),
    'total_calls': len(data['calls']),
    'by_user': {
        user_id: {
            'leads': people_by_user.get(user_id, 0),
            'calls': calls_by_user.get(user_id, 0)
        }
        for user_id in set(list(people_by_user.keys()) + list(calls_by_user.keys()))
    }
}
"""
    }
    
    result = await execute_custom_query(args)
    print(json.dumps(json.loads(result[0].text), indent=2))


if __name__ == "__main__":
    print("Example 1: Simple Query")
    print("=" * 50)
    asyncio.run(example_simple_query())
    
    print("\n\nExample 2: Date Range Query")
    print("=" * 50)
    asyncio.run(example_date_range_query())
    
    print("\n\nExample 3: Processed Query")
    print("=" * 50)
    asyncio.run(example_processed_query())

