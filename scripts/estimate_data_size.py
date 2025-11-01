"""Estimate data size for cached entries."""

import asyncio
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from fub_mcp.server import call_tool


async def estimate_size():
    """Estimate the memory usage of different data types."""
    print("=" * 80)
    print("Estimating Data Sizes")
    print("=" * 80)
    print()
    
    # Fetch sample data
    samples = []
    
    # 1. People (100 contacts)
    print("Fetching 100 people...")
    result = await call_tool("get_people", {"limit": 100})
    data = json.loads(result[0].text)
    people = data.get('people', [])
    print(f"✅ Fetched {len(people)} people")
    
    if people:
        # Serialize to JSON to get realistic size
        json_str = json.dumps(people)
        total_bytes = len(json_str.encode('utf-8'))
        total_kb = total_bytes / 1024
        total_mb = total_kb / 1024
        per_person_bytes = total_bytes / len(people)
        per_person_kb = per_person_bytes / 1024
        
        print()
        print(f"📊 100 People Statistics:")
        print(f"   Total JSON size: {total_bytes:,} bytes")
        print(f"   Total JSON size: {total_kb:.2f} KB")
        print(f"   Total JSON size: {total_mb:.2f} MB")
        print(f"   Per person: {per_person_bytes:,.0f} bytes ({per_person_kb:.2f} KB)")
        print()
        
        # Extrapolate to 1000
        est_1000_bytes = per_person_bytes * 1000
        est_1000_kb = est_1000_bytes / 1024
        est_1000_mb = est_1000_kb / 1024
        
        print(f"📈 Estimated for 1,000 people:")
        print(f"   Total: {est_1000_bytes:,.0f} bytes")
        print(f"   Total: {est_1000_kb:.2f} KB")
        print(f"   Total: {est_1000_mb:.2f} MB")
        print()
        
        # Show sample record
        if len(people) > 0:
            print("📝 Sample person record (first entry):")
            sample_json = json.dumps(people[0], indent=2)
            sample_bytes = len(sample_json.encode('utf-8'))
            print(f"   Size: {sample_bytes:,} bytes ({sample_bytes/1024:.2f} KB)")
            print()
            print("   Fields present:")
            for key in people[0].keys():
                print(f"      - {key}")
            print()
    
    # 2. Custom fields for context
    print("-" * 80)
    print()
    result = await call_tool("get_custom_fields", {})
    data = json.loads(result[0].text)
    fields = data.get('customfields', [])
    
    if fields:
        json_str = json.dumps(fields)
        total_bytes = len(json_str.encode('utf-8'))
        per_field = total_bytes / len(fields) if fields else 0
        print(f"📊 Custom Fields ({len(fields)} fields):")
        print(f"   Total: {total_bytes:,} bytes ({total_bytes/1024:.2f} KB)")
        print(f"   Per field: {per_field:,.0f} bytes")
        print()
    
    # 3. Users for context
    result = await call_tool("get_users", {})
    data = json.loads(result[0].text)
    users = data.get('users', [])
    
    if users:
        json_str = json.dumps(users)
        total_bytes = len(json_str.encode('utf-8'))
        per_user = total_bytes / len(users) if users else 0
        print(f"📊 Users ({len(users)} users):")
        print(f"   Total: {total_bytes:,} bytes ({total_bytes/1024:.2f} KB)")
        print(f"   Per user: {per_user:,.0f} bytes")
        print()
    
    print("=" * 80)
    print()
    print("💡 Key Insights:")
    print()
    print("   1. FUB API limit: 100 records per request")
    print("   2. For 1,000 people: Need 10 API calls (paginated)")
    print("   3. Typical person record: 2-5 KB (varies by custom fields)")
    print("   4. 1,000 people cached: ~2-5 MB in memory")
    print()
    print("   ✅ Current cache limit: 1,000 entries (plenty of headroom)")
    print()


if __name__ == "__main__":
    asyncio.run(estimate_size())

