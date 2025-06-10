"""
Tests for performance monitoring utilities.
"""

import pytest
import asyncio
import time
from iqa_server.utils.performance import (
    PerformanceMonitor,
    LRUCache,
    monitor,
    cache
)

@pytest.fixture
def performance_monitor():
    """Create a fresh performance monitor instance."""
    return PerformanceMonitor()

@pytest.fixture
def lru_cache():
    """Create a fresh LRU cache instance."""
    return LRUCache(maxsize=2)

def test_performance_monitor_tracking(performance_monitor):
    """Test function performance tracking."""
    @performance_monitor.track("test_func")
    async def test_func():
        await asyncio.sleep(0.1)
        return 42
    
    asyncio.run(test_func())
    
    metrics = performance_monitor.get_metrics("test_func")
    assert metrics["count"] == 1
    assert metrics["total_time"] >= 0.1
    assert metrics["min_time"] == metrics["max_time"]
    assert metrics["avg_time"] == metrics["total_time"]

def test_performance_monitor_multiple_calls(performance_monitor):
    """Test tracking multiple function calls."""
    @performance_monitor.track("test_func")
    def test_func(sleep_time):
        time.sleep(sleep_time)
        return 42
    
    test_func(0.1)
    test_func(0.2)
    
    metrics = performance_monitor.get_metrics("test_func")
    assert metrics["count"] == 2
    assert metrics["total_time"] >= 0.3
    assert metrics["min_time"] < metrics["max_time"]

def test_performance_monitor_reset(performance_monitor):
    """Test resetting performance metrics."""
    @performance_monitor.track("test_func")
    def test_func():
        time.sleep(0.1)
        return 42
    
    test_func()
    performance_monitor.reset("test_func")
    
    metrics = performance_monitor.get_metrics("test_func")
    assert not metrics
    
    # Reset all
    test_func()
    performance_monitor.reset()
    assert not performance_monitor.get_metrics()

def test_lru_cache_basic(lru_cache):
    """Test basic LRU cache operations."""
    lru_cache.put("key1", "value1")
    assert lru_cache.get("key1") == "value1"
    assert lru_cache.get("key2") is None

def test_lru_cache_eviction(lru_cache):
    """Test LRU cache eviction policy."""
    lru_cache.put("key1", "value1")
    lru_cache.put("key2", "value2")
    lru_cache.put("key3", "value3")  # Should evict key1
    
    assert lru_cache.get("key1") is None
    assert lru_cache.get("key2") == "value2"
    assert lru_cache.get("key3") == "value3"

def test_lru_cache_update_access(lru_cache):
    """Test that accessing an item updates its position."""
    lru_cache.put("key1", "value1")
    lru_cache.put("key2", "value2")
    
    # Access key1 to make it most recently used
    lru_cache.get("key1")
    
    # Add new item, should evict key2 instead of key1
    lru_cache.put("key3", "value3")
    
    assert lru_cache.get("key1") == "value1"
    assert lru_cache.get("key2") is None
    assert lru_cache.get("key3") == "value3"

def test_lru_cache_clear(lru_cache):
    """Test cache clearing."""
    lru_cache.put("key1", "value1")
    lru_cache.put("key2", "value2")
    
    lru_cache.clear()
    
    assert lru_cache.get("key1") is None
    assert lru_cache.get("key2") is None

def test_global_instances():
    """Test global monitor and cache instances."""
    assert isinstance(monitor, PerformanceMonitor)
    assert isinstance(cache, LRUCache)
