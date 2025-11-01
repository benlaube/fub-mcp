"""Test actual memory usage of cached data."""

import asyncio
import sys
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))

from fub_mcp.server import call_tool
from fub_mcp.cache import get_cache_manager


def get_size(obj, seen=None):
    """Recursively calculate size of objects in bytes."""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    
    seen.add(obj_id)
    
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    
    return size


async def test_memory_usage():
    """Calculate actual memory usage of cached data."""
    print("=" * 80)
    print("Testing Memory Usage of Cache")
    print("=" * 80)
    print()
    
    cache_manager = get_cache_manager()
    
    # Clear cache first
    cache_manager.clear()
    print("📋 Cleared cache to start fresh")
    print()
    
    # Test 1: Cache a small dataset (custom fields)
    print("Test 1: Caching custom fields...")
    print("-" * 80)
    result = await call_tool("get_custom_fields", {})
    data = json.loads(result[0].text)
    custom_fields_count = len(data.get('customfields', []))
    
    # Calculate size
    cache_stats = cache_manager.stats()
    print(f"✅ Cached {custom_fields_count} custom fields")
    print(f"   Cache entries: {cache_stats['size']}")
    
    # Estimate size
    data_size = get_size(data)
    print(f"   Estimated data size: {data_size:,} bytes ({data_size/1024:.2f} KB)")
    print()
    
    # Test 2: Cache multiple people queries
    print("Test 2: Caching people queries...")
    print("-" * 80)
    
    # Get 100 people
    result = await call_tool("get_people", {"limit": 100})
    people_data = json.loads(result[0].text)
    people_count = len(people_data.get('people', []))
    
    cache_stats = cache_manager.stats()
    print(f"✅ Cached {people_count} people")
    print(f"   Cache entries: {cache_stats['size']}")
    
    people_size = get_size(people_data)
    print(f"   People data size: {people_size:,} bytes ({people_size/1024:.2f} KB)")
    print()
    
    # Test 3: Multiple different queries
    print("Test 3: Multiple different queries...")
    print("-" * 80)
    
    queries = [
        ("get_users", {}),
        ("get_pipelines", {}),
        ("get_stages", {}),
        ("get_people", {"limit": 50}),
        ("get_people", {"limit": 20, "offset": 100}),
    ]
    
    for tool_name, args in queries:
        await call_tool(tool_name, args)
    
    cache_stats = cache_manager.stats()
    print(f"✅ Executed {len(queries)} more queries")
    print(f"   Total cache entries: {cache_stats['size']}")
    print()
    
    # Calculate total cache size
    total_size = 0
    for entry_info in cache_stats['entries']:
        # This is approximate - we'd need to access the actual cache entries
        pass
    
    # Estimate based on what we know
    avg_entry_size = (data_size + people_size) / 2
    estimated_total = avg_entry_size * cache_stats['size']
    
    print("Summary:")
    print("-" * 80)
    print(f"Total cache entries: {cache_stats['size']}")
    print(f"Average entry size: ~{avg_entry_size/1024:.2f} KB")
    print(f"Estimated total cache size: ~{estimated_total/1024:.2f} KB ({estimated_total/1024/1024:.2f} MB)")
    print()
    
    # Extrapolate to 1000 entries
    print("Extrapolation to 1000 entries:")
    print("-" * 80)
    size_for_1000 = avg_entry_size * 1000
    print(f"Estimated size for 1000 cache entries: ~{size_for_1000/1024:.2f} KB ({size_for_1000/1024/1024:.2f} MB)")
    print()
    
    # Test single person record size
    print("Test 4: Size of single person record...")
    print("-" * 80)
    if people_count > 0:
        single_person = people_data['people'][0]
        single_person_size = get_size(single_person)
        print(f"Single person record: {single_person_size:,} bytes ({single_person_size/1024:.2f} KB)")
        print(f"Estimated 1000 people: {single_person_size * 1000 / 1024:.2f} KB ({single_person_size * 1000 / 1024 / 1024:.2f} MB)")
    print()


if __name__ == "__main__":
    asyncio.run(test_memory_usage())

