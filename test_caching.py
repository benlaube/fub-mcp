"""Test caching functionality."""

import asyncio
import sys
import time
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from fub_mcp.server import call_tool


async def test_caching():
    """Test that caching improves performance on repeated queries."""
    print("=" * 80)
    print("Testing Caching Performance")
    print("=" * 80)
    print()
    
    # Test 1: First request (cache miss - should hit API)
    print("Test 1: First request (cache miss)")
    print("-" * 80)
    start = time.time()
    result1 = await call_tool("get_custom_fields", {})
    time1 = time.time() - start
    data1 = json.loads(result1[0].text)
    print(f"✅ Request completed in {time1:.3f} seconds")
    print(f"   Custom fields returned: {len(data1.get('customfields', []))}")
    print()
    
    # Test 2: Second request (cache hit - should be instant)
    print("Test 2: Second request (should use cache)")
    print("-" * 80)
    start = time.time()
    result2 = await call_tool("get_custom_fields", {})
    time2 = time.time() - start
    data2 = json.loads(result2[0].text)
    print(f"✅ Request completed in {time2:.3f} seconds")
    print(f"   Custom fields returned: {len(data2.get('customfields', []))}")
    print()
    
    # Compare
    speedup = time1 / time2 if time2 > 0 else float('inf')
    print(f"Performance: {speedup:.1f}x faster with cache")
    print(f"Time saved: {time1 - time2:.3f} seconds")
    print()
    
    if time2 < time1 * 0.5:  # Cache should be at least 2x faster
        print("✅ Cache is working! Second request was significantly faster.")
    else:
        print("⚠️  Cache may not be working as expected.")
    
    # Test 3: Verify data is the same
    print("Test 3: Verify cached data matches original")
    print("-" * 80)
    if data1 == data2:
        print("✅ Cached data matches original data")
    else:
        print("⚠️  Cached data differs from original (this shouldn't happen)")
    print()


if __name__ == "__main__":
    asyncio.run(test_caching())


