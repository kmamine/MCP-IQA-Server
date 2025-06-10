"""
Example of batch image quality assessment using PyIQA metrics.
"""

import asyncio
import json
from pathlib import Path
from typing import List
from iqa_server.server.mcp_server import IQAServer

def get_image_paths(directory: Path, pattern: str = "*.jpg") -> List[Path]:
    """Get all image paths in a directory."""
    return list(directory.glob(pattern))

async def main():
    # Initialize server
    server = IQAServer()
    await server.startup()
    
    try:
        # Get paths to test and reference images
        sample_dir = Path(__file__).parent.parent / "iqa_server/data/sample_images"
        test_images = get_image_paths(sample_dir / "test")
        ref_images = get_image_paths(sample_dir / "reference")
        
        # Batch assessment with no-reference metrics
        print("\nBatch assessment with no-reference metrics...")
        result = await server.handle_tool_call({
            "name": "batch_assessment",
            "parameters": {
                "image_paths": [str(p) for p in test_images],
                "metrics": ["brisque", "niqe", "musiq"]
            }
        })
        print(json.dumps(result, indent=2))
        
        # Batch assessment with full-reference metrics
        print("\nBatch assessment with full-reference metrics...")
        result = await server.handle_tool_call({
            "name": "batch_assessment",
            "parameters": {
                "image_paths": [str(p) for p in test_images[:5]],  # First 5 images
                "reference_paths": [str(p) for p in ref_images[:5]],
                "metrics": ["psnr", "ssim", "lpips"]
            }
        })
        print(json.dumps(result, indent=2))
        
        # Get available metrics info
        print("\nGetting available metrics info...")
        result = await server.handle_tool_call({
            "name": "get_available_metrics",
            "parameters": {
                "metric_type": "all",
                "detailed": True
            }
        })
        print(json.dumps(result, indent=2))
        
    finally:
        await server.shutdown()

if __name__ == "__main__":
    asyncio.run(main())