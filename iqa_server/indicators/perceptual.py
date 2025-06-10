"""
Perceptual image quality assessment indicators.
These metrics aim to match human perception of image quality.
"""

import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
import numpy as np
from typing import Optional
from .base import BaseIndicator

class LPIPSIndicator(BaseIndicator):
    """Learned Perceptual Image Patch Similarity"""
    
    def __init__(self, net: str = 'alex'):
        super().__init__(
            name="LPIPS",
            description="Learned Perceptual Image Patch Similarity metric"
        )
        self.net_type = net
        self.model: Optional[nn.Module] = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                              std=[0.229, 0.224, 0.225])
        ])
        
    async def initialize(self) -> None:
        """Initialize the LPIPS model."""
        if self.net_type == 'alex':
            self.model = models.alexnet(pretrained=True)
        elif self.net_type == 'vgg':
            self.model = models.vgg16(pretrained=True)
        else:
            raise ValueError(f"Unknown network type: {self.net_type}")
            
        self.model = self.model.features.to(self.device)
        self.model.eval()
        
    async def compute(self, image: np.ndarray) -> float:
        """
        Compute LPIPS score for an image.
        Lower scores indicate better perceptual quality.
        """
        if self.model is None:
            await self.initialize()
            
        # Convert numpy array to torch tensor
        if image.dtype == np.uint8:
            image = image.astype(np.float32) / 255.0
            
        x = self.transform(image).unsqueeze(0).to(self.device)
        
        # Generate reference using Gaussian blur as a simple baseline
        sigma = 0.5
        kernel_size = int(2 * 4 * sigma + 1)
        reference = transforms.GaussianBlur(kernel_size, sigma)(x)
        
        with torch.no_grad():
            feat_x = self.model(x)
            feat_ref = self.model(reference)
            
            # Compute distance in feature space
            dist = torch.mean((feat_x - feat_ref) ** 2)
            
        # Normalize to 0-100 range where 0 is best quality
        score = min(max(float(dist) * 100, 0), 100)
        return score
        
    async def cleanup(self) -> None:
        """Cleanup GPU memory."""
        if self.model is not None:
            self.model.cpu()
            torch.cuda.empty_cache()

class SSIMIndicator(BaseIndicator):
    """Structural Similarity Index Measure"""
    
    def __init__(self):
        super().__init__(
            name="SSIM",
            description="Structural Similarity Index Measure"
        )
        
    async def initialize(self) -> None:
        """No initialization needed."""
        pass
        
    async def compute(self, image: np.ndarray) -> float:
        """
        Compute SSIM score for an image.
        Higher scores indicate better structural similarity.
        """
        if len(image.shape) == 3:
            image = np.mean(image, axis=2)
            
        # Generate reference using Gaussian blur
        from scipy.ndimage import gaussian_filter
        reference = gaussian_filter(image, sigma=0.5)
        
        # Constants for stability
        C1 = (0.01 * 255) ** 2
        C2 = (0.03 * 255) ** 2
        
        # Compute means
        mu_x = image.mean()
        mu_y = reference.mean()
        
        # Compute variances and covariance
        sigma_x = np.sqrt(((image - mu_x) ** 2).mean())
        sigma_y = np.sqrt(((reference - mu_y) ** 2).mean())
        sigma_xy = ((image - mu_x) * (reference - mu_y)).mean()
        
        # Compute SSIM
        num = (2 * mu_x * mu_y + C1) * (2 * sigma_xy + C2)
        den = (mu_x ** 2 + mu_y ** 2 + C1) * (sigma_x ** 2 + sigma_y ** 2 + C2)
        ssim = num / den
        
        # Convert to 0-100 range where 100 is best quality
        score = min(max(float(ssim) * 100, 0), 100)
        return score