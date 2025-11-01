"""Main MCP server for Follow Up Boss."""

import asyncio
import json
import sys
import os
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Resource
import httpx

from .config import Config
from .fub_client import FUBClient
from .processors import DataProcessors
from .tools import get_all_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fub_mcp_server.log'),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

# Validate configuration
try:
    Config.validate()
    logger.info("FUB MCP Server configuration validated successfully")
except ValueError as e:
    logger.error(f"Configuration error: {e}")
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


@server.list_resources()
async def list_resources() -> List[Resource]:
    """
    List available MCP resources for dynamic discovery.
    
    Returns:
        List of Resource definitions
    """
    return [
        Resource(
            uri="fub://schema/quick-reference",
            name="FUB Quick Reference Guide",
            description="⭐ READ THIS FIRST! Common data locations, stages, custom fields, and query examples",
            mimeType="application/json"
        ),
        Resource(
            uri="fub://schema/endpoints",
            name="FUB API Endpoints Index",
            description="Complete list of available endpoints with descriptions and capabilities",
            mimeType="application/json"
        ),
        Resource(
            uri="fub://schema/custom-fields",
            name="Custom Fields Schema",
            description="All custom fields with types and usage examples",
            mimeType="application/json"
        )
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """
    Read a resource by URI.
    
    Args:
        uri: Resource URI string
        
    Returns:
        Resource content as JSON string
    """
    
    async with FUBClient() as fub:
        if uri == "fub://schema/quick-reference":
            from .discovery import DataDiscovery
            quick_ref = await DataDiscovery.get_quick_reference(fub)
            return json.dumps(quick_ref, indent=2, default=str)
        
        elif uri == "fub://schema/endpoints":
            from .discovery import DataDiscovery
            endpoints_info = {
                "endpoints": DataDiscovery.ENDPOINTS,
                "tip": "Use find_data_location to search by keywords"
            }
            return json.dumps(endpoints_info, indent=2)
        
        elif uri == "fub://schema/custom-fields":
            try:
                response = await fub.get("/customFields")
                fields = response.get("customFields", [])
                
                fields_schema = {
                    "totalFields": len(fields),
                    "fields": [
                        {
                            "id": f.get("id"),
                            "name": f.get("name"),
                            "label": f.get("label"),
                            "type": f.get("type"),
                            "usage": f"Use in create_person/update_person: customFields={{'{f.get('name')}': 'value'}}"
                        }
                        for f in fields
                    ],
                    "tip": "Use find_data_location to search custom fields by keyword"
                }
                return json.dumps(fields_schema, indent=2)
            except Exception as e:
                return json.dumps({"error": str(e)})
        
        else:
            raise ValueError(f"Unknown resource: {uri}")


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
    # Log incoming request
    logger.info(f"Tool called: {name} with arguments: {json.dumps(arguments, default=str)[:200]}")
    
    if name == "execute_custom_query":
        return await execute_custom_query(arguments)
    
    # Discovery tools
    async with FUBClient() as fub:
        if name == "find_data_location":
            from .discovery import DataDiscovery
            
            keywords = arguments.get("keywords", [])
            entity_type = arguments.get("entity_type", "any")
            limit = arguments.get("limit", 10)
            
            results = await DataDiscovery.find_all(
                fub,
                keywords=keywords,
                entity_type=entity_type,
                limit=limit
            )
            
            response = {
                "query": {
                    "keywords": keywords,
                    "entityType": entity_type,
                    "limit": limit
                },
                "resultsFound": len(results),
                "matches": results,
                "tip": "Use get_schema_hints for detailed information about how to query an endpoint"
            }
            
            return [TextContent(type="text", text=json.dumps(response, indent=2, default=str))]
        
        elif name == "get_schema_hints":
            endpoint = arguments.get("endpoint")
            
            # Build schema hints based on endpoint
            hints = await build_schema_hints(fub, endpoint)
            
            return [TextContent(type="text", text=json.dumps(hints, indent=2, default=str))]
    
    # Individual endpoint tools
    async with FUBClient() as fub:
        try:
            # PEOPLE ENDPOINTS
            if name == "get_people":
                # SMART DATE FILTERING: Convert smart date expressions
                from .date_filters import DateFilters
                arguments = DateFilters.convert_filters(arguments)
                
                limit = arguments.get("limit", 20)
                offset = arguments.get("offset", 0)
                sort = arguments.get("sort", "-created")
                include_custom_fields = arguments.get("includeCustomFields", True)
                
                # Build params dict - DYNAMIC: pass through ALL arguments
                params = {"sort": sort}
                
                # CRITICAL: Include custom fields by default
                if include_custom_fields:
                    params["fields"] = "allFields"
                
                # Known filter parameters to pass through
                known_filters = [
                    "search", "stageId", "assignedUserId", "sourceId", "tags",
                    "created", "updated", "email", "phone", "name",
                    "createdAfter", "createdBefore", "updatedAfter", "updatedBefore"
                ]
                
                # Add all known filters if provided
                for filter_name in known_filters:
                    if filter_name in arguments and arguments[filter_name] is not None:
                        params[filter_name] = arguments[filter_name]
                
                # DYNAMIC: Also pass through any custom field filters
                # Format: customFields.fieldName=value
                for key, value in arguments.items():
                    if key.startswith("customFields.") and value is not None:
                        params[key] = value
                
                # If requesting more than max page size, use fetch_all_pages for automatic pagination
                if limit > Config.MAX_PAGE_SIZE:
                    # Fetch all pages up to the requested limit
                    all_people = await fub.fetch_all_pages(
                        "/people",
                        params=params,
                        limit=Config.MAX_PAGE_SIZE
                    )
                    
                    # Apply offset and limit to the results
                    if offset > 0:
                        all_people = all_people[offset:]
                    if limit and len(all_people) > limit:
                        all_people = all_people[:limit]
                    
                    # Format response to match API structure
                    result = {
                        "people": all_people,
                        "_metadata": {
                            "limit": limit,
                            "offset": offset,
                            "total": len(all_people),
                            "returned": len(all_people)
                        }
                    }
                else:
                    # Single page request - use regular endpoint
                    params["limit"] = limit
                    params["offset"] = offset
                    result = await fub.get("/people", params=params)
                
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "get_person":
                person_id = arguments["personId"]
                # Include custom fields by default
                result = await fub.get(f"/people/{person_id}", params={"fields": "allFields"})
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "search_people":
                params = {"q": arguments["q"], "limit": arguments.get("limit", 20)}
                result = await fub.get("/people", params=params)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "check_duplicates":
                from .duplicate_checker import DuplicateChecker
                
                email = arguments.get("email")
                phone = arguments.get("phone")
                first_name = arguments.get("firstName")
                last_name = arguments.get("lastName")
                search_limit = arguments.get("searchLimit", 500)
                
                if not email and not phone:
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "error": True,
                            "message": "At least one of 'email' or 'phone' must be provided"
                        }, indent=2)
                    )]
                
                if phone and (not first_name or not last_name):
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "error": True,
                            "message": "Both 'firstName' and 'lastName' are required when checking by phone"
                        }, indent=2)
                    )]
                
                # Search for contacts efficiently
                # If email provided, search by email first
                contacts_to_check = []
                
                if email:
                    # Search by email
                    search_result = await fub.get("/people", params={
                        "search": email,
                        "limit": search_limit
                    })
                    if "people" in search_result:
                        contacts_to_check.extend(search_result["people"])
                
                if phone:
                    # Search by phone
                    search_result = await fub.get("/people", params={
                        "search": phone,
                        "limit": search_limit
                    })
                    if "people" in search_result:
                        # Add contacts that aren't already in the list
                        existing_ids = {c.get("id") for c in contacts_to_check}
                        for contact in search_result["people"]:
                            if contact.get("id") not in existing_ids:
                                contacts_to_check.append(contact)
                
                # If we didn't find contacts via search, get a broader sample
                # This handles cases where exact match search might miss variations
                if len(contacts_to_check) < 50:
                    # Get recent contacts to check against
                    recent_result = await fub.get("/people", params={
                        "limit": min(search_limit, 500),
                        "sort": "-created"
                    })
                    if "people" in recent_result:
                        existing_ids = {c.get("id") for c in contacts_to_check}
                        for contact in recent_result["people"]:
                            if contact.get("id") not in existing_ids:
                                contacts_to_check.append(contact)
                
                # Check for duplicates
                duplicates = DuplicateChecker.find_duplicates(
                    contacts_to_check,
                    email=email,
                    phone=phone,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Format result
                result = DuplicateChecker.format_duplicate_result(duplicates)
                result["searchedContacts"] = len(contacts_to_check)
                result["searchCriteria"] = {
                    "email": email,
                    "phone": phone,
                    "firstName": first_name,
                    "lastName": last_name
                }
                
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            # PEOPLE CRUD OPERATIONS
            elif name == "create_person":
                # Invalidate people cache when creating
                from .cache import get_cache_manager
                cache_manager = get_cache_manager(enabled=Config.ENABLE_CACHING)
                if cache_manager.enabled:
                    cache_manager.invalidate("/people")
                
                # Build person data from arguments
                person_data = {}
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
                if arguments.get("tags"):
                    person_data["tags"] = arguments["tags"]
                
                # CRITICAL FIX: Custom fields are TOP-LEVEL, not nested!
                # FUB API expects: { "customUUID": "value" } not { "customFields": { "customUUID": "value" }}
                if arguments.get("customFields"):
                    for field_name, field_value in arguments["customFields"].items():
                        # Add custom prefix if not already present
                        if not field_name.startswith("custom"):
                            field_name = f"custom{field_name[0].upper()}{field_name[1:]}"
                        person_data[field_name] = field_value
                
                result = await fub.create_person(person_data)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "update_person":
                # Invalidate people cache when updating
                from .cache import get_cache_manager
                cache_manager = get_cache_manager(enabled=Config.ENABLE_CACHING)
                if cache_manager.enabled:
                    cache_manager.invalidate("/people")
                person_id = arguments["personId"]
                
                # Build person data from arguments (exclude personId)
                person_data = {}
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
                if arguments.get("tags"):
                    person_data["tags"] = arguments["tags"]
                
                # CRITICAL FIX: Custom fields are TOP-LEVEL, not nested!
                if arguments.get("customFields"):
                    for field_name, field_value in arguments["customFields"].items():
                        # Add custom prefix if not already present
                        if not field_name.startswith("custom"):
                            field_name = f"custom{field_name[0].upper()}{field_name[1:]}"
                        person_data[field_name] = field_value
                
                result = await fub.update_person(person_id, person_data)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "delete_person":
                # Invalidate people cache when deleting
                from .cache import get_cache_manager
                cache_manager = get_cache_manager(enabled=Config.ENABLE_CACHING)
                if cache_manager.enabled:
                    cache_manager.invalidate("/people")
                person_id = arguments["personId"]
                result = await fub.delete_person(person_id)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "batch_update_people":
                # Invalidate people cache
                from .cache import get_cache_manager
                cache_manager = get_cache_manager(enabled=Config.ENABLE_CACHING)
                if cache_manager.enabled:
                    cache_manager.invalidate("/people")
                
                updates = arguments.get("updates", [])
                stop_on_error = arguments.get("stopOnError", False)
                
                logger.info(f"Starting batch update of {len(updates)} contacts")
                
                results = {
                    "total": len(updates),
                    "successful": 0,
                    "failed": 0,
                    "results": []
                }
                
                for i, update in enumerate(updates):
                    person_id = update.get("personId")
                    person_data = update.get("data", {})
                    
                    try:
                        logger.debug(f"Updating person {i+1}/{len(updates)}: {person_id}")
                        result = await fub.update_person(person_id, person_data)
                        
                        results["successful"] += 1
                        results["results"].append({
                            "personId": person_id,
                            "status": "success",
                            "result": result
                        })
                        
                    except Exception as e:
                        logger.error(f"Failed to update person {person_id}: {e}")
                        results["failed"] += 1
                        results["results"].append({
                            "personId": person_id,
                            "status": "failed",
                            "error": str(e)
                        })
                        
                        if stop_on_error:
                            results["message"] = f"Stopped after {i+1} updates due to error"
                            break
                
                logger.info(f"Batch update complete: {results['successful']} successful, {results['failed']} failed")
                return [TextContent(type="text", text=json.dumps(results, indent=2, default=str))]
            
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
            
            elif name == "create_custom_field":
                # Invalidate custom fields cache
                from .cache import get_cache_manager
                cache_manager = get_cache_manager(enabled=Config.ENABLE_CACHING)
                if cache_manager.enabled:
                    cache_manager.invalidate("/customFields")
                custom_field_data = {
                    "label": arguments["label"],
                    "type": arguments["type"]
                }
                # Note: 'name' is auto-generated by FUB API, don't include it
                # Optional fields
                if "orderWeight" in arguments:
                    custom_field_data["orderWeight"] = arguments["orderWeight"]
                if "hideIfEmpty" in arguments:
                    custom_field_data["hideIfEmpty"] = arguments["hideIfEmpty"]
                if "readOnly" in arguments:
                    custom_field_data["readOnly"] = arguments["readOnly"]
                if "options" in arguments:
                    custom_field_data["options"] = arguments["options"]
                result = await fub.create_custom_field(custom_field_data)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "update_custom_field":
                # Invalidate custom fields cache
                from .cache import get_cache_manager
                cache_manager = get_cache_manager(enabled=Config.ENABLE_CACHING)
                if cache_manager.enabled:
                    cache_manager.invalidate("/customFields")
                custom_field_data = {}
                # Only include fields that are provided
                if "label" in arguments:
                    custom_field_data["label"] = arguments["label"]
                if "type" in arguments:
                    custom_field_data["type"] = arguments["type"]
                if "orderWeight" in arguments:
                    custom_field_data["orderWeight"] = arguments["orderWeight"]
                if "hideIfEmpty" in arguments:
                    custom_field_data["hideIfEmpty"] = arguments["hideIfEmpty"]
                if "readOnly" in arguments:
                    custom_field_data["readOnly"] = arguments["readOnly"]
                if "options" in arguments:
                    custom_field_data["options"] = arguments["options"]
                result = await fub.update_custom_field(arguments["customFieldId"], custom_field_data)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            elif name == "delete_custom_field":
                # Invalidate custom fields cache
                from .cache import get_cache_manager
                cache_manager = get_cache_manager(enabled=Config.ENABLE_CACHING)
                if cache_manager.enabled:
                    cache_manager.invalidate("/customFields")
                result = await fub.delete_custom_field(arguments["customFieldId"])
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
            else:
                raise ValueError(f"Unknown tool: {name}")
        
        except Exception as e:
            logger.error(f"Tool execution error ({name}): {e}", exc_info=True)
            
            # Enhanced error messages with context
            error_response = await build_enhanced_error(e, name, arguments, fub)
            
            return [TextContent(
                type="text",
                text=json.dumps(error_response, indent=2)
            )]


async def build_enhanced_error(
    exception: Exception,
    tool_name: str,
    arguments: Dict[str, Any],
    fub_client: FUBClient
) -> Dict[str, Any]:
    """
    Build enhanced error message with context and helpful suggestions.
    
    Args:
        exception: The exception that occurred
        tool_name: Name of the tool that failed
        arguments: Arguments passed to the tool
        fub_client: FUB client for fetching context
        
    Returns:
        Enhanced error response with helpful information
    """
    error_response = {
        "error": True,
        "message": str(exception),
        "tool": tool_name,
        "arguments": arguments
    }
    
    # Handle HTTP errors with context
    if isinstance(exception, httpx.HTTPStatusError):
        status_code = exception.response.status_code
        error_response["status_code"] = status_code
        
        try:
            api_error = exception.response.json()
            error_response["api_error"] = api_error
        except:
            pass
        
        # Add contextual help based on error type and tool
        if status_code == 400:  # Bad Request
            # Check for common issues
            if "stageId" in arguments:
                try:
                    stages_response = await fub_client.get("/stages")
                    stages = stages_response.get("stages", [])
                    stage_list = [f"{s['name']} (ID: {s['id']})" for s in stages[:10]]
                    
                    error_response["helpfulContext"] = {
                        "issue": f"Invalid stageId: {arguments['stageId']}",
                        "availableStages": stage_list,
                        "suggestion": "Use find_data_location to discover valid stage IDs",
                        "example": f"find_data_location({{\"keywords\": [\"stage\", \"name\"], \"entity_type\": \"stage\"}})"
                    }
                except:
                    pass
            
            elif "assignedUserId" in arguments:
                error_response["helpfulContext"] = {
                    "issue": f"Invalid assignedUserId: {arguments['assignedUserId']}",
                    "suggestion": "Use get_users to see available users",
                    "example": "get_users()"
                }
            
            elif "sourceId" in arguments:
                error_response["helpfulContext"] = {
                    "issue": f"Invalid sourceId: {arguments['sourceId']}",
                    "suggestion": "Use find_data_location to discover valid sources",
                    "example": f"find_data_location({{\"keywords\": [\"source\"], \"entity_type\": \"source\"}})"
                }
        
        elif status_code == 404:  # Not Found
            if "personId" in arguments:
                error_response["helpfulContext"] = {
                    "issue": f"Person not found: {arguments['personId']}",
                    "suggestion": "Verify the person ID exists with get_person or search_people"
                }
        
        elif status_code == 429:  # Rate Limit
            error_response["helpfulContext"] = {
                "issue": "Rate limit exceeded",
                "suggestion": "Wait a moment before retrying. Consider using batch operations for bulk updates.",
                "recommendation": "Use batch_update_people for updating multiple contacts at once"
            }
    
    # Add general suggestions based on tool
    if tool_name == "get_people":
        if "helpfulContext" not in error_response:
            error_response["helpfulContext"] = {
                "availableFilters": ["stageId", "assignedUserId", "sourceId", "tags", "search"],
                "suggestion": "Use get_schema_hints to see all available filters and examples",
                "example": "get_schema_hints({\"endpoint\": \"people\"})"
            }
    
    return error_response


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


async def build_schema_hints(fub: FUBClient, endpoint: str) -> Dict[str, Any]:
    """
    Build schema hints for an endpoint with query examples.
    
    Args:
        fub: FUB client
        endpoint: Endpoint name
        
    Returns:
        Schema hints with examples and filters
    """
    hints = {
        "endpoint": endpoint,
        "path": f"/api/v1/{endpoint}",
        "description": "",
        "availableFilters": [],
        "commonQueries": [],
        "customFields": [],
        "relatedEndpoints": []
    }
    
    # People endpoint
    if endpoint == "people":
        hints["description"] = "Contacts, leads, and clients in your database"
        hints["availableFilters"] = [
            {
                "name": "stageId",
                "type": "number",
                "description": "Filter by stage (use get_stages to find IDs)",
                "example": "stageId=2"
            },
            {
                "name": "assignedUserId",
                "type": "number",
                "description": "Filter by assigned user",
                "example": "assignedUserId=1"
            },
            {
                "name": "sourceId",
                "type": "number",
                "description": "Filter by lead source",
                "example": "sourceId=210"
            },
            {
                "name": "tags",
                "type": "string",
                "description": "Filter by tags (comma-separated)",
                "example": "tags='VIP,Hot Lead'"
            },
            {
                "name": "search",
                "type": "string",
                "description": "Search names, emails, phones",
                "example": "search='John'"
            },
            {
                "name": "sort",
                "type": "string",
                "description": "Sort order",
                "example": "sort='-created' (newest first)"
            }
        ]
        
        # Get stages for examples
        try:
            stages_response = await fub.get("/stages")
            stages = stages_response.get("stages", [])
            
            if stages:
                hints["commonQueries"].append({
                    "description": f"Last 10 contacts in '{stages[0].get('name')}' stage",
                    "tool": "get_people",
                    "arguments": {
                        "stageId": stages[0].get("id"),
                        "sort": "-created",
                        "limit": 10
                    }
                })
                
                hints["stages"] = [
                    {"id": s.get("id"), "name": s.get("name")}
                    for s in stages
                ]
        except Exception:
            pass
        
        # Get custom fields
        try:
            fields_response = await fub.get("/customFields")
            fields = fields_response.get("customFields", [])
            
            hints["customFields"] = [
                {
                    "name": f.get("name"),
                    "label": f.get("label"),
                    "type": f.get("type"),
                    "usage": f"customFields.{f.get('name')}"
                }
                for f in fields
            ]
        except Exception:
            pass
        
        hints["relatedEndpoints"] = ["deals", "tasks", "events", "notes"]
    
    # Deals endpoint
    elif endpoint == "deals":
        hints["description"] = "Real estate deals and transactions"
        hints["availableFilters"] = [
            {
                "name": "personId",
                "type": "string",
                "description": "Filter by person ID",
                "example": "personId='12345'"
            },
            {
                "name": "pipelineId",
                "type": "string",
                "description": "Filter by pipeline",
                "example": "pipelineId='1'"
            },
            {
                "name": "stageId",
                "type": "string",
                "description": "Filter by deal stage",
                "example": "stageId='7'"
            }
        ]
        hints["relatedEndpoints"] = ["people", "pipelines"]
    
    # Tasks endpoint
    elif endpoint == "tasks":
        hints["description"] = "Tasks and to-dos"
        hints["availableFilters"] = [
            {
                "name": "personId",
                "type": "string",
                "description": "Filter by person",
                "example": "personId='12345'"
            },
            {
                "name": "assignedTo",
                "type": "string",
                "description": "Filter by assigned user ID",
                "example": "assignedTo='1'"
            },
            {
                "name": "status",
                "type": "string",
                "description": "Filter by status",
                "example": "status='pending'"
            }
        ]
        hints["commonQueries"].append({
            "description": "Pending tasks assigned to me",
            "tool": "get_tasks",
            "arguments": {
                "status": "pending",
                "assignedTo": "<user_id>"
            }
        })
        hints["relatedEndpoints"] = ["people"]
    
    # Events endpoint
    elif endpoint == "events":
        hints["description"] = "Activity history and interactions"
        hints["availableFilters"] = [
            {
                "name": "personId",
                "type": "string",
                "description": "Filter by person",
                "example": "personId='12345'"
            },
            {
                "name": "type",
                "type": "string",
                "description": "Filter by event type",
                "example": "type='call'"
            }
        ]
        hints["relatedEndpoints"] = ["people", "calls"]
    
    return hints


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
