"""Verify the UUID custom field was created."""

import asyncio
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from fub_mcp.server import call_tool


async def verify_uuid():
    """Verify UUID field exists."""
    result = await call_tool("get_custom_field", {"customFieldId": "276"})
    field = json.loads(result[0].text)
    print("✅ UUID Custom Field Verified:")
    print(json.dumps(field, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(verify_uuid())

