#!/usr/bin/env python3
"""
Example usage of the IQA MCP Server
"""

import asyncio
import json
from mcp import ClientSession, StdioClientParameters
from mcp.client import Client
from mcp.client.stdio import stdio_client
from mcp.types import AnyUrl

async def main():
    """Example client usage of the IQA MCP Server."""
    # Create a client session
    async with stdio_client("python iqa_server.py") as (read_stream, write_stream):
        client = Client()
        await client.initialize(
            read_stream,
            write_stream,
            StdioClientParameters(server_name="iqa-pytorch"),
        )

        # List all available resources
        resources = await client.list_resources()
        print("\nAvailable Resources:")
        for resource in resources:
            print(f"- {resource.name}: {resource.uri}")

        # Get all IQA models
        content = await client.read_resource(AnyUrl("iqa://models/all"))
        models = json.loads(content)
        print("\nTotal number of models:", sum(len(category) for category in models.values()))

        # Search for SSIM-related models
        result = await client.call_tool("search_models", {"query": "ssim"})
        print("\nSSIM-related models:")
        ssim_models = json.loads(result[0].text)
        for model in ssim_models:
            print(f"- {model['key']}: {model['info']['description']}")

        # Get usage example for SSIM
        result = await client.call_tool("get_usage_example", {"model_name": "ssim"})
        print("\nSSIM Usage Example:")
        print(result[0].text)

if __name__ == "__main__":
    asyncio.run(main())
