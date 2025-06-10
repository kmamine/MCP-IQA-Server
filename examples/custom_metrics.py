"""
Example of using custom metrics with the IQA server.
"""

import asyncio
import json
from pathlib import Path
import torch
import pyiqa
from iqa_server.indicators.base import BaseIndicator
from iqa_server.server.mcp_server import IQAServer

class CustomLPIPSIndicator(BaseIndicator):
    """Custom LPIPS indicator with different backbone."""
    
    def __init__(self, net_type: str = 'vgg'):
        super().__init__(metric_name='lpips')
        self.net_type = net_type
        
    async def initialize(self) -> None:
        """Initialize with specific network backbone."""
        if not self._is_initialized:
            self.iqa_metric = pyiqa.create_metric(
                self.name,
                net=self.net_type,
                device=self.device
            )
            self._is_initialized = True
            
    def get_metadata(self) -> Dict:
        """Get metadata including network type."""
        meta = super().get_metadata()
        meta['net_type'] = self.net_type
        return meta

async def main():
    # Initialize server
    server = IQAServer()
    
    # Register custom metric
    server._metrics['lpips_vgg'] = CustomLPIPSIndicator(net_type='vgg')
    
    await server.startup()
    
    try:
        # Example image paths
        image_path = Path(__file__).parent.parent / "iqa_server/data/sample_images/test.jpg"
        reference_path = Path(__file__).parent.parent / "iqa_server/data/sample_images/reference.jpg"
        
        # Compare using both default and custom LPIPS
        print("\nComparing LPIPS variants...")
        result = await server.handle_tool_call({
            "name": "assess_image_quality",
            "parameters": {
                "image_path": str(image_path),
                "reference_path": str(reference_path),
                "metrics": ["lpips", "lpips_vgg"]
            }
        })
        print(json.dumps(result, indent=2))
        
        # Get metadata for custom metric
        custom_metric = server._metrics['lpips_vgg']
        print("\nCustom metric metadata:")
        print(json.dumps(custom_metric.get_metadata(), indent=2))
        
    finally:
        await server.shutdown()

if __name__ == "__main__":
    asyncio.run(main())