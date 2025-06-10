"""
IQA MCP Server Module

Implements the Model Context Protocol server for IQA model information.
"""

import json
from typing import Dict, List, Any
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.types as types

from .models import model_database
from .utils import format_model_info, generate_model_comparison, format_search_results, generate_usage_example

class IQAServer:
    """MCP server implementation for IQA models."""
    
    def __init__(self, server_name: str = "iqa-pytorch"):
        self.server = Server(server_name)
        self.format_model_info = format_model_info
        self.generate_model_comparison = generate_model_comparison
        self.format_search_results = format_search_results
        self.generate_usage_example = generate_usage_example
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up the server request handlers."""
        
        @self.server.list_resources()
        async def handle_list_resources() -> list[types.Resource]:
            """List available IQA model resources."""
            return [
                types.Resource(
                    uri="iqa://models/all",
                    name="All IQA Models",
                    description="Complete list of all available IQA models",
                    mimeType="application/json",
                ),
                types.Resource(
                    uri="iqa://models/fr", 
                    name="Full Reference Models",
                    description="List of Full Reference (FR) IQA models",
                    mimeType="application/json",
                ),
                types.Resource(
                    uri="iqa://models/nr",
                    name="No Reference Models", 
                    description="List of No Reference (NR) IQA models",
                    mimeType="application/json",
                ),
                types.Resource(
                    uri="iqa://models/specific",
                    name="Task-Specific Models",
                    description="List of task-specific IQA models (Color, Face, Underwater)",
                    mimeType="application/json",
                ),
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: types.AnyUrl) -> str:
            """Read IQA model information based on URI."""
            uri_str = str(uri)
            
            if uri_str == "iqa://models/all":
                return json.dumps(model_database.get_all_models(), indent=2)
            elif uri_str == "iqa://models/fr":
                return json.dumps(model_database.get_fr_models(), indent=2)
            elif uri_str == "iqa://models/nr":
                return json.dumps(model_database.get_nr_models(), indent=2)
            elif uri_str == "iqa://models/specific":
                return json.dumps(model_database.get_specific_models(), indent=2)
            else:
                raise ValueError(f"Unknown resource URI: {uri}")
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """List available tools for IQA model operations."""
            return [
                types.Tool(
                    name="search_models",
                    description="Search for IQA models by name, type, or category",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query (model name, type, or category)"
                            },
                            "model_type": {
                                "type": "string",
                                "enum": ["FR", "NR", "Specific", "all"],
                                "description": "Filter by model type"
                            }
                        },
                        "required": ["query"]
                    },
                ),
                types.Tool(
                    name="get_model_info",
                    description="Get detailed information about a specific IQA model",
                    inputSchema={
                        "type": "object", 
                        "properties": {
                            "model_name": {
                                "type": "string",
                                "description": "Name of the IQA model"
                            }
                        },
                        "required": ["model_name"]
                    },
                ),
                types.Tool(
                    name="list_model_names",
                    description="Get all available model names for pyiqa.create_metric()",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "model_type": {
                                "type": "string",
                                "enum": ["FR", "NR", "Specific", "all"],
                                "description": "Filter by model type (default: all)"
                            }
                        }
                    },
                ),
                types.Tool(
                    name="get_usage_example",
                    description="Get usage examples for IQA models",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "model_name": {
                                "type": "string", 
                                "description": "Name of the IQA model"
                            }
                        },
                        "required": ["model_name"]
                    },
                ),
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict[str, Any]
        ) -> list[types.TextContent]:
            """Handle tool calls for IQA model operations."""
            
            if name == "search_models":
                query = arguments["query"]
                model_type = arguments.get("model_type", "all")
                results = model_database.search_models(query, model_type)
                return [types.TextContent(
                    type="text",
                    text=self.format_search_results(results)
                )]
            
            elif name == "get_model_info":
                model_name = arguments["model_name"]
                model_info = model_database.get_model_info(model_name)
                if model_info:
                    return [types.TextContent(
                        type="text",
                        text=self.format_model_info(model_info)
                    )]
                return [types.TextContent(
                    type="text", 
                    text=f"Model '{model_name}' not found in IQA database."
                )]
            
            elif name == "list_model_names":
                model_type = arguments.get("model_type", "all")
                names = model_database.list_model_names(model_type)
                return [types.TextContent(
                    type="text",
                    text=json.dumps(names, indent=2)
                )]
            
            elif name == "get_usage_example":
                model_name = arguments["model_name"]
                model_info = model_database.get_model_info(model_name)
                return [types.TextContent(
                    type="text",
                    text=self.generate_usage_example(model_name, model_info)
                )]
            
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def run(self, read_stream, write_stream):
        """Run the server."""
        await self.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="iqa-pytorch",
                server_version="0.1.0",
                capabilities=self.server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={},
                ),
            ),
        )
