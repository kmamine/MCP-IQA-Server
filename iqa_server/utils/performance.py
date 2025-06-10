"""
Utilities for monitoring and optimizing performance.
"""

import time
import asyncio
import functools
from typing import Any, Callable, Dict, Optional, TypeVar
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import numpy as np
from ..core.constants import DEFAULT_CACHE_SIZE, CACHE_TIMEOUT

T = TypeVar('T')

class PerformanceMonitor:
    """Monitor execution time and resource usage of functions."""
    
    def __init__(self):
        self.metrics: Dict[str, Dict[str, float]] = {}
        self._lock = Lock()
        
    def track(self, func_name: str) -> Callable:
        """
        Decorator to track function performance.
        
        Args:
            func_name: Name of the function to track
            
        Returns:
            Decorated function
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            async def wrapped(*args: Any, **kwargs: Any) -> Any:
                start_time = time.time()
                try:
                    if asyncio.iscoroutinefunction(func):
                        result = await func(*args, **kwargs)
                    else:
                        result = func(*args, **kwargs)
                finally:
                    duration = time.time() - start_time
                    self._update_metrics(func_name, duration)
                return result
            return wrapped
        return decorator
        
    def _update_metrics(self, func_name: str, duration: float) -> None:
        """Update performance metrics for a function."""
        with self._lock:
            if func_name not in self.metrics:
                self.metrics[func_name] = {
                    'count': 0,
                    'total_time': 0,
                    'min_time': float('inf'),
                    'max_time': 0,
                    'avg_time': 0
                }
            
            metrics = self.metrics[func_name]
            metrics['count'] += 1
            metrics['total_time'] += duration
            metrics['min_time'] = min(metrics['min_time'], duration)
            metrics['max_time'] = max(metrics['max_time'], duration)
            metrics['avg_time'] = metrics['total_time'] / metrics['count']
            
    def get_metrics(self, func_name: Optional[str] = None) -> Dict:
        """Get performance metrics for one or all functions."""
        with self._lock:
            if func_name:
                return self.metrics.get(func_name, {})
            return self.metrics.copy()
            
    def reset(self, func_name: Optional[str] = None) -> None:
        """Reset metrics for one or all functions."""
        with self._lock:
            if func_name:
                self.metrics.pop(func_name, None)
            else:
                self.metrics.clear()

class LRUCache:
    """Least Recently Used (LRU) cache for computationally expensive results."""
    
    def __init__(self, maxsize: int = DEFAULT_CACHE_SIZE):
        self.maxsize = maxsize
        self.cache: Dict[str, Dict] = {}
        self.timestamps: Dict[str, float] = {}
        self._lock = Lock()
        
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache if it exists and isn't expired."""
        with self._lock:
            if key not in self.cache:
                return None
                
            # Check for expiration
            if time.time() - self.timestamps[key] > CACHE_TIMEOUT:
                self.cache.pop(key)
                self.timestamps.pop(key)
                return None
                
            # Update timestamp on access
            self.timestamps[key] = time.time()
            return self.cache[key]
            
    def put(self, key: str, value: Any) -> None:
        """Add item to cache, removing least recently used if full."""
        with self._lock:
            if len(self.cache) >= self.maxsize:
                # Remove least recently used item
                lru_key = min(self.timestamps.items(), key=lambda x: x[1])[0]
                self.cache.pop(lru_key)
                self.timestamps.pop(lru_key)
                
            self.cache[key] = value
            self.timestamps[key] = time.time()
            
    def clear(self) -> None:
        """Clear all items from cache."""
        with self._lock:
            self.cache.clear()
            self.timestamps.clear()

# Global instances
monitor = PerformanceMonitor()
cache = LRUCache()