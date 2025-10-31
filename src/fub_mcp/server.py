"""Main MCP server for Follow Up Boss."""

import asyncio
import json
import sys
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .config import Config
from .fub_client import FUBClient
from .processors import DataProcessors
from .tools import get_all_tools

# Validate configuration
try:
    Config.validate()
except ValueError as e:
    print(f"Configuration error: {e}", file=sys.stderr)
    sys.exit(1)

# Create MCP server
server = Server("fub-mcp")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """
    List available MCP tools.
    
    Returns:
        List of Tool definitions including execute_custom_query and individual endpoint tools
    """
    return get_all_tools()


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """
    Handle tool execution requests.
    
    Args:
        name: Tool name
        arguments: Tool arguments
        
    Returns:
        List of TextContent with results
    """
    if name == "execute_custom_query":
        return await execute_custom_query(arguments)
    
    # Individual endpoint tools
    async with FUBClient() as fub:
        try:
            # PEOPLE ENDPOINTS
            if name == "get_people":
                params = {
                    "limit": arguments.get("limit", 20),
                    "offset": arguments.get("offset", 0),
                    "sort": arguments.get("sort", "-created"),
                }
                if arguments.get("search"):
                    params["search"] = arguments["search"]
                result = await fub.get("/people", params=params)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "get_person":
                result = await fub.get_person(arguments["personId"])
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "search_people":
                params = {"q": arguments["q"], "limit": arguments.get("limit", 20)}
                result = await fub.get("/people", params=params)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            # PEOPLE CRUD OPERATIONS
            elif name == "create_person":
                # Build person data from arguments
                person_data = {}
                if arguments.get("name"):
                    person_data["name"] = arguments["name"]
                if arguments.get("firstName"):
                    person_data["firstName"] = arguments["firstName"]
                if arguments.get("lastName"):
                    person_data["lastName"] = arguments["lastName"]
                if arguments.get("emails"):
                    person_data["emails"] = arguments["emails"]
                if arguments.get("phones"):
                    person_data["phones"] = arguments["phones"]
                if arguments.get("source"):
                    person_data["source"] = arguments["source"]
                if arguments.get("assignedUserId"):
                    person_data["assignedUserId"] = arguments["assignedUserId"]
                if arguments.get("stageId"):
                    person_data["stageId"] = arguments["stageId"]
                if arguments.get("customFields"):
                    person_data["customFields"] = arguments["customFields"]
                if arguments.get("tags"):
                    person_data["tags"] = arguments["tags"]
                
                result = await fub.create_person(person_data)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "update_person":
                person_id = arguments["personId"]
                # Build person data from arguments (exclude personId)
                person_data = {}
                if arguments.get("name"):
                    person_data["name"] = arguments["name"]
                if arguments.get("firstName"):
                    person_data["firstName"] = arguments["firstName"]
                if arguments.get("lastName"):
                    person_data["lastName"] = arguments["lastName"]
                if arguments.get("emails"):
                    person_data["emails"] = arguments["emails"]
                if arguments.get("phones"):
                    person_data["phones"] = arguments["phones"]
                if arguments.get("source"):
                    person_data["source"] = arguments["source"]
                if arguments.get("assignedUserId"):
                    person_data["assignedUserId"] = arguments["assignedUserId"]
                if arguments.get("stageId"):
                    person_data["stageId"] = arguments["stageId"]
                if arguments.get("customFields"):
                    person_data["customFields"] = arguments["customFields"]
                if arguments.get("tags"):
                    person_data["tags"] = arguments["tags"]
                
                result = await fub.update_person(person_id, person_data)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "delete_person":
                person_id = arguments["personId"]
                result = await fub.delete_person(person_id)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            # CALLS ENDPOINTS
            elif name == "get_calls":
                params = {"limit": arguments.get("limit", 20), "offset": arguments.get("offset", 0)}
                if arguments.get("personId"):
                    params["personId"] = arguments["personId"]
                result = await fub.get("/calls", params=params)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "get_call":
                result = await fub.get(f"/calls/{arguments['callId']}")
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            # EVENTS ENDPOINTS
            elif name == "get_events":
                params = {"limit": arguments.get("limit", 20), "offset": arguments.get("offset", 0)}
                if arguments.get("personId"):
                    params["personId"] = arguments["personId"]
                if arguments.get("type"):
                    params["type"] = arguments["type"]
                result = await fub.get("/events", params=params)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "get_event":
                result = await fub.get(f"/events/{arguments['eventId']}")
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            # DEALS ENDPOINTS
            elif name == "get_deals":
                params = {"limit": arguments.get("limit", 20), "offset": arguments.get("offset", 0)}
                if arguments.get("personId"):
                    params["personId"] = arguments["personId"]
                if arguments.get("pipelineId"):
                    params["pipelineId"] = arguments["pipelineId"]
                if arguments.get("stageId"):
                    params["stageId"] = arguments["stageId"]
                result = await fub.get("/deals", params=params)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "get_deal":
                result = await fub.get(f"/deals/{arguments['dealId']}")
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            # TASKS ENDPOINTS
            elif name == "get_tasks":
                params = {"limit": arguments.get("limit", 20), "offset": arguments.get("offset", 0)}
                if arguments.get("personId"):
                    params["personId"] = arguments["personId"]
                if arguments.get("assignedTo"):
                    params["assignedTo"] = arguments["assignedTo"]
                if arguments.get("status"):
                    params["status"] = arguments["status"]
                result = await fub.get("/tasks", params=params)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "get_task":
                result = await fub.get(f"/tasks/{arguments['taskId']}")
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            # USERS ENDPOINTS
            elif name == "get_users":
                params = {"limit": arguments.get("limit", 20)}
                result = await fub.get("/users", params=params)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "get_user":
                result = await fub.get(f"/users/{arguments['userId']}")
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "get_me":
                result = await fub.get_me()
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            # NOTES ENDPOINTS
            elif name == "get_notes":
                params = {"limit": arguments.get("limit", 20), "offset": arguments.get("offset", 0)}
                if arguments.get("personId"):
                    params["personId"] = arguments["personId"]
                result = await fub.get("/notes", params=params)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "get_note":
                result = await fub.get(f"/notes/{arguments['noteId']}")
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            # APPOINTMENTS ENDPOINTS
            elif name == "get_appointments":
                params = {"limit": arguments.get("limit", 20), "offset": arguments.get("offset", 0)}
                if arguments.get("personId"):
                    params["personId"] = arguments["personId"]
                if arguments.get("startDate"):
                    params["startDate"] = arguments["startDate"]
                if arguments.get("endDate"):
                    params["endDate"] = arguments["endDate"]
                result = await fub.get("/appointments", params=params)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "get_appointment":
                result = await fub.get(f"/appointments/{arguments['appointmentId']}")
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            # PIPELINES & STAGES
            elif name == "get_pipelines":
                result = await fub.get("/pipelines")
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "get_pipeline":
                result = await fub.get(f"/pipelines/{arguments['pipelineId']}")
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "get_stages":
                result = await fub.get("/stages")
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "get_stage":
                result = await fub.get(f"/stages/{arguments['stageId']}")
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            # CUSTOM FIELDS ENDPOINTS
            elif name == "get_custom_fields":
                result = await fub.get_custom_fields()
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "get_custom_field":
                result = await fub.get_custom_field(arguments["customFieldId"])
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            else:
                raise ValueError(f"Unknown tool: {name}")
        
        except Exception as e:
            error_response = {
                "error": True,
                "message": str(e),
                "tool": name,
                "arguments": arguments
            }
            print(f"Tool execution error ({name}): {e}", file=sys.stderr)
            return [TextContent(
                type="text",
                text=json.dumps(error_response, indent=2)
            )]


async def execute_custom_query(args: Dict[str, Any]) -> List[TextContent]:
    """
    Execute a custom query against FUB API.
    
    Args:
        args: Query arguments
        
    Returns:
        List of TextContent with results
    """
    description = args.get("description", "")
    endpoints = args.get("endpoints", [])
    date_range = args.get("dateRange")
    processing_code = args.get("processing", "return data")
    
    start_time = datetime.now()
    
    try:
        # Initialize FUB client
        async with FUBClient() as fub:
            # Fetch data from all requested endpoints
            data: Dict[str, List[Dict]] = {}
            
            for endpoint_config in endpoints:
                endpoint = endpoint_config.get("endpoint", "")
                params = endpoint_config.get("params", {})
                date_field = endpoint_config.get("dateField")
                
                # Clean endpoint name for use as object key
                endpoint_key = endpoint.replace("/", "_").replace("-", "_").lstrip("_")
                
                print(f"Fetching data from {endpoint}...", file=sys.stderr)
                
                # Fetch all pages
                items = await fub.fetch_all_pages(
                    endpoint,
                    params=params,
                    date_field=date_field,
                    date_range=date_range,
                    limit=Config.MAX_PAGE_SIZE
                )
                
                data[endpoint_key] = items
                print(f"Fetched {len(items)} items from {endpoint}", file=sys.stderr)
            
            # Process the data if custom processing is provided
            result = data
            processing_time_ms = 0
            
            if processing_code and processing_code.strip() != "return data":
                try:
                    process_start = datetime.now()
                    
                    # Create processing function with utilities
                    utils = DataProcessors()
                    
                    # Safe execution context
                    safe_globals = {
                        "data": data,
                        "utils": utils,
                        "json": json,
                        "__builtins__": {
                            "len": len,
                            "str": str,
                            "int": int,
                            "float": float,
                            "sum": sum,
                            "min": min,
                            "max": max,
                            "sorted": sorted,
                            "list": list,
                            "dict": dict,
                            "set": set,
                            "range": range,
                            "enumerate": enumerate,
                            "zip": zip,
                        }
                    }
                    
                    # Execute processing code in safe environment
                    # The code should either:
                    # 1. Be an expression that returns a value (assign to result)
                    # 2. Be a block that sets a 'result' variable
                    try:
                        # Try as expression first
                        if "\n" not in processing_code.strip():
                            # Single line - treat as expression
                            exec_code = f"result = {processing_code}"
                            exec(exec_code, safe_globals)
                        else:
                            # Multi-line - wrap in function
                            exec_code = f"""
def _process():
    {processing_code}
    return result if 'result' in locals() else data

result = _process()
"""
                            exec(exec_code, safe_globals)
                        
                        result = safe_globals.get("result", data)
                    except (SyntaxError, NameError) as e:
                        # If expression fails, try as block of code
                        try:
                            exec(processing_code, safe_globals)
                            # Check if result was set, otherwise return data
                            result = safe_globals.get("result", data)
                        except Exception as e2:
                            raise e2 from e
                    
                    processing_time_ms = int((datetime.now() - process_start).total_seconds() * 1000)
                    
                    # Check result size
                    result_str = json.dumps(result)
                    result_size_mb = len(result_str.encode("utf-8")) / (1024 * 1024)
                    
                    if result_size_mb > Config.MAX_RESULT_SIZE_MB:
                        result = {
                            "error": "Result too large",
                            "message": f"Result size ({result_size_mb:.2f} MB) exceeds limit ({Config.MAX_RESULT_SIZE_MB} MB)",
                            "recommendation": "Refine your processing to aggregate data instead of returning raw records",
                            "data_counts": {k: len(v) for k, v in data.items()}
                        }
                
                except Exception as e:
                    print(f"Processing error: {e}", file=sys.stderr)
                    result = {
                        "error": "Processing failed",
                        "message": str(e),
                        "recommendation": (
                            "Check your processing code syntax. "
                            "Use utils.groupBy(), utils.countBy(), etc. for common operations."
                        ),
                        "available_data": list(data.keys()),
                        "data_counts": {k: len(v) for k, v in data.items()}
                    }
            
            # Build response
            total_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            
            response = {
                "success": True,
                "query": description,
                "executedAt": datetime.now().isoformat(),
                "dateRange": date_range,
                "performance": {
                    "totalRecordsFetched": sum(len(items) for items in data.values()),
                    "processingTimeMs": processing_time_ms,
                    "totalTimeMs": total_time_ms,
                    "endpoints": [
                        {"endpoint": k, "recordCount": len(v)}
                        for k, v in data.items()
                    ]
                },
                "results": result
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(response, indent=2, default=str)
            )]
    
    except Exception as e:
        error_response = {
            "success": False,
            "error": "Query execution failed",
            "message": str(e),
            "query": description,
            "recommendation": "Verify endpoint names and parameters. Check logs for details."
        }
        
        print(f"Query execution error: {e}", file=sys.stderr)
        
        return [TextContent(
            type="text",
            text=json.dumps(error_response, indent=2)
        )]


async def main():
    """
    Main entry point for the MCP server.
    
    Supports stdio transport for compatibility with all MCP clients:
    - Claude Desktop
    - Cline
    - Continue.dev
    - Cursor IDE
    - Any MCP-compatible client
    """
    try:
        # Use stdio transport (standard for MCP, works with all clients)
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    except KeyboardInterrupt:
        print("Server stopped by user", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
