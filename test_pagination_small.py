"""Test pagination with a smaller number first to verify it works."""

import asyncio
import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from fub_mcp.server import call_tool


async def test_pagination():
    """Test fetching 150 contacts (should require 2 pages)."""
    print("=" * 80)
    print("Testing Pagination: Fetching 150 Contacts (should paginate)")
    print("=" * 80)
    print()
    
    start_time = time.time()
    
    try:
        print("📋 Requesting 150 contacts (max page size is 100)...")
        print("   This should trigger automatic pagination")
        print()
        
        result = await call_tool("get_people", {
            "limit": 150,
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
            print(f"   Total in response metadata: {total}")
            print()
            
            if people_count >= 150:
                print("✅ SUCCESS: Pagination working correctly!")
                print(f"   Requested: 150")
                print(f"   Received: {people_count}")
                print("   Multiple pages were fetched automatically")
            elif people_count == 100:
                print("⚠️  Only received first page (100 contacts)")
                print("   Pagination may not be working")
            else:
                print(f"ℹ️  Retrieved {people_count} contacts (database may have fewer)")
                
            # Show first and last contact
            if people_count > 0:
                print()
                print("Sample contacts:")
                print(f"  First: {response_data['people'][0].get('name')} (ID: {response_data['people'][0].get('id')})")
                if people_count > 1:
                    print(f"  Last: {response_data['people'][-1].get('name')} (ID: {response_data['people'][-1].get('id')})")
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

