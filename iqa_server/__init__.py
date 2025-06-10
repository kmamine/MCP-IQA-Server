"""
IQA MCP Server Package

Contains modules for Image Quality Assessment (IQA) model information
through the Model Context Protocol.
"""

from iqa_server.server import IQAServer
from iqa_server.models import IQAModelDatabase, model_database
from iqa_server.utils import (
    format_model_info,
    generate_model_comparison,
    format_search_results,
    generate_usage_example
)
from iqa_server import constants

__version__ = constants.SERVER_VERSION

__all__ = [
    "IQAServer",
    "IQAModelDatabase",
    "model_database",
    "format_model_info",
    "generate_model_comparison",
    "format_search_results",
    "generate_usage_example",
    "constants"
]
