"""Dynamic discovery system for FUB data sources."""

from typing import Any, Dict, List, Optional
import re


class DataDiscovery:
    """Handles dynamic discovery of data locations in FUB."""
    
    # Define FUB data structure
    ENDPOINTS = {
        "people": {
            "name": "people",
            "description": "Contacts/leads - people in your database",
            "type": "endpoint",
            "keywords": ["contact", "lead", "person", "client", "prospect", "customer"],
            "filters": ["stageId", "assignedUserId", "sourceId", "tags", "search"],
            "examples": [
                "Get contacts in a specific stage",
                "Find people assigned to a user",
                "Search contacts by name, email, or phone"
            ]
        },
        "deals": {
            "name": "deals",
            "description": "Real estate deals and transactions",
            "type": "endpoint",
            "keywords": ["deal", "transaction", "sale", "listing", "contract"],
            "filters": ["personId", "pipelineId", "stageId"],
            "examples": [
                "Get deals for a specific person",
                "Find deals in a pipeline",
                "Filter deals by stage"
            ]
        },
        "tasks": {
            "name": "tasks",
            "description": "Tasks and to-dos assigned to team members",
            "type": "endpoint",
            "keywords": ["task", "todo", "action", "followup", "reminder"],
            "filters": ["personId", "assignedTo", "status"],
            "examples": [
                "Get tasks for a person",
                "Find tasks assigned to a user",
                "Filter by status (pending, completed)"
            ]
        },
        "events": {
            "name": "events",
            "description": "Activities and interactions (calls, emails, etc.)",
            "type": "endpoint",
            "keywords": ["event", "activity", "interaction", "history", "log"],
            "filters": ["personId", "type"],
            "examples": [
                "Get events for a person",
                "Filter by event type"
            ]
        },
        "calls": {
            "name": "calls",
            "description": "Phone call records",
            "type": "endpoint",
            "keywords": ["call", "phone", "conversation", "dial"],
            "filters": ["personId"],
            "examples": [
                "Get calls for a person",
                "View call history"
            ]
        },
        "notes": {
            "name": "notes",
            "description": "Notes and comments about contacts",
            "type": "endpoint",
            "keywords": ["note", "comment", "memo", "annotation"],
            "filters": ["personId"],
            "examples": [
                "Get notes for a person",
                "View all notes"
            ]
        },
        "appointments": {
            "name": "appointments",
            "description": "Scheduled appointments and meetings",
            "type": "endpoint",
            "keywords": ["appointment", "meeting", "showing", "schedule"],
            "filters": ["personId", "startDate", "endDate"],
            "examples": [
                "Get appointments for a person",
                "Filter by date range"
            ]
        }
    }
    
    @staticmethod
    def match_score(text: str, keywords: List[str]) -> int:
        """
        Calculate relevance score for text against keywords.
        
        Args:
            text: Text to search in
            keywords: List of keywords to search for
            
        Returns:
            Score (higher = more relevant)
        """
        normalized = text.lower()
        score = 0
        
        for keyword in keywords:
            kw_lower = keyword.lower()
            
            # Exact match (highest score)
            if normalized == kw_lower:
                score += 10
            # Word boundary match
            elif re.search(r'\b' + re.escape(kw_lower) + r'\b', normalized):
                score += 8
            # Contains match
            elif kw_lower in normalized:
                score += 5
            # Partial word match
            else:
                # Check if any words in the keyword partially match
                for word in kw_lower.split():
                    if len(word) > 3 and word in normalized:
                        score += 2
        
        return score
    
    @classmethod
    async def find_endpoints(
        cls,
        keywords: List[str],
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find endpoints matching keywords.
        
        Args:
            keywords: Search keywords
            limit: Maximum results
            
        Returns:
            List of matching endpoints with scores
        """
        results = []
        
        for endpoint_name, endpoint_data in cls.ENDPOINTS.items():
            # Search in name, description, and keywords
            search_text = (
                f"{endpoint_data['name']} "
                f"{endpoint_data['description']} "
                f"{' '.join(endpoint_data['keywords'])}"
            )
            
            score = cls.match_score(search_text, keywords)
            
            if score > 0:
                results.append({
                    "type": "endpoint",
                    "name": endpoint_name,
                    "description": endpoint_data["description"],
                    "path": f"/api/v1/{endpoint_name}",
                    "tool": f"get_{endpoint_name}",
                    "filters": endpoint_data["filters"],
                    "examples": endpoint_data["examples"],
                    "score": score
                })
        
        # Sort by score and limit
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]
    
    @classmethod
    async def find_stages(
        cls,
        fub_client,
        keywords: List[str],
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find stages matching keywords.
        
        Args:
            fub_client: FUB API client
            keywords: Search keywords
            limit: Maximum results
            
        Returns:
            List of matching stages with scores
        """
        results = []
        
        # Fetch stages from API
        try:
            response = await fub_client.get("/stages")
            stages = response.get("stages", [])
            
            for stage in stages:
                stage_name = stage.get("name", "")
                stage_id = stage.get("id")
                
                # Search in stage name
                score = cls.match_score(stage_name, keywords)
                
                if score > 0:
                    results.append({
                        "type": "stage",
                        "name": stage_name,
                        "id": stage_id,
                        "description": f"Stage: {stage_name}",
                        "usage": f"Use stageId={stage_id} in get_people or get_deals",
                        "example": f"get_people(stageId={stage_id}, limit=10)",
                        "score": score
                    })
        except Exception as e:
            # If stages fetch fails, return empty
            pass
        
        # Sort by score and limit
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]
    
    @classmethod
    async def find_custom_fields(
        cls,
        fub_client,
        keywords: List[str],
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find custom fields matching keywords.
        
        Args:
            fub_client: FUB API client
            keywords: Search keywords
            limit: Maximum results
            
        Returns:
            List of matching custom fields with scores
        """
        results = []
        
        # Fetch custom fields from API
        try:
            response = await fub_client.get("/customFields")
            fields = response.get("customFields", [])
            
            for field in fields:
                field_name = field.get("name", "")
                field_label = field.get("label", "")
                field_type = field.get("type", "")
                field_id = field.get("id")
                
                # Search in name and label
                search_text = f"{field_name} {field_label}"
                score = cls.match_score(search_text, keywords)
                
                if score > 0:
                    results.append({
                        "type": "custom_field",
                        "name": field_name,
                        "label": field_label,
                        "id": field_id,
                        "fieldType": field_type,
                        "description": f"Custom field: {field_label} ({field_type})",
                        "usage": f"Use in customFields when creating/updating people",
                        "example": f"create_person(customFields={{'{field_name}': 'value'}})",
                        "score": score
                    })
        except Exception as e:
            # If custom fields fetch fails, return empty
            pass
        
        # Sort by score and limit
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]
    
    @classmethod
    async def find_sources(
        cls,
        fub_client,
        keywords: List[str],
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find lead sources matching keywords.
        
        Args:
            fub_client: FUB API client
            keywords: Search keywords
            limit: Maximum results
            
        Returns:
            List of matching sources
        """
        results = []
        
        # Get sample people to extract sources
        try:
            response = await fub_client.get("/people", params={"limit": 100})
            people = response.get("people", [])
            
            # Extract unique sources
            sources_map = {}
            for person in people:
                source_name = person.get("source")
                source_id = person.get("sourceId")
                if source_name and source_id:
                    if source_id not in sources_map:
                        sources_map[source_id] = source_name
            
            # Score sources
            for source_id, source_name in sources_map.items():
                score = cls.match_score(source_name, keywords)
                
                if score > 0:
                    results.append({
                        "type": "source",
                        "name": source_name,
                        "id": source_id,
                        "description": f"Lead source: {source_name}",
                        "usage": f"Use sourceId={source_id} in get_people",
                        "example": f"get_people(sourceId={source_id}, limit=10)",
                        "score": score
                    })
        except Exception:
            pass
        
        # Sort by score and limit
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]
    
    @classmethod
    async def find_all(
        cls,
        fub_client,
        keywords: List[str],
        entity_type: str = "any",
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find all matching entities across all types.
        
        Args:
            fub_client: FUB API client
            keywords: Search keywords
            entity_type: Filter by type or 'any'
            limit: Maximum results
            
        Returns:
            Combined list of matches sorted by relevance
        """
        all_results = []
        
        # Search endpoints (always, they're static)
        if entity_type in ["any", "endpoint"]:
            endpoint_results = await cls.find_endpoints(keywords, limit=limit * 2)
            all_results.extend(endpoint_results)
        
        # Search stages
        if entity_type in ["any", "stage"]:
            stage_results = await cls.find_stages(fub_client, keywords, limit=limit * 2)
            all_results.extend(stage_results)
        
        # Search custom fields
        if entity_type in ["any", "field"]:
            field_results = await cls.find_custom_fields(fub_client, keywords, limit=limit * 2)
            all_results.extend(field_results)
        
        # Search sources
        if entity_type in ["any", "source"]:
            source_results = await cls.find_sources(fub_client, keywords, limit=limit * 2)
            all_results.extend(source_results)
        
        # Sort by score and limit
        all_results.sort(key=lambda x: x["score"], reverse=True)
        return all_results[:limit]
    
    @classmethod
    async def get_quick_reference(cls, fub_client) -> Dict[str, Any]:
        """
        Build quick reference guide on-demand.
        
        Args:
            fub_client: FUB API client
            
        Returns:
            Quick reference with common data locations
        """
        quick_ref = {
            "overview": {
                "description": "Common data locations in Follow Up Boss",
                "tip": "Use find_data_location for detailed search"
            },
            "endpoints": {
                "contacts": {
                    "tool": "get_people",
                    "description": "People/contacts/leads",
                    "filters": ["stageId", "assignedUserId", "sourceId", "tags"]
                },
                "deals": {
                    "tool": "get_deals",
                    "description": "Real estate transactions",
                    "filters": ["personId", "pipelineId", "stageId"]
                },
                "tasks": {
                    "tool": "get_tasks",
                    "description": "Tasks and to-dos",
                    "filters": ["personId", "assignedTo", "status"]
                },
                "activities": {
                    "tool": "get_events",
                    "description": "Activity history",
                    "filters": ["personId", "type"]
                }
            },
            "commonQueries": []
        }
        
        # Get stages
        try:
            stages_response = await fub_client.get("/stages")
            stages = stages_response.get("stages", [])
            
            stage_list = []
            for stage in stages[:10]:  # Top 10 stages
                stage_list.append({
                    "name": stage.get("name"),
                    "id": stage.get("id"),
                    "usage": f"stageId={stage.get('id')}"
                })
            
            quick_ref["stages"] = stage_list
            
            # Add common queries
            if stages:
                quick_ref["commonQueries"].append({
                    "query": f"Last 10 contacts in '{stages[0].get('name')}' stage",
                    "tool": "get_people",
                    "args": {
                        "stageId": stages[0].get("id"),
                        "sort": "-created",
                        "limit": 10
                    }
                })
        except Exception:
            pass
        
        # Get custom fields summary
        try:
            fields_response = await fub_client.get("/customFields")
            fields = fields_response.get("customFields", [])
            
            quick_ref["customFields"] = {
                "count": len(fields),
                "examples": [
                    {
                        "name": field.get("name"),
                        "label": field.get("label"),
                        "type": field.get("type")
                    }
                    for field in fields[:5]  # Top 5
                ],
                "tip": "Use find_data_location to search all custom fields"
            }
        except Exception:
            pass
        
        return quick_ref

