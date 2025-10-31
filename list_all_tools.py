"""List all available MCP tools and identify gaps."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from fub_mcp.server import list_tools


async def list_all_tools():
    """List all tools organized by category."""
    tools = await list_tools()
    
    print("=" * 80)
    print(f"📋 FUB MCP SERVER - TOTAL TOOLS: {len(tools)}")
    print("=" * 80)
    print()
    
    # Categorize tools
    categories = {
        "CRUD - People": [],
        "Read - People": [],
        "Custom Fields": [],
        "Read - Calls": [],
        "Read - Events": [],
        "Read - Deals": [],
        "Read - Tasks": [],
        "Read - Notes": [],
        "Read - Appointments": [],
        "Read - Users": [],
        "Read - Pipelines/Stages": [],
        "Advanced": []
    }
    
    for tool in tools:
        name = tool.name
        if name in ["create_person", "update_person", "delete_person"]:
            categories["CRUD - People"].append(tool)
        elif name in ["get_people", "get_person", "search_people"]:
            categories["Read - People"].append(tool)
        elif "custom" in name.lower() or "customField" in name:
            categories["Custom Fields"].append(tool)
        elif "call" in name.lower():
            categories["Read - Calls"].append(tool)
        elif "event" in name.lower():
            categories["Read - Events"].append(tool)
        elif "deal" in name.lower():
            categories["Read - Deals"].append(tool)
        elif "task" in name.lower():
            categories["Read - Tasks"].append(tool)
        elif "note" in name.lower():
            categories["Read - Notes"].append(tool)
        elif "appointment" in name.lower():
            categories["Read - Appointments"].append(tool)
        elif "user" in name.lower() or name == "get_me":
            categories["Read - Users"].append(tool)
        elif "pipeline" in name.lower() or "stage" in name.lower():
            categories["Read - Pipelines/Stages"].append(tool)
        elif "execute" in name.lower():
            categories["Advanced"].append(tool)
    
    # Print categorized
    total_shown = 0
    for category, tool_list in categories.items():
        if tool_list:
            print(f"## {category} ({len(tool_list)} tools)")
            for tool in sorted(tool_list, key=lambda t: t.name):
                total_shown += 1
                desc = tool.description[:70] + "..." if len(tool.description) > 70 else tool.description
                print(f"  • {tool.name:30} - {desc}")
            print()
    
    print("=" * 80)
    print(f"Total: {total_shown} tools")
    print("=" * 80)
    print()
    
    # Identify gaps
    print("## 🔍 POTENTIAL GAPS / MISSING CAPABILITIES")
    print()
    print("Based on FUB API, we may be missing:")
    print()
    print("### CRUD Operations Missing:")
    print("  ❌ create_custom_field - Create new custom fields")
    print("  ❌ update_custom_field - Update existing custom fields")
    print("  ❌ delete_custom_field - Delete custom fields")
    print("  ❌ create_deal - Create new deals")
    print("  ❌ update_deal - Update existing deals")
    print("  ❌ delete_deal - Delete deals")
    print("  ❌ create_note - Create new notes")
    print("  ❌ update_note - Update existing notes")
    print("  ❌ delete_note - Delete notes")
    print("  ❌ create_task - Create new tasks")
    print("  ❌ update_task - Update existing tasks")
    print("  ❌ delete_task - Delete tasks")
    print("  ❌ create_appointment - Create appointments")
    print("  ❌ update_appointment - Update appointments")
    print("  ❌ delete_appointment - Delete appointments")
    print("  ❌ create_event - Create events")
    print("  ❌ create_call - Create call records")
    print()
    print("### Other Potential Endpoints:")
    print("  ❌ Smart Lists - get_smart_lists, get_smart_list")
    print("  ❌ Teams/Groups - get_teams, get_groups")
    print("  ❌ Relationships - get_relationships")
    print("  ❌ Webhooks - webhook management")
    print("  ❌ Automations - automation management")
    print()
    
    return tools


if __name__ == "__main__":
    asyncio.run(list_all_tools())

