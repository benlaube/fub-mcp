"""Get the most recent contact from FUB."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fub_mcp.fub_client import FUBClient


async def get_recent_contact():
    """Get the most recent contact."""
    print("Fetching most recent contact from FUB...")
    
    async with FUBClient() as client:
        try:
            # Get people, sorted by creation date (most recent first)
            result = await client.get("/people", params={
                "limit": 1,
                "sort": "-created"  # Sort by created date descending
            })
            
            # Extract people from response
            if "people" in result:
                people = result["people"]
                if people and len(people) > 0:
                    contact = people[0]
                    print("\n✅ Most Recent Contact Found:")
                    print("=" * 50)
                    print(f"Name: {contact.get('name', 'N/A')}")
                    print(f"Email: {contact.get('email', 'N/A')}")
                    print(f"Phone: {contact.get('phone', 'N/A')}")
                    print(f"ID: {contact.get('id', 'N/A')}")
                    print(f"Created: {contact.get('created', 'N/A')}")
                    print(f"Source: {contact.get('source', 'N/A')}")
                    print(f"Assigned To: {contact.get('assignedUserId', 'N/A')}")
                    print(f"Contacted: {'Yes' if contact.get('contacted') == 1 else 'No'}")
                    
                    if contact.get('tags'):
                        print(f"Tags: {', '.join(contact.get('tags', []))}")
                    
                    print("\n" + "=" * 50)
                    print("\nFull Contact Data:")
                    import json
                    print(json.dumps(contact, indent=2, default=str))
                    
                    return contact
                else:
                    print("❌ No contacts found")
                    return None
            else:
                print(f"❌ Unexpected response format: {list(result.keys())}")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching contact: {e}")
            import traceback
            traceback.print_exc()
            return None


if __name__ == "__main__":
    contact = asyncio.run(get_recent_contact())

