"""Test pagination with 1,000 contacts."""

import asyncio
import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from fub_mcp.server import call_tool


async def test_pagination():
    """Test fetching 1,000 contacts."""
    print("=" * 80)
    print("Testing Pagination: Fetching 1,000 Contacts")
    print("=" * 80)
    print()
    
    start_time = time.time()
    
    try:
        # Request 1,000 contacts
        print("📋 Requesting 1,000 contacts...")
        print("   Note: This will test if pagination works correctly")
        print()
        
        result = await call_tool("get_people", {
            "limit": 1000,
            "offset": 0,
            "sort": "-created"
        })
        
        elapsed = time.time() - start_time
        
        response_data = json.loads(result[0].text)
        
        # Check what we got
        if "people" in response_data:
            people_count = len(response_data["people"])
            metadata = response_data.get("_metadata", {})
            total = metadata.get("total", "unknown")
            
            print(f"✅ Request completed in {elapsed:.2f} seconds")
            print(f"   Contacts received: {people_count}")
            print(f"   Total available: {total}")
            print(f"   Has more: {metadata.get('nextLink', 'N/A')}")
            print()
            
            if people_count < 1000 and total and isinstance(total, int) and total > people_count:
                print("⚠️  WARNING: Only partial results returned!")
                print(f"   Requested: 1,000")
                print(f"   Received: {people_count}")
                print(f"   Available: {total}")
                print()
                print("   The current implementation may not be properly paginating.")
                print("   It should use fetch_all_pages() to get all requested contacts.")
            elif people_count >= 1000:
                print("✅ Successfully retrieved 1,000+ contacts")
            else:
                print(f"ℹ️  Retrieved {people_count} contacts (database has {total} total)")
        else:
            print("❌ Unexpected response format:")
            print(json.dumps(response_data, indent=2)[:500])
            
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ Error after {elapsed:.2f} seconds: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_pagination())

