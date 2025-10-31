"""Follow Up Boss API client."""

import asyncio
from typing import Any, Dict, List, Optional
import httpx
from .config import Config
from .cache import get_cache_manager


class FUBClient:
    """Async client for Follow Up Boss API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize FUB API client.
        
        Args:
            api_key: FUB API key. If not provided, uses Config.FUB_API_KEY
        """
        self.api_key = api_key or Config.FUB_API_KEY
        self.base_url = Config.FUB_API_BASE
        self.headers = Config.get_headers()
        
        self._client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            auth=(self.api_key, ""),
            headers=self.headers,
            timeout=30.0,
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if not self._client:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                auth=(self.api_key, ""),
                headers=self.headers,
                timeout=30.0,
            )
        return self._client
    
    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make an API request with rate limiting and header checking.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            json_data: JSON body data (for POST/PUT)
            **kwargs: Additional arguments for httpx request
            
        Returns:
            Response data as dictionary
        """
        client = await self._get_client()
        
        # Rate limiting - base delay between requests
        await asyncio.sleep(Config.RATE_LIMIT_DELAY_MS / 1000.0)
        
        # Prepare request kwargs
        request_kwargs = {"params": params, **kwargs}
        if json_data:
            request_kwargs["json"] = json_data
        
        # Check cache for GET requests
        cache_manager = get_cache_manager(
            max_size=Config.CACHE_MAX_SIZE,
            enabled=Config.ENABLE_CACHING
        )
        
        if method == "GET" and cache_manager.enabled:
            cached_data = cache_manager.get(endpoint, params)
            if cached_data is not None:
                # Return cached data without making API call
                return cached_data
        
        response = await client.request(
            method,
            endpoint,
            **request_kwargs
        )
        
        # Check rate limit headers and respect them
        rate_limit_remaining = response.headers.get("X-RateLimit-Remaining")
        rate_limit_reset = response.headers.get("X-RateLimit-Reset")
        
        if rate_limit_remaining:
            try:
                remaining = int(rate_limit_remaining)
                # If we're getting close to the limit (less than 10 remaining), wait longer
                if remaining < 10:
                    # Wait a bit longer to avoid hitting the limit
                    await asyncio.sleep(0.2)
                elif remaining < 50:
                    # Moderate slowdown
                    await asyncio.sleep(0.1)
            except (ValueError, TypeError):
                pass
        
        # Handle 429 Too Many Requests
        if response.status_code == 429:
            # Wait a bit and potentially retry (for now, just raise)
            wait_time = 2.0
            if rate_limit_reset:
                try:
                    # If we have reset time, we could calculate wait, but for now just wait
                    pass
                except (ValueError, TypeError):
                    pass
            await asyncio.sleep(wait_time)
            raise httpx.HTTPStatusError(
                message=f"429 Rate Limit Exceeded. Please wait before retrying.",
                request=response.request,
                response=response
            )
        
        # Get error details before raising
        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = f"{response.status_code} Bad Request: {error_data}"
            except:
                error_msg = f"{response.status_code} Bad Request"
            raise httpx.HTTPStatusError(
                message=error_msg,
                request=response.request,
                response=response
            )
        
        # Parse response
        response_data = response.json()
        
        # Cache successful GET responses
        if method == "GET" and response.status_code == 200 and cache_manager.enabled:
            cache_manager.set(endpoint, response_data, params=params)
        
        return response_data
    
    async def get(
        self,
        endpoint: str,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        GET request to API.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            Response data
        """
        return await self._request("GET", endpoint, params=params)
    
    async def post(
        self,
        endpoint: str,
        json_data: Dict[str, Any],
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        POST request to API.
        
        Args:
            endpoint: API endpoint
            json_data: JSON body data
            params: Query parameters
            
        Returns:
            Response data
        """
        return await self._request("POST", endpoint, params=params, json_data=json_data)
    
    async def put(
        self,
        endpoint: str,
        json_data: Dict[str, Any],
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        PUT request to API.
        
        Args:
            endpoint: API endpoint
            json_data: JSON body data
            params: Query parameters
            
        Returns:
            Response data
        """
        return await self._request("PUT", endpoint, params=params, json_data=json_data)
    
    async def delete(
        self,
        endpoint: str,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        DELETE request to API.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            Response data
        """
        return await self._request("DELETE", endpoint, params=params)
    
    async def fetch_all_pages(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        date_field: Optional[str] = None,
        date_range: Optional[Dict[str, str]] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Fetch all pages from a paginated endpoint.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            date_field: Field to filter by date
            date_range: Optional date range filter {"start": "...", "end": "..."}
            limit: Page size (max 100)
            
        Returns:
            List of all items across all pages
        """
        all_data: List[Dict[str, Any]] = []
        offset = 0
        has_more = True
        total_fetched = 0
        
        # Parse date range if provided
        start_date = None
        end_date = None
        if date_range and date_field:
            from datetime import datetime
            try:
                start_date = datetime.fromisoformat(date_range["start"].replace("Z", "+00:00"))
                end_date = datetime.fromisoformat(date_range["end"].replace("Z", "+00:00"))
            except (ValueError, KeyError):
                pass
        
        while has_more:
            try:
                # Prepare params with pagination
                page_params = {**(params or {}), "limit": limit, "offset": offset}
                
                response = await self.get(endpoint, params=page_params)
                
                # Extract items from response
                # Response format: {"endpointName": [...], "_metadata": {...}}
                items_key = None
                for key in response.keys():
                    if key != "_metadata" and isinstance(response[key], list):
                        items_key = key
                        break
                
                if not items_key:
                    break
                
                items = response[items_key]
                
                # Filter by date if needed
                filtered_items = items
                if date_field and start_date and end_date:
                    from .processors import DataProcessors
                    filtered_items = DataProcessors.filter_by_date_range(
                        items,
                        date_field,
                        start_date,
                        end_date
                    )
                    
                    # If no items match and we're past the date range, stop
                    if not filtered_items and items:
                        last_item_date_str = items[-1].get(date_field)
                        if last_item_date_str:
                            try:
                                from datetime import datetime
                                last_date = datetime.fromisoformat(
                                    last_item_date_str.replace("Z", "+00:00")
                                )
                                if last_date < start_date:
                                    has_more = False
                            except (ValueError, TypeError):
                                pass
                
                all_data.extend(filtered_items)
                total_fetched += len(items)
                
                # Check metadata for pagination
                metadata = response.get("_metadata")
                if metadata:
                    total = metadata.get("total", 0)
                    offset += limit
                    has_more = offset < total
                else:
                    has_more = False
                
                # If we got fewer items than limit, we're done
                if len(items) < limit:
                    has_more = False
                    
            except Exception as e:
                # Log error but don't break - return what we have
                print(f"Error fetching {endpoint}: {e}")
                has_more = False
        
        return all_data
    
    async def get_people(self, **params) -> Dict[str, Any]:
        """Get people/contacts."""
        return await self.get("/people", params=params)
    
    async def get_person(self, person_id: str) -> Dict[str, Any]:
        """Get a specific person."""
        return await self.get(f"/people/{person_id}")
    
    async def get_calls(self, **params) -> Dict[str, Any]:
        """Get calls."""
        return await self.get("/calls", params=params)
    
    async def get_events(self, **params) -> Dict[str, Any]:
        """Get events."""
        return await self.get("/events", params=params)
    
    async def get_deals(self, **params) -> Dict[str, Any]:
        """Get deals."""
        return await self.get("/deals", params=params)
    
    async def get_tasks(self, **params) -> Dict[str, Any]:
        """Get tasks."""
        return await self.get("/tasks", params=params)
    
    async def get_users(self, **params) -> Dict[str, Any]:
        """Get users."""
        return await self.get("/users", params=params)
    
    async def get_me(self) -> Dict[str, Any]:
        """Get current user."""
        return await self.get("/me")
    
    # CRUD Operations for People
    
    async def create_person(self, person_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new person/contact.
        
        Args:
            person_data: Person data (name, email, phone, customFields, etc.)
            
        Returns:
            Created person data
        """
        return await self.post("/people", json_data=person_data)
    
    async def update_person(self, person_id: str, person_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing person/contact.
        
        Args:
            person_id: Person ID
            person_data: Updated person data
            
        Returns:
            Updated person data
        """
        return await self.put(f"/people/{person_id}", json_data=person_data)
    
    async def delete_person(self, person_id: str) -> Dict[str, Any]:
        """
        Delete a person/contact.
        
        Args:
            person_id: Person ID
            
        Returns:
            Deletion confirmation
        """
        return await self.delete(f"/people/{person_id}")
    
    # Custom Fields Operations
    
    async def get_custom_fields(self) -> Dict[str, Any]:
        """Get all custom fields."""
        return await self.get("/customFields")
    
    async def get_custom_field(self, custom_field_id: str) -> Dict[str, Any]:
        """Get a specific custom field by ID."""
        return await self.get(f"/customFields/{custom_field_id}")

    async def create_custom_field(self, custom_field_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new custom field.

        Args:
            custom_field_data: Custom field data (name, label, type, etc.)

        Returns:
            Created custom field data
        """
        return await self.post("/customFields", json_data=custom_field_data)

    async def update_custom_field(self, custom_field_id: str, custom_field_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing custom field.

        Args:
            custom_field_id: Custom field ID
            custom_field_data: Updated custom field data

        Returns:
            Updated custom field data
        """
        return await self.put(f"/customFields/{custom_field_id}", json_data=custom_field_data)

    async def delete_custom_field(self, custom_field_id: str) -> Dict[str, Any]:
        """
        Delete a custom field.

        Args:
            custom_field_id: Custom field ID

        Returns:
            Deletion confirmation
        """
        return await self.delete(f"/customFields/{custom_field_id}")

