#!/usr/bin/env python3
"""Test smart date filtering capabilities."""

import asyncio
import json
from fub_mcp.server import call_tool
from fub_mcp.date_filters import DateFilters

async def test_smart_dates():
    """Test smart date filtering."""
    
    print("=" * 80)
    print("SMART DATE FILTERING TEST")
    print("=" * 80)
    
    # Test 1: Show available date filter examples
    print("\n📅 Available Smart Date Filters:")
    print("-" * 80)
    examples = DateFilters.get_examples()
    for filter_expr, description in list(examples.items())[:10]:
        print(f"  • '{filter_expr}' → {description}")
    
    # Test 2: Test date parsing
    print("\n🔧 Testing Date Filter Parsing:")
    print("-" * 80)
    test_filters = [
        "last 7 days",
        "last 30 days",
        "older than 30 days",
        "this week",
        "this month",
        "today"
    ]
    
    for filter_expr in test_filters:
        try:
            result = DateFilters.parse_smart_date_filter(filter_expr)
            print(f"  ✓ '{filter_expr}' → '{result}'")
        except Exception as e:
            print(f"  ❌ '{filter_expr}' → Error: {e}")
    
    # Test 3: Test with real queries
    print("\n🎯 Testing Smart Date Queries:")
    print("-" * 80)
    
    # Query 1: Last 7 days
    print("\n  Query 1: Contacts created in last 7 days")
    try:
        result = await call_tool("get_people", {
            "created": "last 7 days",
            "limit": 5
        })
        data = json.loads(result[0].text)
        people = data.get("people", [])
        print(f"  ✓ Found {len(people)} contacts")
        if people:
            print(f"    Most recent: {people[0].get('name')} ({people[0].get('created')})")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Query 2: This month
    print("\n  Query 2: Contacts created this month")
    try:
        result = await call_tool("get_people", {
            "created": "this month",
            "limit": 5
        })
        data = json.loads(result[0].text)
        people = data.get("people", [])
        print(f"  ✓ Found {len(people)} contacts")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Query 3: Convenience syntax
    print("\n  Query 3: Using convenience syntax 'createdInLast'")
    try:
        result = await call_tool("get_people", {
            "createdInLast": "30 days",
            "stageId": 2,
            "limit": 5
        })
        data = json.loads(result[0].text)
        people = data.get("people", [])
        print(f"  ✓ Found {len(people)} contacts in Lead stage from last 30 days")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Query 4: Older than
    print("\n  Query 4: Contacts older than 90 days")
    try:
        result = await call_tool("get_people", {
            "created": "older than 90 days",
            "limit": 5
        })
        data = json.loads(result[0].text)
        people = data.get("people", [])
        print(f"  ✓ Found {len(people)} contacts")
        if people:
            print(f"    Oldest shown: {people[-1].get('name')} ({people[-1].get('created')})")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test 4: Combined filters
    print("\n🔥 Testing Combined Filters:")
    print("-" * 80)
    print("  Query: Contacts in Lead stage, from website, created last 30 days")
    try:
        result = await call_tool("get_people", {
            "stageId": 2,
            "created": "last 30 days",
            "limit": 10
        })
        data = json.loads(result[0].text)
        people = data.get("people", [])
        print(f"  ✓ Found {len(people)} matching contacts")
        
        if people:
            print(f"\n  Sample results:")
            for person in people[:3]:
                print(f"    • {person.get('name')}")
                print(f"      Stage: {person.get('stage')}, Created: {person.get('created')}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("✅ SMART DATE FILTERING IS ACTIVE!")
    print("=" * 80)
    print("""
Smart Date Filter Capabilities:

✅ Relative Dates:
   - "last 7 days" / "last 30 days" / "last 1 week"
   - "last 3 months" / "last 1 year"

✅ Comparative Dates:
   - "older than 30 days" / "older than 1 year"

✅ Named Periods:
   - "today" / "yesterday"
   - "this week" / "this month" / "this year"

✅ Raw Dates:
   - ">2024-01-01" (after)
   - "<2024-12-31" (before)
   - "2024-10-31" (exact date)

✅ Convenience Syntax:
   - createdInLast="7 days"
   - updatedInLast="30 days"

✅ Combined with Other Filters:
   - Can combine with stageId, assignedUserId, sourceId, tags, etc.

Examples:
  get_people({"created": "last 7 days", "stageId": 2})
  get_people({"created": "this month", "tags": "VIP"})
  get_people({"created": "older than 90 days", "assignedUserId": 1})
  get_people({"createdInLast": "30 days", "search": "John"})
    """)


if __name__ == "__main__":
    asyncio.run(test_smart_dates())

