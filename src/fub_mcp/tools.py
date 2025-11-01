"""Individual tool definitions for common FUB API endpoints."""

from typing import Any, Dict, List
from mcp.types import Tool


def get_all_tools() -> List[Tool]:
    """
    Get all available tools including the main execute_custom_query
    and individual endpoint tools.
    """
    return [
        # DISCOVERY & SEARCH TOOLS
        Tool(
            name="find_data_location",
            description=(
                "🔍 DISCOVERY TOOL - Use FIRST for natural language queries! "
                "Search for data by keywords to find where information lives. "
                "Searches across: endpoints (people, deals, tasks), stages, custom fields, "
                "sources, users, and more. Returns ranked results with query hints. "
                "Example: keywords=['realtor', 'stage'] finds stage filtering options."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "array",
                        "description": "Keywords to search for (e.g., ['stage', 'realtor'], ['custom', 'field'], ['deal', 'value'])",
                        "items": {"type": "string"}
                    },
                    "entity_type": {
                        "type": "string",
                        "description": "What to search for: 'endpoint', 'field', 'stage', 'source', 'any' (default)",
                        "enum": ["endpoint", "field", "stage", "source", "user", "any"],
                        "default": "any"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum results to return (default: 10)",
                        "default": 10
                    }
                },
                "required": ["keywords"]
            }
        ),
        Tool(
            name="get_schema_hints",
            description=(
                "Get detailed schema information with query hints for an endpoint. "
                "Returns available fields, filter options, common queries, and examples. "
                "Use after find_data_location to understand how to query the data."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "endpoint": {
                        "type": "string",
                        "description": "Endpoint name: 'people', 'deals', 'tasks', 'events', etc.",
                        "enum": ["people", "deals", "tasks", "events", "calls", "notes", "appointments"]
                    }
                },
                "required": ["endpoint"]
            }
        ),
        
        # Main powerful tool
        Tool(
            name="execute_custom_query",
            description=(
                "⭐ The ultimate reporting tool. Fetch data from multiple FUB API endpoints "
                "and process it with Python to create ANY report imaginable. Returns EXACT "
                "numbers, not approximations. Includes powerful utilities: groupBy, countBy, "
                "sumBy, unique, aggregate, and more. Handles massive datasets intelligently "
                "with progress tracking and automatic pagination."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Human-readable description of what this query does"
                    },
                    "endpoints": {
                        "type": "array",
                        "description": "List of endpoints to fetch data from",
                        "items": {
                            "type": "object",
                            "properties": {
                                "endpoint": {
                                    "type": "string",
                                    "description": "API endpoint path (e.g., /people, /calls)"
                                },
                                "params": {
                                    "type": "object",
                                    "description": "Query parameters for this endpoint",
                                    "default": {}
                                },
                                "dateField": {
                                    "type": "string",
                                    "description": "Field to filter by date if needed"
                                }
                            },
                            "required": ["endpoint"]
                        }
                    },
                    "dateRange": {
                        "type": "object",
                        "description": "Optional date range filter",
                        "properties": {
                            "start": {
                                "type": "string",
                                "description": "Start date (ISO format)"
                            },
                            "end": {
                                "type": "string",
                                "description": "End date (ISO format)"
                            }
                        }
                    },
                    "processing": {
                        "type": "string",
                        "description": (
                            "Optional Python code to process the fetched data. "
                            "Will receive a 'data' dict with keys matching endpoint names. "
                            "Available utilities: utils.groupBy, utils.countBy, utils.sumBy, "
                            "utils.unique, utils.aggregate, utils.dateRange. "
                            "Return the processed result."
                        ),
                        "default": "return data"
                    }
                },
                "required": ["description", "endpoints"]
            }
        ),
        
        # PEOPLE ENDPOINTS
        Tool(
            name="get_people",
            description=(
                "Get a list of people/contacts from Follow Up Boss. Supports filtering by stage, source, "
                "user assignment, and SMART DATE FILTERING. "
                "Examples: created='last 7 days', created='this month', created='older than 30 days'. "
                "Set includeCustomFields=true to get custom field values (recommended!)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Number of results (max 100)",
                        "default": 20
                    },
                    "offset": {
                        "type": "number",
                        "description": "Number of results to skip",
                        "default": 0
                    },
                    "search": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "sort": {
                        "type": "string",
                        "description": "Sort field (e.g., '-created' for newest first, 'name' for alphabetical)",
                        "default": "-created"
                    },
                    "stageId": {
                        "type": "number",
                        "description": "Filter by stage ID (use get_stages to find stage IDs)"
                    },
                    "assignedUserId": {
                        "type": "number",
                        "description": "Filter by assigned user ID"
                    },
                    "sourceId": {
                        "type": "number",
                        "description": "Filter by source ID"
                    },
                    "tags": {
                        "type": "string",
                        "description": "Filter by tags (comma-separated)"
                    },
                    "created": {
                        "type": "string",
                        "description": (
                            "SMART DATE FILTER: 'last 7 days', 'last 30 days', 'this week', 'this month', "
                            "'older than 30 days', 'today', 'yesterday', '>2024-01-01', '<2024-12-31'"
                        )
                    },
                    "updated": {
                        "type": "string",
                        "description": (
                            "SMART DATE FILTER: Same as created. Filter by last update time."
                        )
                    },
                    "createdInLast": {
                        "type": "string",
                        "description": "Convenience: '7 days', '30 days', '1 week' (automatically converted to created filter)"
                    },
                    "updatedInLast": {
                        "type": "string",
                        "description": "Convenience: '7 days', '30 days', '1 week' (automatically converted to updated filter)"
                    },
                    "includeCustomFields": {
                        "type": "boolean",
                        "description": "Include custom field values in response (default: true). Uses fields=allFields parameter.",
                        "default": True
                    }
                }
            }
        ),
        Tool(
            name="get_person",
            description="Get details of a specific person by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "personId": {
                        "type": "string",
                        "description": "Person ID"
                    }
                },
                "required": ["personId"]
            }
        ),
        Tool(
            name="search_people",
            description="Search for people by name, email, or phone",
            inputSchema={
                "type": "object",
                "properties": {
                    "q": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of results",
                        "default": 20
                    }
                },
                "required": ["q"]
            }
        ),
        Tool(
            name="check_duplicates",
            description=(
                "Check for duplicate contacts in Follow Up Boss. "
                "Uses FUB's deduplication rules: "
                "1) Email address match, or "
                "2) Phone number AND both first and last name match. "
                "Returns potential duplicates with match reasons and confidence levels."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "Email address to check for duplicates"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Phone number to check for duplicates"
                    },
                    "firstName": {
                        "type": "string",
                        "description": "First name (required if checking phone duplicates)"
                    },
                    "lastName": {
                        "type": "string",
                        "description": "Last name (required if checking phone duplicates)"
                    },
                    "searchLimit": {
                        "type": "number",
                        "description": "Maximum number of contacts to search (default: 500). Higher values give more thorough checks but are slower.",
                        "default": 500
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="create_person",
            description="Create a new person/contact in Follow Up Boss",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Full name of the person"
                    },
                    "firstName": {
                        "type": "string",
                        "description": "First name"
                    },
                    "lastName": {
                        "type": "string",
                        "description": "Last name"
                    },
                    "emails": {
                        "type": "array",
                        "description": "List of email addresses",
                        "items": {
                            "type": "object",
                            "properties": {
                                "value": {"type": "string"},
                                "type": {"type": "string", "description": "home, work, other"},
                                "isPrimary": {"type": "number", "description": "1 for primary, 0 for not"}
                            }
                        }
                    },
                    "phones": {
                        "type": "array",
                        "description": "List of phone numbers",
                        "items": {
                            "type": "object",
                            "properties": {
                                "value": {"type": "string"},
                                "type": {"type": "string", "description": "mobile, home, work, other"},
                                "isPrimary": {"type": "number", "description": "1 for primary, 0 for not"}
                            }
                        }
                    },
                    "source": {
                        "type": "string",
                        "description": "Lead source"
                    },
                    "assignedUserId": {
                        "type": "string",
                        "description": "User ID to assign the person to"
                    },
                    "stageId": {
                        "type": "number",
                        "description": "Stage ID"
                    },
                    "customFields": {
                        "type": "object",
                        "description": "Custom field values keyed by custom field name"
                    },
                    "tags": {
                        "type": "array",
                        "description": "List of tags",
                        "items": {"type": "string"}
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="update_person",
            description="Update an existing person/contact",
            inputSchema={
                "type": "object",
                "properties": {
                    "personId": {
                        "type": "string",
                        "description": "Person ID to update"
                    },
                    "name": {
                        "type": "string",
                        "description": "Full name of the person"
                    },
                    "firstName": {
                        "type": "string",
                        "description": "First name"
                    },
                    "lastName": {
                        "type": "string",
                        "description": "Last name"
                    },
                    "emails": {
                        "type": "array",
                        "description": "List of email addresses",
                        "items": {
                            "type": "object",
                            "properties": {
                                "value": {"type": "string"},
                                "type": {"type": "string"},
                                "isPrimary": {"type": "number"}
                            }
                        }
                    },
                    "phones": {
                        "type": "array",
                        "description": "List of phone numbers",
                        "items": {
                            "type": "object",
                            "properties": {
                                "value": {"type": "string"},
                                "type": {"type": "string"},
                                "isPrimary": {"type": "number"}
                            }
                        }
                    },
                    "source": {
                        "type": "string",
                        "description": "Lead source"
                    },
                    "assignedUserId": {
                        "type": "string",
                        "description": "User ID to assign the person to"
                    },
                    "stageId": {
                        "type": "number",
                        "description": "Stage ID"
                    },
                    "customFields": {
                        "type": "object",
                        "description": "Custom field values to update, keyed by custom field name"
                    },
                    "tags": {
                        "type": "array",
                        "description": "List of tags",
                        "items": {"type": "string"}
                    }
                },
                "required": ["personId"]
            }
        ),
        Tool(
            name="delete_person",
            description="Delete a person/contact from Follow Up Boss (permanent action)",
            inputSchema={
                "type": "object",
                "properties": {
                    "personId": {
                        "type": "string",
                        "description": "Person ID to delete"
                    }
                },
                "required": ["personId"]
            }
        ),
        Tool(
            name="batch_update_people",
            description=(
                "Update multiple contacts at once (up to 100). Much faster than individual updates. "
                "Returns success/failure status for each update with detailed error messages."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "updates": {
                        "type": "array",
                        "description": "List of update objects, each containing personId and fields to update",
                        "items": {
                            "type": "object",
                            "properties": {
                                "personId": {
                                    "type": "string",
                                    "description": "Person ID to update"
                                },
                                "data": {
                                    "type": "object",
                                    "description": "Fields to update (same as update_person)",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "firstName": {"type": "string"},
                                        "lastName": {"type": "string"},
                                        "stageId": {"type": "number"},
                                        "assignedUserId": {"type": "string"},
                                        "tags": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        },
                                        "customFields": {"type": "object"}
                                    }
                                }
                            },
                            "required": ["personId", "data"]
                        }
                    },
                    "stopOnError": {
                        "type": "boolean",
                        "description": "Stop processing if an error occurs (default: false)",
                        "default": False
                    }
                },
                "required": ["updates"]
            }
        ),
        
        # CALLS ENDPOINTS
        Tool(
            name="get_calls",
            description="Get a list of phone calls",
            inputSchema={
                "type": "object",
                "properties": {
                    "personId": {
                        "type": "string",
                        "description": "Filter by person ID"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of results (max 100)",
                        "default": 20
                    },
                    "offset": {
                        "type": "number",
                        "description": "Number of results to skip",
                        "default": 0
                    }
                }
            }
        ),
        Tool(
            name="get_call",
            description="Get details of a specific call by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "callId": {
                        "type": "string",
                        "description": "Call ID"
                    }
                },
                "required": ["callId"]
            }
        ),
        
        # EVENTS ENDPOINTS
        Tool(
            name="get_events",
            description="Get a list of events/activities",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Number of results (max 100)",
                        "default": 20
                    },
                    "offset": {
                        "type": "number",
                        "description": "Number of results to skip",
                        "default": 0
                    },
                    "personId": {
                        "type": "string",
                        "description": "Filter by person ID"
                    },
                    "type": {
                        "type": "string",
                        "description": "Filter by event type"
                    }
                }
            }
        ),
        Tool(
            name="get_event",
            description="Get details of a specific event by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "eventId": {
                        "type": "string",
                        "description": "Event ID"
                    }
                },
                "required": ["eventId"]
            }
        ),
        
        # DEALS ENDPOINTS
        Tool(
            name="get_deals",
            description="Get a list of deals",
            inputSchema={
                "type": "object",
                "properties": {
                    "personId": {
                        "type": "string",
                        "description": "Filter by person ID"
                    },
                    "pipelineId": {
                        "type": "string",
                        "description": "Filter by pipeline ID"
                    },
                    "stageId": {
                        "type": "string",
                        "description": "Filter by stage ID"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of results (max 100)",
                        "default": 20
                    },
                    "offset": {
                        "type": "number",
                        "description": "Number of results to skip",
                        "default": 0
                    }
                }
            }
        ),
        Tool(
            name="get_deal",
            description="Get details of a specific deal by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "dealId": {
                        "type": "string",
                        "description": "Deal ID"
                    }
                },
                "required": ["dealId"]
            }
        ),
        
        # TASKS ENDPOINTS
        Tool(
            name="get_tasks",
            description="Get a list of tasks",
            inputSchema={
                "type": "object",
                "properties": {
                    "personId": {
                        "type": "string",
                        "description": "Filter by person ID"
                    },
                    "assignedTo": {
                        "type": "string",
                        "description": "Filter by assigned user ID"
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by status (e.g., 'pending', 'completed')"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of results (max 100)",
                        "default": 20
                    },
                    "offset": {
                        "type": "number",
                        "description": "Number of results to skip",
                        "default": 0
                    }
                }
            }
        ),
        Tool(
            name="get_task",
            description="Get details of a specific task by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "taskId": {
                        "type": "string",
                        "description": "Task ID"
                    }
                },
                "required": ["taskId"]
            }
        ),
        
        # USERS ENDPOINTS
        Tool(
            name="get_users",
            description="Get a list of users/team members",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Number of results",
                        "default": 20
                    }
                }
            }
        ),
        Tool(
            name="get_user",
            description="Get details of a specific user by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "userId": {
                        "type": "string",
                        "description": "User ID"
                    }
                },
                "required": ["userId"]
            }
        ),
        Tool(
            name="get_me",
            description="Get current user information",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        # NOTES ENDPOINTS
        Tool(
            name="get_notes",
            description="Get a list of notes",
            inputSchema={
                "type": "object",
                "properties": {
                    "personId": {
                        "type": "string",
                        "description": "Filter by person ID"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of results (max 100)",
                        "default": 20
                    },
                    "offset": {
                        "type": "number",
                        "description": "Number of results to skip",
                        "default": 0
                    }
                }
            }
        ),
        Tool(
            name="get_note",
            description="Get details of a specific note by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "noteId": {
                        "type": "string",
                        "description": "Note ID"
                    }
                },
                "required": ["noteId"]
            }
        ),
        
        # APPOINTMENTS ENDPOINTS
        Tool(
            name="get_appointments",
            description="Get a list of appointments",
            inputSchema={
                "type": "object",
                "properties": {
                    "personId": {
                        "type": "string",
                        "description": "Filter by person ID"
                    },
                    "startDate": {
                        "type": "string",
                        "description": "Start date filter (ISO format)"
                    },
                    "endDate": {
                        "type": "string",
                        "description": "End date filter (ISO format)"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of results (max 100)",
                        "default": 20
                    },
                    "offset": {
                        "type": "number",
                        "description": "Number of results to skip",
                        "default": 0
                    }
                }
            }
        ),
        Tool(
            name="get_appointment",
            description="Get details of a specific appointment by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "appointmentId": {
                        "type": "string",
                        "description": "Appointment ID"
                    }
                },
                "required": ["appointmentId"]
            }
        ),
        
        # PIPELINES & STAGES
        Tool(
            name="get_pipelines",
            description="Get all pipelines",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_pipeline",
            description="Get details of a specific pipeline by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "pipelineId": {
                        "type": "string",
                        "description": "Pipeline ID"
                    }
                },
                "required": ["pipelineId"]
            }
        ),
        Tool(
            name="get_stages",
            description="Get all stages",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_stage",
            description="Get details of a specific stage by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "stageId": {
                        "type": "string",
                        "description": "Stage ID"
                    }
                },
                "required": ["stageId"]
            }
        ),
        
        # CUSTOM FIELDS ENDPOINTS
        Tool(
            name="get_custom_fields",
            description="Get all custom fields available in Follow Up Boss",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_custom_field",
            description="Get details of a specific custom field by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "customFieldId": {
                        "type": "string",
                        "description": "Custom field ID"
                    }
                },
                "required": ["customFieldId"]
            }
        ),
        Tool(
            name="create_custom_field",
            description="Create a new custom field in Follow Up Boss. The internal 'name' is auto-generated from the label.",
            inputSchema={
                "type": "object",
                "properties": {
                    "label": {
                        "type": "string",
                        "description": "Display label for the field (e.g., 'UUID'). This will be used to generate the internal field name."
                    },
                    "type": {
                        "type": "string",
                        "description": "Field type: 'text', 'number', 'date', 'select', 'checkbox', 'textarea'",
                        "enum": ["text", "number", "date", "select", "checkbox", "textarea"]
                    },
                    "orderWeight": {
                        "type": "integer",
                        "description": "Order/position weight (optional)"
                    },
                    "hideIfEmpty": {
                        "type": "boolean",
                        "description": "Hide field if empty (optional, default: false)"
                    },
                    "readOnly": {
                        "type": "boolean",
                        "description": "Make field read-only (optional, default: false)"
                    },
                    "options": {
                        "type": "array",
                        "description": "Options for 'select' type fields (optional)",
                        "items": {"type": "string"}
                    }
                },
                "required": ["label", "type"]
            }
        ),
        Tool(
            name="update_custom_field",
            description="Update an existing custom field",
            inputSchema={
                "type": "object",
                "properties": {
                    "customFieldId": {
                        "type": "string",
                        "description": "Custom field ID to update"
                    },
                    "label": {
                        "type": "string",
                        "description": "Updated display label"
                    },
                    "type": {
                        "type": "string",
                        "description": "Field type"
                    },
                    "orderWeight": {
                        "type": "integer",
                        "description": "Order/position weight"
                    },
                    "hideIfEmpty": {
                        "type": "boolean",
                        "description": "Hide field if empty"
                    },
                    "readOnly": {
                        "type": "boolean",
                        "description": "Make field read-only"
                    },
                    "options": {
                        "type": "array",
                        "description": "Options for 'select' type fields",
                        "items": {"type": "string"}
                    }
                },
                "required": ["customFieldId"]
            }
        ),
        Tool(
            name="delete_custom_field",
            description="Delete a custom field from Follow Up Boss (permanent action)",
            inputSchema={
                "type": "object",
                "properties": {
                    "customFieldId": {
                        "type": "string",
                        "description": "Custom field ID to delete"
                    }
                },
                "required": ["customFieldId"]
            }
        ),
    ]

