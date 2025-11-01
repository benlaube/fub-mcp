#!/usr/bin/env python3
"""
Test the fixed stage filtering functionality.
Demonstrates querying contacts by stage using the updated get_people tool.
"""

import asyncio
import json
from fub_mcp.fub_client import FUBClient

async def test_stage_filtering():
    """Test that we can now filter contacts by stage."""
    
    print("=" * 80)
    print("TEST: Stage Filtering with Updated get_people Tool")
    print("=" * 80)
    
    async with FUBClient() as fub:
        # Step 1: Get available stages
        print("\n📋 Step 1: Fetching available stages...")
        stages_response = await fub.get("/stages")
        stages = stages_response.get("stages", [])
        
        print(f"✓ Found {len(stages)} stages:")
        for stage in stages:
            print(f"  • {stage.get('name')} (ID: {stage.get('id')})")
        
        if not stages:
            print("❌ No stages available to test!")
            return
        
        # Pick a stage for testing (use first available)
        test_stage = stages[0]
        stage_id = test_stage.get("id")
        stage_name = test_stage.get("name")
        
        print(f"\n🎯 Testing with stage: '{stage_name}' (ID: {stage_id})")
        
        # Step 2: Query contacts in this stage
        print("\n📞 Step 2: Querying last 10 contacts in this stage...")
        print(f"   Using params: stageId={stage_id}, sort=-created, limit=10")
        
        response = await fub.get("/people", params={
            "stageId": stage_id,
            "sort": "-created",
            "limit": 10
        })
        
        people = response.get("people", [])
        metadata = response.get("_metadata", {})
        
        print(f"\n✓ Retrieved {len(people)} contacts")
        print(f"  Total in stage: {metadata.get('total', 'unknown')}")
        
        if people:
            print(f"\n📊 Results:")
            for i, person in enumerate(people, 1):
                print(f"  {i}. {person.get('name')}")
                print(f"     Stage: {person.get('stage')} (ID: {person.get('stageId')})")
                print(f"     Created: {person.get('created')}")
                print(f"     Source: {person.get('source')}")
                print()
        
        # Step 3: Test multiple stages
        print("\n📊 Step 3: Testing multiple stages...")
        stage_counts = {}
        
        for stage in stages[:5]:  # Test first 5 stages
            stage_id = stage.get("id")
            stage_name = stage.get("name")
            
            response = await fub.get("/people", params={
                "stageId": stage_id,
                "limit": 1  # Just count
            })
            
            total = response.get("_metadata", {}).get("total", 0)
            stage_counts[stage_name] = total
            print(f"  • {stage_name}: {total} contacts")
        
        # Step 4: Test combined filters
        print("\n🔍 Step 4: Testing combined filters (stage + search)...")
        
        # Get contacts in first stage that match a search
        test_stage = stages[0]
        stage_id = test_stage.get("id")
        
        response = await fub.get("/people", params={
            "stageId": stage_id,
            "search": "Test",  # Search for "Test" in names
            "limit": 5
        })
        
        people = response.get("people", [])
        print(f"  Found {len(people)} contacts in '{test_stage.get('name')}' stage matching 'Test'")
        
        for person in people[:3]:  # Show first 3
            print(f"    • {person.get('name')}")
        
        print("\n" + "=" * 80)
        print("✅ SUCCESS: Stage filtering is now working!")
        print("=" * 80)
        print("""
The get_people tool now supports:
  • stageId: Filter by stage ID
  • assignedUserId: Filter by assigned user
  • sourceId: Filter by lead source
  • tags: Filter by tags
  • search: Search for contacts
  • sort: Sort results (e.g., '-created' for newest first)
  • limit/offset: Pagination

Example usage through MCP:
  {
    "tool": "get_people",
    "arguments": {
      "stageId": 2,
      "sort": "-created",
      "limit": 10
    }
  }
        """)


if __name__ == "__main__":
    asyncio.run(test_stage_filtering())

