"""Test script to create a dummy contact in Follow Up Boss."""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fub_mcp.server import call_tool


async def create_dummy_contact():
    """Create a dummy/test contact in FUB."""
    print("=" * 60)
    print("Creating Dummy Contact in Follow Up Boss")
    print("=" * 60)
    print()
    
    # Create a unique name with timestamp to avoid duplicates
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    create_args = {
        "firstName": "Test",
        "lastName": f"Dummy_{timestamp}",
        "emails": [
            {
                "value": f"test.dummy.{timestamp}@example.com",
                "type": "home",
                "isPrimary": 1
            }
        ],
        "phones": [
            {
                "value": f"555{timestamp[-4:]}",  # Remove dashes, just numbers
                "type": "mobile",
                "isPrimary": 1
            }
        ],
        "source": "MCP Test"
    }
    
    contact_name = f"{create_args['firstName']} {create_args['lastName']}"
    print(f"Creating contact: {contact_name}")
    print(f"Email: {create_args['emails'][0]['value']}")
    print(f"Phone: {create_args['phones'][0]['value']}")
    print()
    
    try:
        result = await call_tool("create_person", create_args)
        
        import json
        response_data = json.loads(result[0].text)
        
        if "id" in response_data:
            print("✅ Contact Created Successfully!")
            print("=" * 60)
            print(f"Contact ID: {response_data['id']}")
            print(f"Name: {response_data.get('name')}")
            print(f"Created: {response_data.get('created')}")
            print(f"Source: {response_data.get('source')}")
            print(f"Tags: {response_data.get('tags', [])}")
            
            if response_data.get('emails'):
                print(f"Email: {response_data['emails'][0].get('value')}")
            if response_data.get('phones'):
                print(f"Phone: {response_data['phones'][0].get('value')}")
            
            print()
            print("Full Contact Data:")
            print(json.dumps(response_data, indent=2, default=str))
            
            return response_data
        else:
            print("❌ Failed to create contact")
            print(json.dumps(response_data, indent=2))
            return None
            
    except Exception as e:
        print(f"❌ Error creating contact: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    contact = asyncio.run(create_dummy_contact())
    if contact:
        print(f"\n✅ Dummy contact created with ID: {contact.get('id')}")
        sys.exit(0)
    else:
        print("\n❌ Failed to create dummy contact")
        sys.exit(1)

