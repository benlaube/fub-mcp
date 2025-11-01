"""Smart date filtering utilities for FUB queries."""

from datetime import datetime, timedelta
from typing import Dict, Optional, Any


class DateFilters:
    """Helper class for smart date filtering."""
    
    @staticmethod
    def parse_relative_date(relative_expr: str) -> datetime:
        """
        Parse relative date expressions into datetime objects.
        
        Args:
            relative_expr: Relative date expression like:
                - "7 days ago"
                - "30 days"
                - "1 week ago"
                - "2 months ago"
                - "1 year ago"
                
        Returns:
            datetime object
        """
        now = datetime.now()
        expr = relative_expr.lower().strip()
        
        # Remove "ago" if present
        expr = expr.replace(" ago", "").strip()
        
        # Parse number and unit
        parts = expr.split()
        if len(parts) != 2:
            raise ValueError(f"Invalid relative date format: {relative_expr}")
        
        try:
            amount = int(parts[0])
            unit = parts[1].rstrip('s')  # Remove plural 's'
        except ValueError:
            raise ValueError(f"Invalid number in date expression: {parts[0]}")
        
        # Calculate timedelta
        if unit in ['day', 'days']:
            delta = timedelta(days=amount)
        elif unit in ['week', 'weeks']:
            delta = timedelta(weeks=amount)
        elif unit in ['month', 'months']:
            delta = timedelta(days=amount * 30)  # Approximate
        elif unit in ['year', 'years']:
            delta = timedelta(days=amount * 365)  # Approximate
        elif unit in ['hour', 'hours']:
            delta = timedelta(hours=amount)
        elif unit in ['minute', 'minutes']:
            delta = timedelta(minutes=amount)
        else:
            raise ValueError(f"Unknown time unit: {unit}")
        
        return now - delta
    
    @staticmethod
    def parse_smart_date_filter(filter_value: Any) -> str:
        """
        Parse smart date filter expressions into FUB API format.
        
        Supports:
        - "last 7 days" → ">YYYY-MM-DD"
        - "older than 30 days" → "<YYYY-MM-DD"
        - "this week" → date range
        - "this month" → date range
        - "today" → today's date
        - "yesterday" → yesterday's date
        
        Args:
            filter_value: Smart date expression or raw date
            
        Returns:
            FUB API compatible date filter string
        """
        if not isinstance(filter_value, str):
            return str(filter_value)
        
        value = filter_value.lower().strip()
        now = datetime.now()
        
        # Handle "today"
        if value == "today":
            return now.strftime(">%Y-%m-%d")
        
        # Handle "yesterday"
        if value == "yesterday":
            yesterday = now - timedelta(days=1)
            return yesterday.strftime("%Y-%m-%d")
        
        # Handle "last X days/weeks/months"
        if value.startswith("last "):
            expr = value.replace("last ", "")
            date = DateFilters.parse_relative_date(expr)
            return date.strftime(">%Y-%m-%d")
        
        # Handle "older than X days/weeks/months"
        if value.startswith("older than "):
            expr = value.replace("older than ", "")
            date = DateFilters.parse_relative_date(expr)
            return date.strftime("<%Y-%m-%d")
        
        # Handle "this week"
        if value == "this week":
            start_of_week = now - timedelta(days=now.weekday())
            return start_of_week.strftime(">%Y-%m-%d")
        
        # Handle "this month"
        if value == "this month":
            start_of_month = now.replace(day=1)
            return start_of_month.strftime(">%Y-%m-%d")
        
        # Handle "this year"
        if value == "this year":
            start_of_year = now.replace(month=1, day=1)
            return start_of_year.strftime(">%Y-%m-%d")
        
        # Handle "in last X days" (alternative syntax)
        if value.startswith("in last "):
            expr = value.replace("in last ", "")
            date = DateFilters.parse_relative_date(expr)
            return date.strftime(">%Y-%m-%d")
        
        # If it's already in a valid format, return as-is
        return filter_value
    
    @staticmethod
    def convert_filters(arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert smart date filters in arguments to FUB API format.
        
        Args:
            arguments: Tool arguments that may contain smart date filters
            
        Returns:
            Modified arguments with converted date filters
        """
        converted = arguments.copy()
        
        # Known date fields
        date_fields = ['created', 'updated', 'createdAfter', 'createdBefore', 
                      'updatedAfter', 'updatedBefore']
        
        for field in date_fields:
            if field in converted:
                try:
                    converted[field] = DateFilters.parse_smart_date_filter(converted[field])
                except Exception as e:
                    # If parsing fails, leave as-is
                    pass
        
        # Handle special convenience fields
        if 'createdInLast' in converted:
            try:
                date_str = DateFilters.parse_smart_date_filter(f"last {converted['createdInLast']}")
                converted['created'] = date_str
                del converted['createdInLast']
            except Exception:
                pass
        
        if 'updatedInLast' in converted:
            try:
                date_str = DateFilters.parse_smart_date_filter(f"last {converted['updatedInLast']}")
                converted['updated'] = date_str
                del converted['updatedInLast']
            except Exception:
                pass
        
        if 'createdOlderThan' in converted:
            try:
                date_str = DateFilters.parse_smart_date_filter(f"older than {converted['createdOlderThan']}")
                converted['created'] = date_str
                del converted['createdOlderThan']
            except Exception:
                pass
        
        if 'updatedOlderThan' in converted:
            try:
                date_str = DateFilters.parse_smart_date_filter(f"older than {converted['updatedOlderThan']}")
                converted['updated'] = date_str
                del converted['updatedOlderThan']
            except Exception:
                pass
        
        return converted
    
    @staticmethod
    def get_examples() -> Dict[str, str]:
        """
        Get examples of smart date filters.
        
        Returns:
            Dictionary of example filters and their descriptions
        """
        return {
            "last 7 days": "Contacts created in the last 7 days",
            "last 30 days": "Contacts created in the last 30 days",
            "last 1 week": "Contacts created in the last week",
            "last 3 months": "Contacts created in the last 3 months",
            "older than 30 days": "Contacts created more than 30 days ago",
            "older than 1 year": "Contacts created more than a year ago",
            "today": "Contacts created today",
            "yesterday": "Contacts created yesterday",
            "this week": "Contacts created this week",
            "this month": "Contacts created this month",
            "this year": "Contacts created this year",
            ">2024-01-01": "Contacts created after Jan 1, 2024",
            "<2024-12-31": "Contacts created before Dec 31, 2024",
            "2024-10-31": "Contacts created on Oct 31, 2024"
        }

