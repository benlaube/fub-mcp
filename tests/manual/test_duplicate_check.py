"""Test the duplicate checking functionality."""

import asyncio
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from fub_mcp.server import call_tool


async def test_duplicate_check():
    """Test duplicate checking with various scenarios."""
    print("=" * 80)
    print("Testing Duplicate Check Functionality")
    print("=" * 80)
    print()
    
    # Test 1: Check by email
    print("Test 1: Checking for duplicates by email...")
    print("-" * 80)
    try:
        result = await call_tool("check_duplicates", {
            "email": "test.dummy.20251031_160648@example.com",
            "searchLimit": 100
        })
        response_data = json.loads(result[0].text)
        
        print(f"✅ Duplicate check completed")
        print(f"   Has duplicates: {response_data.get('hasDuplicates')}")
        print(f"   Duplicate count: {response_data.get('duplicateCount')}")
        print(f"   Contacts searched: {response_data.get('searchedContacts')}")
        
        if response_data.get("duplicates"):
            print(f"\n   Found {len(response_data['duplicates'])} duplicate(s):")
            for dup in response_data["duplicates"]:
                print(f"     - ID: {dup.get('id')}, Name: {dup.get('name')}")
                print(f"       Match reasons: {', '.join(dup.get('matchReasons', []))}")
                print(f"       Confidence: {dup.get('confidence')}")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print()
    
    # Test 2: Check by phone and name
    print("Test 2: Checking for duplicates by phone and name...")
    print("-" * 80)
    try:
        result = await call_tool("check_duplicates", {
            "phone": "5550648",
            "firstName": "Test",
            "lastName": "Dummy_20251031_160648",
            "searchLimit": 100
        })
        response_data = json.loads(result[0].text)
        
        print(f"✅ Duplicate check completed")
        print(f"   Has duplicates: {response_data.get('hasDuplicates')}")
        print(f"   Duplicate count: {response_data.get('duplicateCount')}")
        print(f"   Contacts searched: {response_data.get('searchedContacts')}")
        
        if response_data.get("duplicates"):
            print(f"\n   Found {len(response_data['duplicates'])} duplicate(s):")
            for dup in response_data["duplicates"]:
                print(f"     - ID: {dup.get('id')}, Name: {dup.get('name')}")
                print(f"       Match reasons: {', '.join(dup.get('matchReasons', []))}")
                print(f"       Confidence: {dup.get('confidence')}")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print()
    
    # Test 3: Check for a non-existent contact (should find no duplicates)
    print("Test 3: Checking for a non-existent contact...")
    print("-" * 80)
    try:
        result = await call_tool("check_duplicates", {
            "email": "definitely.does.not.exist@example.com",
            "searchLimit": 100
        })
        response_data = json.loads(result[0].text)
        
        print(f"✅ Duplicate check completed")
        print(f"   Has duplicates: {response_data.get('hasDuplicates')}")
        print(f"   Duplicate count: {response_data.get('duplicateCount')}")
        print(f"   Contacts searched: {response_data.get('searchedContacts')}")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print()
    
    print("=" * 80)
    print("✅ All tests completed")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_duplicate_check())

