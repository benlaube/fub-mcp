"""
Example: CRUD operations for People/Contacts with Custom Fields

This demonstrates how to use the CRUD tools to manage contacts.
"""

import asyncio
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fub_mcp.fub_client import FUBClient
from fub_mcp.server import call_tool


async def example_crud_workflow():
    """Demonstrate complete CRUD workflow."""
    print("=" * 60)
    print("FUB MCP Server - CRUD Operations Example")
    print("=" * 60)
    print()
    
    # Step 1: Get available custom fields
    print("Step 1: Getting available custom fields...")
    result = await call_tool("get_custom_fields", {})
    custom_fields_data = json.loads(result[0].text)
    
    if "customFields" in custom_fields_data:
        print(f"✅ Found {len(custom_fields_data['customFields'])} custom fields")
        # Show first few custom fields
        for cf in custom_fields_data["customFields"][:3]:
            print(f"   - {cf.get('label')} ({cf.get('name')}): {cf.get('type')}")
    print()
    
    # Step 2: Create a person with custom fields
    print("Step 2: Creating a new person...")
    create_args = {
        "firstName": "Example",
        "lastName": "Contact",
        "emails": [
            {
                "value": "example@test.com",
                "type": "home",
                "isPrimary": 1
            }
        ],
        "phones": [
            {
                "value": "555-0000",
                "type": "mobile",
                "isPrimary": 1
            }
        ],
        "source": "Test Source",
        "customFields": {
            # Example - use actual custom field names from your account
            # "customClosePrice": "500000",
            # "customBuyerType": "First Time Buyer"
        }
    }
    
    try:
        result = await call_tool("create_person", create_args)
        person_data = json.loads(result[0].text)
        person_id = person_data.get("id")
        print(f"✅ Created person with ID: {person_id}")
        print(f"   Name: {person_data.get('name')}")
        print()
        
        # Step 3: Update the person
        if person_id:
            print(f"Step 3: Updating person {person_id}...")
            update_args = {
                "personId": str(person_id),
                "name": "Updated Example Contact",
                "customFields": {
                    # Update custom fields if they exist
                    # "customClosePrice": "550000"
                }
            }
            
            result = await call_tool("update_person", update_args)
            updated_data = json.loads(result[0].text)
            print(f"✅ Updated person: {updated_data.get('name')}")
            print()
            
            # Step 4: Get the updated person
            print(f"Step 4: Retrieving updated person {person_id}...")
            result = await call_tool("get_person", {"personId": str(person_id)})
            retrieved_data = json.loads(result[0].text)
            print(f"✅ Retrieved person: {retrieved_data.get('name')}")
            print(f"   Email: {retrieved_data.get('emails', [{}])[0].get('value', 'N/A') if retrieved_data.get('emails') else 'N/A'}")
            print()
            
            # Step 5: Delete (commented out to avoid accidental deletion)
            # print(f"Step 5: Deleting person {person_id}...")
            # result = await call_tool("delete_person", {"personId": str(person_id)})
            # print("✅ Person deleted")
            print("⚠️  Step 5 (Delete) skipped to avoid accidental deletion")
            print("   Uncomment the delete code if you want to test deletion")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


async def example_create_with_custom_fields():
    """Example: Create a person with custom fields."""
    print("\n" + "=" * 60)
    print("Example: Create Person with Custom Fields")
    print("=" * 60)
    print()
    
    # First, get custom fields to know what's available
    async with FUBClient() as fub:
        try:
            custom_fields = await fub.get_custom_fields()
            print("Available Custom Fields:")
            if "customFields" in custom_fields:
                for cf in custom_fields["customFields"][:5]:  # Show first 5
                    print(f"  - {cf.get('label')} ({cf.get('name')}): {cf.get('type')}")
            
            print("\nExample: Creating person with custom fields...")
            print("Note: Use actual custom field names from your account")
            
        except Exception as e:
            print(f"Error getting custom fields: {e}")


if __name__ == "__main__":
    print("Running CRUD examples...")
    print()
    asyncio.run(example_crud_workflow())
    asyncio.run(example_create_with_custom_fields())

