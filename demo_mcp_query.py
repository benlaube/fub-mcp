"""Demo: How an AI client would use the MCP server to get recent contacts."""

import asyncio
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fub_mcp.server import execute_custom_query


async def demo_mcp_query():
    """Demonstrate using the MCP server's execute_custom_query tool."""
    print("=" * 60)
    print("MCP Server Demo: Getting Most Recent Contact")
    print("=" * 60)
    print()
    
    # This is how an AI client would call the tool
    args = {
        "description": "Get the most recent contact from Follow Up Boss",
        "endpoints": [
            {
                "endpoint": "/people",
                "params": {
                    "limit": 1,
                    "sort": "-created"
                }
            }
        ],
        "processing": """
# Process the data to extract the most recent contact
if data.get('people') and len(data['people']) > 0:
    contact = data['people'][0]
    result = {
        'most_recent_contact': {
            'id': contact.get('id'),
            'name': contact.get('name'),
            'email': contact.get('emails', [{}])[0].get('value', 'N/A') if contact.get('emails') else 'N/A',
            'phone': contact.get('phones', [{}])[0].get('value', 'N/A') if contact.get('phones') else 'N/A',
            'created': contact.get('created'),
            'source': contact.get('source'),
            'assigned_to': contact.get('assignedTo'),
            'contacted': contact.get('contacted') == 1,
            'stage': contact.get('stage')
        },
        'summary': f"Most recent contact: {contact.get('name')} (ID: {contact.get('id')})"
    }
else:
    result = {'error': 'No contacts found'}
"""
    }
    
    print("Executing MCP tool: execute_custom_query")
    print(f"Query: {args['description']}")
    print()
    
    try:
        result = await execute_custom_query(args)
        
        # The result is a list of TextContent
        response_text = result[0].text
        response_data = json.loads(response_text)
        
        print("✅ Query Successful!")
        print()
        print("Response Summary:")
        print("-" * 60)
        
        if response_data.get("success"):
            results = response_data.get("results", {})
            
            if "most_recent_contact" in results:
                contact = results["most_recent_contact"]
                print(f"📇 Name: {contact.get('name')}")
                print(f"📧 Email: {contact.get('email')}")
                print(f"📞 Phone: {contact.get('phone')}")
                print(f"🆔 ID: {contact.get('id')}")
                print(f"📅 Created: {contact.get('created')}")
                print(f"🔗 Source: {contact.get('source')}")
                print(f"👤 Assigned To: {contact.get('assigned_to')}")
                print(f"✅ Contacted: {'Yes' if contact.get('contacted') else 'No'}")
                print(f"📊 Stage: {contact.get('stage')}")
                
                if results.get('summary'):
                    print()
                    print(f"Summary: {results['summary']}")
            else:
                print("No contact data in results")
                print(json.dumps(results, indent=2))
            
            print()
            print("Performance Metrics:")
            print(f"  - Records Fetched: {response_data.get('performance', {}).get('totalRecordsFetched', 0)}")
            print(f"  - Processing Time: {response_data.get('performance', {}).get('processingTimeMs', 0)}ms")
            print(f"  - Total Time: {response_data.get('performance', {}).get('totalTimeMs', 0)}ms")
        else:
            print(f"❌ Query Failed: {response_data.get('error', 'Unknown error')}")
            print(response_data.get('message', ''))
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)
    print("This demonstrates how an AI client would use the MCP server!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(demo_mcp_query())

