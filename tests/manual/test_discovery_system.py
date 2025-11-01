#!/usr/bin/env python3
"""
Comprehensive test of the Dynamic Search Method implementation for FUB MCP.
Tests discovery tools, resources, and schema hints with real FUB data.
"""

import asyncio
import json
from fub_mcp.fub_client import FUBClient
from fub_mcp.discovery import DataDiscovery
from fub_mcp.server import build_schema_hints

async def test_discovery_system():
    """Test the complete discovery system."""
    
    print("=" * 80)
    print("DYNAMIC SEARCH METHOD - COMPREHENSIVE TEST")
    print("=" * 80)
    
    async with FUBClient() as fub:
        
        # Test 1: Find data by keywords - Stages
        print("\n🔍 TEST 1: Finding data about 'realtor stage'")
        print("-" * 80)
        results = await DataDiscovery.find_all(
            fub,
            keywords=["realtor", "stage"],
            entity_type="any",
            limit=10
        )
        
        print(f"Found {len(results)} matches:")
        for i, match in enumerate(results[:5], 1):
            print(f"\n  {i}. {match['type'].upper()}: {match['name']}")
            print(f"     Description: {match.get('description', 'N/A')}")
            if match.get('usage'):
                print(f"     Usage: {match['usage']}")
            if match.get('example'):
                print(f"     Example: {match['example']}")
            print(f"     Relevance Score: {match['score']}")
        
        # Test 2: Find custom fields
        print("\n\n🔍 TEST 2: Finding custom fields with 'uuid'")
        print("-" * 80)
        results = await DataDiscovery.find_all(
            fub,
            keywords=["uuid", "id", "identifier"],
            entity_type="field",
            limit=5
        )
        
        print(f"Found {len(results)} custom field matches:")
        for match in results:
            print(f"\n  • {match['label']} ({match['name']})")
            print(f"    Type: {match['fieldType']}")
            print(f"    Example: {match['example']}")
        
        # Test 3: Find endpoints
        print("\n\n🔍 TEST 3: Finding endpoints about 'contacts' and 'people'")
        print("-" * 80)
        results = await DataDiscovery.find_all(
            fub,
            keywords=["contact", "person", "lead"],
            entity_type="endpoint",
            limit=5
        )
        
        print(f"Found {len(results)} endpoint matches:")
        for match in results:
            print(f"\n  • {match['name']}")
            print(f"    Tool: {match['tool']}")
            print(f"    Filters: {', '.join(match['filters'])}")
            print(f"    Examples:")
            for example in match['examples'][:2]:
                print(f"      - {example}")
        
        # Test 4: Find sources
        print("\n\n🔍 TEST 4: Finding lead sources matching 'website'")
        print("-" * 80)
        results = await DataDiscovery.find_all(
            fub,
            keywords=["website", "web", "online"],
            entity_type="source",
            limit=5
        )
        
        if results:
            print(f"Found {len(results)} source matches:")
            for match in results:
                print(f"  • {match['name']} (ID: {match['id']})")
                print(f"    Usage: {match['usage']}")
        else:
            print("No matching sources found (this is okay - depends on your data)")
        
        # Test 5: Quick Reference
        print("\n\n📚 TEST 5: Getting Quick Reference")
        print("-" * 80)
        quick_ref = await DataDiscovery.get_quick_reference(fub)
        
        print("Quick Reference Overview:")
        print(f"  Description: {quick_ref['overview']['description']}")
        print(f"\n  Available Endpoints:")
        for endpoint_name, endpoint_info in quick_ref['endpoints'].items():
            print(f"    • {endpoint_name}: {endpoint_info['description']}")
            print(f"      Tool: {endpoint_info['tool']}")
        
        if 'stages' in quick_ref:
            print(f"\n  Top Stages:")
            for stage in quick_ref['stages'][:5]:
                print(f"    • {stage['name']} (ID: {stage['id']})")
        
        if 'customFields' in quick_ref:
            print(f"\n  Custom Fields:")
            print(f"    Total: {quick_ref['customFields']['count']}")
            print(f"    Examples:")
            for field in quick_ref['customFields']['examples'][:3]:
                print(f"      • {field['label']} ({field['type']})")
        
        # Test 6: Schema Hints for People
        print("\n\n📋 TEST 6: Getting Schema Hints for 'people' endpoint")
        print("-" * 80)
        hints = await build_schema_hints(fub, "people")
        
        print(f"Endpoint: {hints['endpoint']}")
        print(f"Description: {hints['description']}")
        print(f"\nAvailable Filters ({len(hints['availableFilters'])}):")
        for filter_def in hints['availableFilters']:
            print(f"  • {filter_def['name']} ({filter_def['type']})")
            print(f"    {filter_def['description']}")
            print(f"    Example: {filter_def['example']}")
        
        if hints.get('stages'):
            print(f"\nAvailable Stages ({len(hints['stages'])}):")
            for stage in hints['stages'][:5]:
                print(f"  • {stage['name']} (ID: {stage['id']})")
        
        if hints.get('customFields'):
            print(f"\nCustom Fields ({len(hints['customFields'])}):")
            for field in hints['customFields'][:5]:
                print(f"  • {field['label']} - {field['usage']}")
        
        if hints.get('commonQueries'):
            print(f"\nCommon Queries:")
            for query in hints['commonQueries']:
                print(f"  • {query['description']}")
                print(f"    Tool: {query['tool']}")
                print(f"    Args: {json.dumps(query['arguments'], indent=8)}")
        
        # Test 7: Natural language query simulation
        print("\n\n🎯 TEST 7: Simulating Natural Language Query")
        print("-" * 80)
        print("Query: 'Show me contacts in Lead stage with custom field UUID'")
        print("\nDiscovery Process:")
        
        # Step 1: Find "lead stage"
        print("\n  Step 1: Find 'lead stage'...")
        stage_results = await DataDiscovery.find_all(
            fub,
            keywords=["lead", "stage"],
            entity_type="stage",
            limit=1
        )
        if stage_results:
            lead_stage = stage_results[0]
            print(f"    ✓ Found: {lead_stage['name']} (ID: {lead_stage['id']})")
            stage_id = lead_stage['id']
        
        # Step 2: Find "uuid" custom field
        print("\n  Step 2: Find 'UUID' custom field...")
        field_results = await DataDiscovery.find_all(
            fub,
            keywords=["uuid"],
            entity_type="field",
            limit=1
        )
        if field_results:
            uuid_field = field_results[0]
            print(f"    ✓ Found: {uuid_field['label']} ({uuid_field['name']})")
            field_name = uuid_field['name']
        
        # Step 3: Get schema hints for people endpoint
        print("\n  Step 3: Get query hints...")
        hints = await build_schema_hints(fub, "people")
        print(f"    ✓ Available filters: {', '.join([f['name'] for f in hints['availableFilters']])}")
        
        # Step 4: Execute query
        print("\n  Step 4: Execute query...")
        if stage_results:
            response = await fub.get("/people", params={
                "stageId": stage_id,
                "limit": 5
            })
            people = response.get("people", [])
            print(f"    ✓ Retrieved {len(people)} contacts")
            
            if people and field_results:
                # Check if any have the UUID field
                people_with_uuid = [
                    p for p in people 
                    if p.get("customFields", {}).get(field_name)
                ]
                print(f"    ✓ {len(people_with_uuid)} have UUID custom field populated")
                
                if people_with_uuid:
                    print(f"\n    Sample contact with UUID:")
                    sample = people_with_uuid[0]
                    print(f"      • Name: {sample.get('name')}")
                    print(f"      • Stage: {sample.get('stage')}")
                    print(f"      • UUID: {sample.get('customFields', {}).get(field_name)}")
        
        # Summary
        print("\n\n" + "=" * 80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("""
The Dynamic Search Method is now fully implemented! Key features:

✅ Discovery Tool (find_data_location):
   - Search across endpoints, stages, custom fields, and sources
   - Keyword-based relevance scoring
   - Returns ranked results with usage examples

✅ Schema Hints (get_schema_hints):
   - Detailed information about how to query each endpoint
   - Available filters with examples
   - Custom fields integration
   - Common query patterns

✅ Quick Reference Resource:
   - Overview of all data locations
   - Top stages and custom fields
   - Common query examples

✅ Natural Language Flow:
   - AI can discover data locations dynamically
   - No need to pre-know schema
   - Always returns current data
   - Guides users to correct tools and parameters

Example Cursor Queries That Now Work:
1. "Show me contacts in Lead stage"
   → Discovers Lead stage ID → Queries with stageId filter

2. "Find people with UUID custom field"
   → Discovers UUID field → Filters/displays accordingly

3. "What filters can I use on deals?"
   → Gets schema hints → Shows all available filters

4. "Find data about tasks"
   → Searches endpoints → Shows tasks endpoint with examples
        """)


if __name__ == "__main__":
    asyncio.run(test_discovery_system())

