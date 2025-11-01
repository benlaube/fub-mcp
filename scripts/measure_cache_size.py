"""Measure actual cache memory usage."""

import asyncio
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from fub_mcp.server import call_tool
from fub_mcp.cache import get_cache_manager
import pympler.asizeof as asizeof


async def measure_cache_size():
    """Measure the actual memory usage of cached data."""
    print("=" * 80)
    print("Measuring Cache Memory Usage")
    print("=" * 80)
    print()
    
    # Get cache manager
    cache_manager = get_cache_manager(enabled=True)
    
    # Clear cache first
    cache_manager.clear()
    print("✅ Cache cleared")
    print()
    
    # Fetch different types of data to populate cache
    print("📋 Fetching data to populate cache...")
    print()
    
    # 1. Custom fields
    print("1. Fetching custom fields...")
    result = await call_tool("get_custom_fields", {})
    data1 = json.loads(result[0].text)
    fields_count = len(data1.get('customfields', []))
    print(f"   ✅ Fetched {fields_count} custom fields")
    
    # 2. Users
    print("2. Fetching users...")
    result = await call_tool("get_users", {})
    data2 = json.loads(result[0].text)
    users_count = len(data2.get('users', []))
    print(f"   ✅ Fetched {users_count} users")
    
    # 3. Pipelines
    print("3. Fetching pipelines...")
    result = await call_tool("get_pipelines", {})
    data3 = json.loads(result[0].text)
    pipelines_count = len(data3.get('pipelines', []))
    print(f"   ✅ Fetched {pipelines_count} pipelines")
    
    # 4. Stages
    print("4. Fetching stages...")
    result = await call_tool("get_stages", {})
    data4 = json.loads(result[0].text)
    stages_count = len(data4.get('stages', []))
    print(f"   ✅ Fetched {stages_count} stages")
    
    # 5. People (100 contacts)
    print("5. Fetching 100 people...")
    result = await call_tool("get_people", {"limit": 100})
    data5 = json.loads(result[0].text)
    people_count = len(data5.get('people', []))
    print(f"   ✅ Fetched {people_count} people")
    
    print()
    print("-" * 80)
    print()
    
    # Get cache stats
    stats = cache_manager.stats()
    cache_entries = stats['size']
    
    # Measure cache size
    cache_size_bytes = asizeof.asizeof(cache_manager.cache)
    cache_size_kb = cache_size_bytes / 1024
    cache_size_mb = cache_size_kb / 1024
    
    print(f"📊 Cache Statistics:")
    print(f"   Entries: {cache_entries}")
    print(f"   Size: {cache_size_bytes:,} bytes")
    print(f"   Size: {cache_size_kb:.2f} KB")
    print(f"   Size: {cache_size_mb:.2f} MB")
    print()
    
    # Calculate per-entry average
    avg_per_entry = cache_size_bytes / cache_entries if cache_entries > 0 else 0
    print(f"📐 Average per entry: {avg_per_entry:,.0f} bytes ({avg_per_entry/1024:.2f} KB)")
    print()
    
    # Extrapolate to 1000 entries
    estimated_1000 = (avg_per_entry * 1000) / (1024 * 1024)
    print(f"📈 Estimated for 1000 entries: {estimated_1000:.2f} MB")
    print()
    
    # Show individual entry sizes
    print("📦 Individual cached responses:")
    print()
    
    # Measure individual response sizes
    responses = [
        ("Custom Fields", data1, fields_count),
        ("Users", data2, users_count),
        ("Pipelines", data3, pipelines_count),
        ("Stages", data4, stages_count),
        ("People (100)", data5, people_count)
    ]
    
    for name, data, count in responses:
        size_bytes = asizeof.asizeof(data)
        size_kb = size_bytes / 1024
        per_record = size_bytes / count if count > 0 else 0
        print(f"   {name}:")
        print(f"      Total: {size_bytes:,} bytes ({size_kb:.2f} KB)")
        print(f"      Records: {count}")
        print(f"      Per record: {per_record:,.0f} bytes")
        print()


if __name__ == "__main__":
    try:
        asyncio.run(measure_cache_size())
    except ImportError as e:
        if "pympler" in str(e):
            print("❌ Error: pympler not installed")
            print()
            print("To measure actual memory usage, install pympler:")
            print("  pip install pympler")
            print()
            print("Alternative: Estimating cache size without pympler...")
            print()
            # Fallback estimation
            print("Rough estimate based on typical JSON sizes:")
            print("  - Custom field: ~500 bytes")
            print("  - User: ~800 bytes")
            print("  - Person/Contact: ~2-5 KB (varies by fields)")
            print("  - Event/Call/Note: ~1-2 KB")
            print()
            print("For 1000 cached entries (mixed types):")
            print("  Estimated: 2-10 MB")
        else:
            raise


