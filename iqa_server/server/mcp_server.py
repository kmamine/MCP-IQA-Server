"""
MCP Server implementation for Image Quality Assessment using PyIQA.
This module implements a Model Context Protocol server that leverages the PyIQA library
for high-quality image assessment metrics.
"""

import asyncio
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import torch
from mcp import MCPBase, Tool, ToolCall
import pyiqa

from ..core.config import Config
from ..core.constants import (
    FR_METRICS, NR_METRICS, ALL_METRICS,
    DEFAULT_FR_METRICS, DEFAULT_NR_METRICS,
    METRIC_INTERPRETATIONS
)
from ..core.exceptions import InvalidInputError, ServerError
from ..utils.validation import validate_image_path
from ..utils.performance import monitor, cache
from .tools import get_iqa_tools
from .handlers import (
    handle_assess_image_quality,
    handle_batch_assessment,
    handle_get_metric_info
)

class IQAServer(MCPBase):
    """MCP server implementation for Image Quality Assessment using PyIQA."""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the IQA server.
        
        Args:
            config: Optional configuration object
        """
        super().__init__()
        self.config = config or Config()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self._metrics = {}  # Cache for PyIQA metric instances
        
    async def startup(self):
        """Initialize resources when the server starts."""
        try:
            # Pre-initialize commonly used metrics
            for metric in DEFAULT_FR_METRICS + DEFAULT_NR_METRICS:
                await self._get_or_create_metric(metric)
        except Exception as e:
            raise ServerError(f"Failed to initialize metrics: {str(e)}")
        
    async def shutdown(self):
        """Cleanup resources when the server shuts down."""
        # Clear metric instances and GPU memory
        self._metrics.clear()
        torch.cuda.empty_cache()
        
    def get_tools(self) -> List[Tool]:
        """Return the list of available tools."""
        return get_iqa_tools()
        
    async def handle_tool_call(self, tool_call: ToolCall) -> Dict[str, Any]:
        """
        Handle incoming tool calls.
        
        Args:
            tool_call: Tool call object containing request details
            
        Returns:
            Response dictionary
        """
        tool_name = tool_call.name
        params = tool_call.parameters
        
        if tool_name == "assess_image_quality":
            return await handle_assess_image_quality(
                image_path=params["image_path"],
                metrics=params.get("metrics"),
                reference_path=params.get("reference_path")
            )
            
        elif tool_name == "batch_assessment":
            return await handle_batch_assessment(
                image_paths=params["image_paths"],
                metrics=params.get("metrics"),
                reference_paths=params.get("reference_paths")
            )
            
        elif tool_name == "get_available_metrics":
            return {
                "fr_metrics": FR_METRICS,
                "nr_metrics": NR_METRICS,
                "all_metrics": ALL_METRICS,
                "default_fr": DEFAULT_FR_METRICS,
                "default_nr": DEFAULT_NR_METRICS
            }
            
        elif tool_name == "get_metric_interpretation":
            metric_name = params["metric_name"]
            score = params.get("score")
            
            if metric_name not in METRIC_INTERPRETATIONS:
                raise InvalidInputError(f"No interpretation available for metric: {metric_name}")
                
            interp = METRIC_INTERPRETATIONS[metric_name]
            if score is not None:
                # Find the range that contains this score
                for range_tuple, description in interp["ranges"].items():
                    if range_tuple[0] <= score <= range_tuple[1]:
                        return {
                            "metric": metric_name,
                            "score": score,
                            "interpretation": description,
                            "better_direction": interp["better"],
                            "ranges": interp["ranges"]
                        }
            
            return {
                "metric": metric_name,
                "better_direction": interp["better"],
                "ranges": interp["ranges"]
            }
            
        else:
            raise InvalidInputError(f"Unknown tool: {tool_name}")
            
    async def _get_or_create_metric(self, metric_name: str) -> Any:
        """
        Get or create a PyIQA metric instance.
        
        Args:
            metric_name: Name of the metric
            
        Returns:
            PyIQA metric instance
        """
        if metric_name not in self._metrics:
            try:
                self._metrics[metric_name] = pyiqa.create_metric(
                    metric_name,
                    device=self.device
                )
            except Exception as e:
                raise ServerError(f"Failed to create metric {metric_name}: {str(e)}")
                
        return self._metrics[metric_name]
    """MCP server implementation for Image Quality Assessment."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the IQA server with configuration."""
        super().__init__()
        self.config = config or Config()
        self.indicators = get_available_indicators()
        
    async def startup(self):
        """Initialize resources when the server starts."""
        # Load any required models or resources
        await self._initialize_indicators()
        
    async def shutdown(self):
        """Cleanup resources when the server shuts down."""
        # Cleanup any resources
        pass

    def get_tools(self) -> List[Tool]:
        """Return the list of available tools."""
        return [
            Tool(
                name="assess_image_quality",
                description="Assess the quality of an input image using various metrics",
                parameters={
                    "type": "object",
                    "properties": {
                        "image_path": {
                            "type": "string",
                            "description": "Path to the input image"
                        },
                        "metrics": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of metrics to compute"
                        }
                    },
                    "required": ["image_path"]
                }
            ),
            Tool(
                name="list_available_metrics",
                description="List all available image quality metrics",
                parameters={"type": "object", "properties": {}}
            )
        ]

    async def handle_tool_call(self, tool_call: ToolCall) -> Any:
        """Handle incoming tool calls."""
        if tool_call.name == "assess_image_quality":
            return await self._handle_assess_image(tool_call.parameters)
        elif tool_call.name == "list_available_metrics":
            return self._handle_list_metrics()
        else:
            raise ValueError(f"Unknown tool: {tool_call.name}")

    async def _initialize_indicators(self):
        """Initialize quality assessment indicators."""
        for indicator in self.indicators:
            await indicator.initialize()

    async def _handle_assess_image(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle image quality assessment requests."""
        image_path = parameters["image_path"]
        requested_metrics = parameters.get("metrics", None)

        # Load and validate image
        image = load_image(image_path)
        validate_image(image)

        # Compute metrics
        results = await compute_metrics(
            image,
            metrics=requested_metrics,
            indicators=self.indicators
        )

        return {
            "metrics": results,
            "summary": self._generate_quality_summary(results)
        }

    def _handle_list_metrics(self) -> Dict[str, List[str]]:
        """Handle requests to list available metrics."""
        return {
            "available_metrics": [
                metric.name for indicator in self.indicators
                for metric in indicator.available_metrics()
            ]
        }

    def _generate_quality_summary(self, results: Dict[str, float]) -> str:
        """Generate a human-readable summary of quality assessment results."""
        # Implementation of quality summary generation
        overall_quality = sum(results.values()) / len(results)
        return f"Overall image quality score: {overall_quality:.2f}"