"""
Custom exceptions for the IQA server.
"""

class IQAError(Exception):
    """Base exception for IQA server errors."""
    pass

class InvalidInputError(IQAError):
    """Exception raised for invalid input data."""
    pass

class MetricError(IQAError):
    """Exception raised for metric-related errors."""
    pass

class ConfigurationError(IQAError):
    """Exception raised for configuration errors."""
    pass

class ResourceError(IQAError):
    """Exception raised for resource-related errors (GPU, memory, etc)."""
    pass

class ServerError(IQAError):
    """Exception raised for server-related errors."""
    pass

class ValidationError(IQAError):
    """Exception raised for validation errors."""
    pass

class CacheError(IQAError):
    """Exception raised for caching-related errors."""
    pass