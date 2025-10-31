"""Download the last 5 people/contacts from Follow Up Boss."""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fub_mcp.server import call_tool


async def download_last_5_people():
    """Get and display the last 5 people/contacts."""
    print("=" * 60)
    print("Downloading Last 5 People from Follow Up Boss")
    print("=" * 60)
    print()
    
    try:
        # Get last 5 people, sorted by creation date (newest first)
        result = await call_tool("get_people", {
            "limit": 5,
            "sort": "-created",  # Sort by created date descending
            "offset": 0
        })
        
        response_data = json.loads(result[0].text)
        
        if "people" in response_data:
            people = response_data["people"]
            print(f"✅ Found {len(people)} people\n")
            
            for i, person in enumerate(people, 1):
                print(f"Person {i}:")
                print(f"  ID: {person.get('id')}")
                print(f"  Name: {person.get('name')}")
                print(f"  Created: {person.get('created')}")
                
                # Email
                emails = person.get('emails', [])
                if emails:
                    primary_email = next((e for e in emails if e.get('isPrimary') == 1), emails[0])
                    print(f"  Email: {primary_email.get('value', 'N/A')}")
                else:
                    print(f"  Email: N/A")
                
                # Phone
                phones = person.get('phones', [])
                if phones:
                    primary_phone = next((p for p in phones if p.get('isPrimary') == 1), phones[0])
                    print(f"  Phone: {primary_phone.get('value', 'N/A')}")
                else:
                    print(f"  Phone: N/A")
                
                print(f"  Source: {person.get('source', 'N/A')}")
                print(f"  Assigned To: {person.get('assignedTo', 'N/A')}")
                print(f"  Stage: {person.get('stage', 'N/A')}")
                
                tags = person.get('tags', [])
                if tags:
                    print(f"  Tags: {', '.join(tags)}")
                
                print()
            
            # Save to JSON file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"last_5_people_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump({
                    "downloaded_at": datetime.now().isoformat(),
                    "count": len(people),
                    "people": people
                }, f, indent=2, default=str)
            
            print(f"✅ Saved to: {filename}")
            print(f"   Total people downloaded: {len(people)}")
            
            return people
        else:
            print("❌ No 'people' key in response")
            print(json.dumps(response_data, indent=2))
            return None
            
    except Exception as e:
        print(f"❌ Error downloading people: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    people = asyncio.run(download_last_5_people())
    if people:
        print(f"\n✅ Successfully downloaded {len(people)} people")
        sys.exit(0)
    else:
        print("\n❌ Failed to download people")
        sys.exit(1)

