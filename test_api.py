"""Quick test script for API connection."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fub_mcp.fub_client import FUBClient


async def test_api():
    """Test API connection."""
    print("Testing FUB API connection...")
    try:
        async with FUBClient() as client:
            result = await client.get("/identity")
            print("✅ API connection successful!")
            print(f"Response keys: {list(result.keys()) if isinstance(result, dict) else 'N/A'}")
            return True
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_api())
    sys.exit(0 if success else 1)

