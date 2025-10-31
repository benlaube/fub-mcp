"""Caching layer for FUB API responses to reduce API calls and improve performance."""

import time
from typing import Any, Dict, Optional, Tuple
from collections import OrderedDict
import hashlib
import json


class CacheEntry:
    """Represents a single cache entry."""
    
    def __init__(self, data: Any, ttl: float):
        """
        Initialize cache entry.
        
        Args:
            data: Cached data
            ttl: Time-to-live in seconds
        """
        self.data = data
        self.created_at = time.time()
        self.ttl = ttl
        self.expires_at = self.created_at + ttl
    
    def is_expired(self) -> bool:
        """Check if cache entry has expired."""
        return time.time() > self.expires_at
    
    def is_valid(self) -> bool:
        """Check if cache entry is still valid."""
        return not self.is_expired()


class LRUCache:
    """Least Recently Used (LRU) cache with TTL support."""
    
    def __init__(self, max_size: int = 1000):
        """
        Initialize LRU cache.
        
        Args:
            max_size: Maximum number of entries to cache
        """
        self.max_size = max_size
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
    
    def _generate_key(self, endpoint: str, params: Optional[Dict] = None) -> str:
        """
        Generate cache key from endpoint and parameters.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            Cache key string
        """
        # Sort params for consistent key generation
        sorted_params = json.dumps(params or {}, sort_keys=True)
        key_string = f"{endpoint}:{sorted_params}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Any]:
        """
        Get cached data if available and not expired.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            Cached data if available and valid, None otherwise
        """
        key = self._generate_key(endpoint, params)
        
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        
        # Check if expired
        if entry.is_expired():
            # Remove expired entry
            del self.cache[key]
            return None
        
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        
        return entry.data
    
    def set(self, endpoint: str, data: Any, ttl: float, params: Optional[Dict] = None) -> None:
        """
        Store data in cache.
        
        Args:
            endpoint: API endpoint
            data: Data to cache
            ttl: Time-to-live in seconds
            params: Query parameters
        """
        key = self._generate_key(endpoint, params)
        
        # Remove old entry if exists
        if key in self.cache:
            del self.cache[key]
        
        # Add new entry
        self.cache[key] = CacheEntry(data, ttl)
        self.cache.move_to_end(key)
        
        # Enforce max size
        if len(self.cache) > self.max_size:
            # Remove oldest entry (least recently used)
            self.cache.popitem(last=False)
    
    def invalidate(self, endpoint_pattern: str = None) -> int:
        """
        Invalidate cache entries matching a pattern.
        
        Args:
            endpoint_pattern: Pattern to match (e.g., "/people" invalidates all people queries)
                             If None, invalidates all entries
        
        Returns:
            Number of entries invalidated
        """
        if endpoint_pattern is None:
            # Invalidate all
            count = len(self.cache)
            self.cache.clear()
            return count
        
        # Invalidate matching entries
        keys_to_remove = [
            key for key in self.cache.keys()
            if endpoint_pattern in key
        ]
        
        for key in keys_to_remove:
            del self.cache[key]
        
        return len(keys_to_remove)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
    
    def size(self) -> int:
        """Get current cache size."""
        return len(self.cache)
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "entries": [
                {
                    "key": key,
                    "age_seconds": time.time() - entry.created_at,
                    "ttl_seconds": entry.ttl,
                    "expires_at": entry.expires_at
                }
                for key, entry in self.cache.items()
            ]
        }


class CacheManager:
    """Manages caching strategy for different types of FUB API data."""
    
    def __init__(self, max_size: int = 1000, enabled: bool = True):
        """
        Initialize cache manager.
        
        Args:
            max_size: Maximum cache size
            enabled: Whether caching is enabled
        """
        self.enabled = enabled
        self.cache = LRUCache(max_size=max_size)
        
        # TTL defaults by endpoint type (in seconds)
        self.ttl_config = {
            # Long-lived data (rarely changes)
            "/customFields": 300,  # 5 minutes - custom fields rarely change
            "/pipelines": 300,     # 5 minutes - pipelines rarely change
            "/stages": 300,        # 5 minutes - stages rarely change
            "/users": 300,         # 5 minutes - user list rarely changes
            
            # Medium-lived data (changes occasionally)
            "/people": 60,         # 1 minute - contacts change more frequently
            "/deals": 60,          # 1 minute
            "/tasks": 60,          # 1 minute
            
            # Short-lived data (changes frequently)
            "/calls": 30,          # 30 seconds - calls are frequently added
            "/events": 30,         # 30 seconds
            "/notes": 30,          # 30 seconds
            "/appointments": 30,   # 30 seconds
            
            # Default
            "default": 60,         # 1 minute default
        }
    
    def get_ttl(self, endpoint: str) -> float:
        """
        Get TTL for an endpoint.
        
        Args:
            endpoint: API endpoint
            
        Returns:
            TTL in seconds
        """
        # Check for exact match first
        if endpoint in self.ttl_config:
            return self.ttl_config[endpoint]
        
        # Check for prefix match
        for pattern, ttl in self.ttl_config.items():
            if pattern != "default" and endpoint.startswith(pattern):
                return ttl
        
        # Return default
        return self.ttl_config["default"]
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Any]:
        """
        Get cached data.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            Cached data if available, None otherwise
        """
        if not self.enabled:
            return None
        
        return self.cache.get(endpoint, params)
    
    def set(self, endpoint: str, data: Any, params: Optional[Dict] = None, ttl: Optional[float] = None) -> None:
        """
        Cache data.
        
        Args:
            endpoint: API endpoint
            data: Data to cache
            params: Query parameters
            ttl: Time-to-live override (uses default if None)
        """
        if not self.enabled:
            return
        
        if ttl is None:
            ttl = self.get_ttl(endpoint)
        
        self.cache.set(endpoint, data, ttl, params)
    
    def invalidate(self, endpoint_pattern: str = None) -> int:
        """
        Invalidate cache for an endpoint pattern.
        
        Args:
            endpoint_pattern: Pattern to match (e.g., "/people")
                             If None, clears all cache
        
        Returns:
            Number of entries invalidated
        """
        if not self.enabled:
            return 0
        
        return self.cache.invalidate(endpoint_pattern)
    
    def clear(self) -> None:
        """Clear all cache."""
        if self.enabled:
            self.cache.clear()
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        if not self.enabled:
            return {"enabled": False}
        
        stats = self.cache.stats()
        stats["enabled"] = True
        return stats


# Global cache manager instance
_cache_manager: Optional[CacheManager] = None


def get_cache_manager(max_size: int = 1000, enabled: bool = True) -> CacheManager:
    """
    Get or create global cache manager.
    
    Args:
        max_size: Maximum cache size
        enabled: Whether caching is enabled
        
    Returns:
        CacheManager instance
    """
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager(max_size=max_size, enabled=enabled)
    return _cache_manager


