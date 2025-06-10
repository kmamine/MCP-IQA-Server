"""
Tool definitions for the IQA MCP server using PyIQA.
"""

from typing import Dict, List
from mcp import Tool
import pyiqa
from ..core.constants import FR_METRICS, NR_METRICS, ALL_METRICS, METRIC_INTERPRETATIONS

def get_iqa_tools() -> List[Tool]:
    """
    Get the list of tools provided by the IQA server.
    
    Returns:
        List of Tool objects
    """
    return [
        Tool(
            name="assess_image_quality",
            description="Assess the quality of an input image using PyIQA metrics",
            parameters={
                "type": "object",
                "required": ["image_path"],
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the input image"
                    },
                    "metrics": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ALL_METRICS
                        },
                        "description": "List of metrics to compute. Available metrics:\n" +
                                     "Full-reference: " + ", ".join(FR_METRICS) + "\n" +
                                     "No-reference: " + ", ".join(NR_METRICS)
                    },
                    "reference_path": {
                        "type": "string",
                        "description": "Path to reference image (required for full-reference metrics)"
                    }
                }
            }
        ),
        Tool(
            name="batch_assessment",
            description="Assess the quality of multiple images using PyIQA metrics",
            parameters={
                "type": "object",
                "required": ["image_paths"],
                "properties": {
                    "image_paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of paths to input images"
                    },
                    "metrics": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ALL_METRICS
                        },
                        "description": "List of metrics to compute. Available metrics:\n" +
                                     "Full-reference: " + ", ".join(FR_METRICS) + "\n" +
                                     "No-reference: " + ", ".join(NR_METRICS)
                    },
                    "reference_paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of paths to reference images (required for full-reference metrics)"
                    }
                }
            }
        ),
        Tool(
            name="get_available_metrics",
            description="Get information about available PyIQA metrics",
            parameters={
                "type": "object",
                "properties": {
                    "metric_type": {
                        "type": "string",
                        "enum": ["fr", "nr", "all"],
                        "description": "Type of metrics to get information about"
                    }
                }
            }
        ),
        Tool(
            name="get_metric_interpretation",
            description="Get interpretation guidelines for PyIQA metric scores",
            parameters={
                "type": "object",
                "required": ["metric_name"],
                "properties": {
                    "metric_name": {
                        "type": "string",
                        "enum": ALL_METRICS,
                        "description": "Name of the metric"
                    },
                    "score": {
                        "type": "number",
                        "description": "Score value to interpret"
                    }
                }
            }
        )
    ]