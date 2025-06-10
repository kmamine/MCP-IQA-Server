"""
Traditional image quality assessment metrics implemented through PyIQA.
"""

from typing import Any, Dict, Optional
import torch
import pyiqa
from .base import BaseIndicator

class PSNRIndicator(BaseIndicator):
    """Peak Signal-to-Noise Ratio (PSNR) metric."""
    
    def __init__(self):
        super().__init__(metric_name='psnr')

class SSIMIndicator(BaseIndicator):
    """Structural Similarity Index (SSIM) metric."""
    
    def __init__(self):
        super().__init__(metric_name='ssim')

class MSEIndicator(BaseIndicator):
    """Mean Squared Error (MSE) metric."""
    
    def __init__(self):
        super().__init__(metric_name='mse')
        
class FIDIndicator(BaseIndicator):
    """Fréchet Inception Distance (FID) metric."""
    
    def __init__(self):
        super().__init__(metric_name='fid')

class LPIPSIndicator(BaseIndicator):
    """Learned Perceptual Image Patch Similarity (LPIPS) metric."""
    
    def __init__(self, net_type: str = 'alex'):
        """
        Initialize LPIPS with specific network backbone.
        
        Args:
            net_type: Network backbone ('alex' or 'vgg')
        """
        super().__init__(metric_name='lpips')
        self.net_type = net_type
        
    async def initialize(self) -> None:
        """Initialize with specific network type."""
        if not self._is_initialized:
            self.iqa_metric = pyiqa.create_metric(
                self.name,
                model_path=None,  # Use default weights
                net=self.net_type,
                device=self.device
            )
            self._is_initialized = True