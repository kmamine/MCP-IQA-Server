"""
IQA Server - A Model Context Protocol server for Image Quality Assessment.
"""

from .server.mcp_server import IQAServer
from .indicators.base import BaseIndicator
from .core.config import Config
from .core.exceptions import IQAError, InvalidInputError, MetricError
from .utils.validation import validate_image_path, validate_metrics

__version__ = "1.0.0"

__all__ = [
    'IQAServer',
    'BaseIndicator',
    'Config',
    'IQAError',
    'InvalidInputError',
    'MetricError',
    'validate_image_path',
    'validate_metrics',
]