"""Check existing custom fields and test if we can create one."""

import asyncio
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from fub_mcp.fub_client import FUBClient


async def check_custom_fields():
    """Check existing custom fields and test creation."""
    print("=" * 80)
    print("Checking Custom Fields API Capabilities")
    print("=" * 80)
    print()
    
    async with FUBClient() as fub:
        # Get existing custom fields
        print("📋 Fetching existing custom fields...")
        try:
            result = await fub.get_custom_fields()
            print(f"✅ Successfully retrieved custom fields")
            print()
            
            # Try to parse the response
            if isinstance(result, dict):
                # Check what keys are in the response
                print("Response structure:")
                print(f"  Keys: {list(result.keys())}")
                print()
                
                # Try to find custom fields in response
                custom_fields = None
                if "customFields" in result:
                    custom_fields = result["customFields"]
                elif "data" in result:
                    custom_fields = result["data"]
                elif isinstance(result.get(list(result.keys())[0]), list):
                    custom_fields = result[list(result.keys())[0]]
                
                if custom_fields:
                    print(f"Found {len(custom_fields)} custom fields:")
                    for cf in custom_fields[:5]:  # Show first 5
                        print(f"  • {cf.get('name', 'N/A')} ({cf.get('id', 'N/A')})")
                        print(f"    Type: {cf.get('type', 'N/A')}")
                        print(f"    Field: {cf.get('field', 'N/A')}")
                    if len(custom_fields) > 5:
                        print(f"  ... and {len(custom_fields) - 5} more")
                    print()
                else:
                    print("⚠️  Could not find custom fields array in response")
                    print(json.dumps(result, indent=2, default=str)[:500])
                    print()
                
                # Check if UUID field already exists
                uuid_field = None
                if custom_fields:
                    for cf in custom_fields:
                        if "uuid" in cf.get("name", "").lower() or "uuid" in cf.get("field", "").lower():
                            uuid_field = cf
                            break
                
                if uuid_field:
                    print(f"✅ UUID custom field already exists:")
                    print(f"   Name: {uuid_field.get('name')}")
                    print(f"   ID: {uuid_field.get('id')}")
                    print(f"   Field: {uuid_field.get('field')}")
                    print(f"   Type: {uuid_field.get('type')}")
                else:
                    print("ℹ️  UUID custom field does not exist yet")
                    print()
                    print("🔧 Testing custom field creation...")
                    print()
                    
                    # Try to create a custom field
                    # Note: Need to check FUB API docs for exact format
                    test_field_data = {
                        "name": "UUID",
                        "field": "uuid",  # Internal field name
                        "type": "text",  # Assuming text type
                        # May need additional fields like:
                        # "required": False,
                        # "visible": True,
                        # etc.
                    }
                    
                    print("Attempting to create custom field with data:")
                    print(json.dumps(test_field_data, indent=2))
                    print()
                    
                    try:
                        # Try POST to /customFields
                        create_result = await fub.post("/customFields", json_data=test_field_data)
                        print("✅ SUCCESS! Custom field created:")
                        print(json.dumps(create_result, indent=2, default=str))
                    except Exception as e:
                        print(f"❌ Failed to create custom field: {e}")
                        print()
                        print("This endpoint may not support POST requests, or we need")
                        print("to implement create_custom_field tool first.")
                        
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(check_custom_fields())

