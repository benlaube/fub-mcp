"""Data processing utilities for FUB MCP Server."""

from typing import Any, Dict, List, Callable, Optional
from datetime import datetime


class DataProcessors:
    """Collection of data processing utility functions."""
    
    @staticmethod
    def group_by(data: List[Dict], key: str) -> Dict[str, List[Dict]]:
        """
        Group data by a key.
        
        Args:
            data: List of dictionaries
            key: Key to group by
            
        Returns:
            Dictionary mapping key values to lists of items
        """
        result: Dict[str, List[Dict]] = {}
        for item in data:
            group_key = str(item.get(key, "undefined"))
            if group_key not in result:
                result[group_key] = []
            result[group_key].append(item)
        return result
    
    @staticmethod
    def count_by(data: List[Dict], key: str) -> Dict[str, int]:
        """
        Count occurrences by key.
        
        Args:
            data: List of dictionaries
            key: Key to count by
            
        Returns:
            Dictionary mapping key values to counts
        """
        result: Dict[str, int] = {}
        for item in data:
            group_key = str(item.get(key, "undefined"))
            result[group_key] = result.get(group_key, 0) + 1
        return result
    
    @staticmethod
    def sum_by(data: List[Dict], key: str) -> float:
        """
        Sum values by key.
        
        Args:
            data: List of dictionaries
            key: Key whose values to sum
            
        Returns:
            Sum of all values
        """
        total = 0.0
        for item in data:
            value = item.get(key, 0)
            try:
                total += float(value)
            except (ValueError, TypeError):
                pass
        return total
    
    @staticmethod
    def unique(data: List[Dict], key: Optional[str] = None) -> List[Any]:
        """
        Get unique items or unique values by key.
        
        Args:
            data: List of dictionaries or items
            key: Optional key to extract unique values from
            
        Returns:
            List of unique items or values
        """
        seen = set()
        result = []
        
        for item in data:
            if key:
                value = item.get(key)
            else:
                value = item
            
            value_str = str(value)
            if value_str not in seen:
                seen.add(value_str)
                result.append(item if not key else value)
        
        return result
    
    @staticmethod
    def filter_by_date_range(
        data: List[Dict],
        date_field: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """
        Filter data by date range.
        
        Args:
            data: List of dictionaries
            date_field: Field name containing date
            start_date: Start of date range
            end_date: End of date range
            
        Returns:
            Filtered list of dictionaries
        """
        result = []
        for item in data:
            date_str = item.get(date_field)
            if not date_str:
                continue
            
            try:
                item_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                if start_date <= item_date <= end_date:
                    result.append(item)
            except (ValueError, TypeError):
                pass
        
        return result
    
    @staticmethod
    def date_range(start: str, end: str) -> Callable[[str], bool]:
        """
        Create a date range filter function.
        
        Args:
            start: Start date (ISO format)
            end: End date (ISO format)
            
        Returns:
            Function that checks if a date string is within range
        """
        start_date = datetime.fromisoformat(start.replace("Z", "+00:00"))
        end_date = datetime.fromisoformat(end.replace("Z", "+00:00"))
        
        def in_range(date_str: str) -> bool:
            try:
                item_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                return start_date <= item_date <= end_date
            except (ValueError, TypeError):
                return False
        
        return in_range
    
    @staticmethod
    def aggregate(data: List[Dict], group_by_key: str, aggregate_key: str, operation: str = "sum") -> Dict[str, float]:
        """
        Aggregate data grouped by a key.
        
        Args:
            data: List of dictionaries
            group_by_key: Key to group by
            aggregate_key: Key to aggregate
            operation: Operation to perform (sum, avg, count, min, max)
            
        Returns:
            Dictionary mapping group keys to aggregated values
        """
        grouped = DataProcessors.group_by(data, group_by_key)
        result: Dict[str, float] = {}
        
        for group_key, items in grouped.items():
            if operation == "sum":
                result[group_key] = DataProcessors.sum_by(items, aggregate_key)
            elif operation == "avg":
                total = DataProcessors.sum_by(items, aggregate_key)
                result[group_key] = total / len(items) if items else 0
            elif operation == "count":
                result[group_key] = float(len(items))
            elif operation == "min":
                values = [float(item.get(aggregate_key, 0)) for item in items]
                result[group_key] = min(values) if values else 0
            elif operation == "max":
                values = [float(item.get(aggregate_key, 0)) for item in items]
                result[group_key] = max(values) if values else 0
        
        return result

