#!/usr/bin/env python3
"""
Test querying contacts by stage using the MCP server.
This tests the scenario: "Show me the last 10 contacts in stage of Realtor that were created"
"""

import asyncio
import json
from fub_mcp.fub_client import FUBClient
from fub_mcp.config import Config

async def test_stage_query():
    """Test querying contacts by stage."""
    
    print("=" * 80)
    print("TEST: Query Last 10 Contacts in 'Realtor' Stage")
    print("=" * 80)
    
    async with FUBClient() as fub:
        # Step 1: Get all stages to find "Realtor" stage ID
        print("\n1. Fetching all stages...")
        try:
            stages_response = await fub.get("/stages")
            print(f"✓ Stages response structure: {list(stages_response.keys())}")
            
            stages = stages_response.get("stages", [])
            print(f"✓ Found {len(stages)} stages")
            
            # Print all stages
            print("\nAvailable stages:")
            realtor_stage_id = None
            for stage in stages:
                stage_id = stage.get("id")
                stage_name = stage.get("name")
                print(f"  - ID: {stage_id}, Name: {stage_name}")
                
                # Find Realtor stage (case-insensitive)
                if stage_name and stage_name.lower() == "realtor":
                    realtor_stage_id = stage_id
            
            if not realtor_stage_id:
                print("\n⚠️  WARNING: 'Realtor' stage not found!")
                print("Available stage names:", [s.get("name") for s in stages])
                
                # Try to find a stage to use for testing
                if stages:
                    realtor_stage_id = stages[0].get("id")
                    print(f"Using first available stage for testing: {stages[0].get('name')} (ID: {realtor_stage_id})")
                else:
                    print("❌ No stages available to test with!")
                    return
            else:
                print(f"\n✓ Found 'Realtor' stage with ID: {realtor_stage_id}")
        
        except Exception as e:
            print(f"❌ Error fetching stages: {e}")
            return
        
        # Step 2: Test direct API call with stageId parameter
        print(f"\n2. Testing direct API call with stageId={realtor_stage_id}...")
        try:
            # Test 1: Try stageId parameter
            print("\n   Test 2a: Using 'stageId' parameter...")
            response = await fub.get("/people", params={
                "stageId": realtor_stage_id,
                "sort": "-created",
                "limit": 10
            })
            
            people = response.get("people", [])
            print(f"   ✓ Retrieved {len(people)} people")
            
            if people:
                print(f"\n   First result:")
                person = people[0]
                print(f"     - Name: {person.get('name')}")
                print(f"     - Stage: {person.get('stage')}")
                print(f"     - Stage ID: {person.get('stageId')}")
                print(f"     - Created: {person.get('created')}")
        except Exception as e:
            print(f"   ❌ Error with stageId parameter: {e}")
            
            # Test 2: Try stage parameter
            print("\n   Test 2b: Using 'stage' parameter...")
            try:
                response = await fub.get("/people", params={
                    "stage": realtor_stage_id,
                    "sort": "-created",
                    "limit": 10
                })
                
                people = response.get("people", [])
                print(f"   ✓ Retrieved {len(people)} people")
                
                if people:
                    print(f"\n   First result:")
                    person = people[0]
                    print(f"     - Name: {person.get('name')}")
                    print(f"     - Stage: {person.get('stage')}")
                    print(f"     - Stage ID: {person.get('stageId')}")
                    print(f"     - Created: {person.get('created')}")
            except Exception as e:
                print(f"   ❌ Error with stage parameter: {e}")
        
        # Step 3: Test fetch_all_pages with filtering
        print("\n3. Testing fetch_all_pages with manual filtering...")
        try:
            # Fetch all people and filter manually
            all_people = await fub.fetch_all_pages(
                "/people",
                params={"sort": "-created"},
                limit=100
            )
            
            print(f"   ✓ Fetched {len(all_people)} total people")
            
            # Filter by stage ID
            filtered_people = [
                p for p in all_people 
                if p.get("stageId") == realtor_stage_id
            ]
            
            print(f"   ✓ Filtered to {len(filtered_people)} people in Realtor stage")
            
            # Get first 10
            top_10 = filtered_people[:10]
            
            print(f"\n   Top 10 people in Realtor stage:")
            for i, person in enumerate(top_10, 1):
                print(f"     {i}. {person.get('name')} - Created: {person.get('created')}")
        
        except Exception as e:
            print(f"   ❌ Error with fetch_all_pages: {e}")
        
        # Step 4: Test what parameters are actually supported
        print("\n4. Testing parameter support...")
        try:
            # Get 5 people to examine structure
            response = await fub.get("/people", params={"limit": 5, "sort": "-created"})
            people = response.get("people", [])
            
            if people:
                print(f"   Sample person fields:")
                sample = people[0]
                for key in sorted(sample.keys()):
                    value = sample.get(key)
                    if isinstance(value, (str, int, float, bool, type(None))):
                        print(f"     - {key}: {value}")
                    else:
                        print(f"     - {key}: <{type(value).__name__}>")
        
        except Exception as e:
            print(f"   ❌ Error examining people structure: {e}")
        
        print("\n" + "=" * 80)
        print("CONCLUSION:")
        print("=" * 80)
        print("""
The FUB API's /people endpoint may not support direct filtering by stageId.
To query "last 10 contacts in stage of Realtor that were created", we need to:

Option 1: Use execute_custom_query with manual filtering:
  - Fetch all people (or recent people)
  - Filter by stageId in processing code
  - Return top 10

Option 2: Add stageId support to get_people tool if API supports it

Option 3: Use search parameter if it supports stage filtering
        """)


if __name__ == "__main__":
    asyncio.run(test_stage_query())

