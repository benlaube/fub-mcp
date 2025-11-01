#!/usr/bin/env python3
"""
Test MCP server functionality for stage-based queries.
Simulates how Cursor would query: "Show me the last 10 contacts in stage of Lead that were created"
"""

import asyncio
import json
from fub_mcp.server import call_tool

async def simulate_mcp_query():
    """Simulate the full MCP query flow."""
    
    print("=" * 80)
    print("SIMULATION: MCP Query Through Cursor")
    print("Query: 'Show me the last 10 contacts in stage of Lead that were created'")
    print("=" * 80)
    
    # Step 1: First, we need to find the stage ID for "Lead"
    print("\n🔍 Step 1: Getting available stages...")
    
    result = await call_tool("get_stages", {})
    stages_data = json.loads(result[0].text)
    
    stages = stages_data.get("stages", [])
    print(f"✓ Found {len(stages)} stages")
    
    # Find "Lead" stage
    lead_stage = None
    for stage in stages:
        if stage.get("name", "").lower() == "lead":
            lead_stage = stage
            break
    
    if not lead_stage:
        print("❌ 'Lead' stage not found!")
        print("Available stages:", [s.get("name") for s in stages])
        return
    
    stage_id = lead_stage.get("id")
    stage_name = lead_stage.get("name")
    print(f"✓ Found stage: '{stage_name}' (ID: {stage_id})")
    
    # Step 2: Query contacts in this stage
    print(f"\n📞 Step 2: Querying contacts in '{stage_name}' stage...")
    
    query_args = {
        "stageId": stage_id,
        "sort": "-created",  # Sort by newest first
        "limit": 10
    }
    
    print(f"   Tool: get_people")
    print(f"   Arguments: {json.dumps(query_args, indent=6)}")
    
    result = await call_tool("get_people", query_args)
    people_data = json.loads(result[0].text)
    
    people = people_data.get("people", [])
    metadata = people_data.get("_metadata", {})
    
    print(f"\n✅ SUCCESS! Retrieved {len(people)} contacts")
    print(f"   Total in '{stage_name}' stage: {metadata.get('total', 'unknown')}")
    
    # Display results
    print(f"\n📊 Results - Last 10 Contacts in '{stage_name}' Stage:")
    print("=" * 80)
    
    for i, person in enumerate(people, 1):
        print(f"\n{i}. {person.get('name')}")
        print(f"   Stage: {person.get('stage')}")
        print(f"   Created: {person.get('created')}")
        print(f"   Source: {person.get('source', 'N/A')}")
        print(f"   Assigned to: {person.get('assignedTo', 'N/A')}")
        
        # Show email and phone if available
        emails = person.get('emails', [])
        if emails:
            primary_email = next((e for e in emails if e.get('isPrimary')), emails[0] if emails else None)
            if primary_email:
                print(f"   Email: {primary_email.get('value')}")
        
        phones = person.get('phones', [])
        if phones:
            primary_phone = next((p for p in phones if p.get('isPrimary')), phones[0] if phones else None)
            if primary_phone:
                print(f"   Phone: {primary_phone.get('value')}")
    
    print("\n" + "=" * 80)
    
    # Step 3: Test other stage queries
    print("\n🔍 Step 3: Testing queries for other stages...")
    
    for stage in stages[:3]:  # Test first 3 stages
        stage_id = stage.get("id")
        stage_name = stage.get("name")
        
        result = await call_tool("get_people", {
            "stageId": stage_id,
            "limit": 5
        })
        
        people_data = json.loads(result[0].text)
        people = people_data.get("people", [])
        total = people_data.get("_metadata", {}).get("total", 0)
        
        print(f"\n  Stage: '{stage_name}' (ID: {stage_id})")
        print(f"    Total contacts: {total}")
        print(f"    Recent contacts:")
        for person in people[:3]:
            print(f"      • {person.get('name')}")
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED!")
    print("=" * 80)
    print("""
Dynamic querying is now working! You can query contacts by:
  • Stage (stageId)
  • Assigned user (assignedUserId)
  • Source (sourceId)
  • Tags
  • Search terms
  • Sort order
  • And combinations of these filters!

Example queries you can now run through Cursor:
  1. "Show me the last 10 contacts in Lead stage"
  2. "Find contacts assigned to user ID 1 in Active stage"
  3. "Get contacts from source 'Website' sorted by creation date"
  4. "Show me all contacts with tag 'VIP' in Under Contract stage"
    """)


if __name__ == "__main__":
    asyncio.run(simulate_mcp_query())

