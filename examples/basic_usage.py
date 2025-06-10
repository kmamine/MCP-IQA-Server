"""
Basic usage example of the IQA server with PyIQA metrics.
"""

import asyncio
import json
from pathlib import Path
from iqa_server.server.mcp_server import IQAServer

async def main():
    # Initialize server
    server = IQAServer()
    await server.startup()
    
    try:
        # Get available metrics
        tools = server.get_tools()
        print("\nAvailable tools:")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")
            
        # Example image paths
        image_path = Path(__file__).parent.parent / "iqa_server/data/sample_images/test.jpg"
        reference_path = Path(__file__).parent.parent / "iqa_server/data/sample_images/reference.jpg"
        
        # Assess single image quality
        print("\nAssessing single image quality...")
        result = await server.handle_tool_call({
            "name": "assess_image_quality",
            "parameters": {
                "image_path": str(image_path),
                "metrics": ["brisque", "niqe"]  # No-reference metrics
            }
        })
        print(json.dumps(result, indent=2))
        
        # Compare with reference image
        print("\nComparing with reference image...")
        result = await server.handle_tool_call({
            "name": "assess_image_quality",
            "parameters": {
                "image_path": str(image_path),
                "reference_path": str(reference_path),
                "metrics": ["psnr", "ssim", "lpips"]  # Full-reference metrics
            }
        })
        print(json.dumps(result, indent=2))
        
        # Get metric interpretation
        print("\nGetting metric interpretation...")
        result = await server.handle_tool_call({
            "name": "get_metric_interpretation",
            "parameters": {
                "metric_name": "brisque",
                "score": 25.5
            }
        })
        print(json.dumps(result, indent=2))
        
    finally:
        await server.shutdown()

if __name__ == "__main__":
    asyncio.run(main())