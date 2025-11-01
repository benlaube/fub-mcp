"""Debug script to check create_person API error."""

import asyncio
import sys
from pathlib import Path
import httpx
import json

sys.path.insert(0, str(Path(__file__).parent / "src"))

from fub_mcp.fub_client import FUBClient


async def test_create():
    """Test creating a person and see the actual error."""
    async with FUBClient() as client:
        try:
            # Try minimal person data
            result = await client.create_person({
                "firstName": "Test",
                "lastName": "Person"
            })
            print("Success:", json.dumps(result, indent=2))
        except httpx.HTTPStatusError as e:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response Text: {e.response.text}")
            try:
                error_json = e.response.json()
                print(f"Error JSON: {json.dumps(error_json, indent=2)}")
            except:
                pass
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_create())

