"""
Base class for all image quality assessment indicators using PyIQA.
"""

import torch
from typing import Any, Dict, List, Optional, Union
import numpy as np
from pathlib import Path
import pyiqa

class BaseIndicator:
    """Base class for IQA indicators using PyIQA."""
    
    def __init__(self, metric_name: str):
        """
        Initialize the indicator with a PyIQA metric.
        
        Args:
            metric_name: Name of the PyIQA metric
        """
        self.name = metric_name
        self.iqa_metric = None
        self.requires_ref = metric_name in pyiqa.get_fr_metrics()
        self.metric_info = pyiqa.get_metric_info(metric_name)
        self.description = self.metric_info.get('metric_reference', 'No description available')
        self._is_initialized = False
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
    async def initialize(self) -> None:
        """Initialize the PyIQA metric."""
        if not self._is_initialized:
            self.iqa_metric = pyiqa.create_metric(self.name, device=self.device)
            self._is_initialized = True
            
    async def compute(self, image_path: Union[str, Path], ref_path: Optional[str] = None) -> float:
        """
        Compute the quality score for an input image.
        
        Args:
            image_path: Path to the input image
            ref_path: Path to the reference image (required for FR metrics)
            
        Returns:
            Quality score as a float
        """
        if not self._is_initialized:
            await self.initialize()
            
        if self.requires_ref and ref_path is None:
            raise ValueError(f"{self.name} requires a reference image")
            
        try:
            if self.requires_ref:
                score = self.iqa_metric(image_path, ref_path)
            else:
                score = self.iqa_metric(image_path)
                
            # Convert to standard Python float and normalize if needed
            score = float(score.cpu().numpy())
            return self._normalize_score(score)
            
        except Exception as e:
            raise RuntimeError(f"Failed to compute {self.name} score: {str(e)}")
            
    def _normalize_score(self, score: float) -> float:
        """
        Normalize the score to a 0-100 range where appropriate.
        Different metrics have different ranges, so this needs to be handled per metric.
        
        Args:
            score: Raw score from the metric
            
        Returns:
            Normalized score
        """
        # Get metric-specific normalization info
        lower_better = self.metric_info.get('lower_better', False)
        value_range = self.metric_info.get('value_range', None)
        
        if value_range:
            min_val, max_val = value_range
            normalized = (score - min_val) / (max_val - min_val) * 100
            if lower_better:
                normalized = 100 - normalized
            return max(0, min(normalized, 100))
        
        return score
        
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get metadata about this indicator.
        
        Returns:
            Dictionary containing indicator metadata
        """
        return {
            "name": self.name,
            "description": self.description,
            "requires_reference": self.requires_ref,
            "is_initialized": self._is_initialized,
            "lower_better": self.metric_info.get('lower_better', False),
            "value_range": self.metric_info.get('value_range', None),
            "metric_reference": self.metric_info.get('metric_reference', None)
        }
        
    async def cleanup(self) -> None:
        """Cleanup GPU memory if needed."""
        if self.iqa_metric is not None:
            self.iqa_metric = None
            torch.cuda.empty_cache()
        
    @abstractmethod
    async def compute(self, image: np.ndarray) -> float:
        """
        Compute the quality score for an input image.
        
        Args:
            image: Input image as numpy array (HxWxC)
            
        Returns:
            Quality score as a float
        """
        raise NotImplementedError
        
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize any required models or resources."""
        raise NotImplementedError
        
    async def __call__(self, image: np.ndarray) -> float:
        """
        Callable interface for convenience.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Quality score
        """
        if not self._is_initialized:
            await self.initialize()
            self._is_initialized = True
        return await self.compute(image)
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get metadata about this indicator.
        
        Returns:
            Dictionary containing indicator metadata
        """
        return {
            "name": self.name,
            "description": self.description,
            "is_initialized": self._is_initialized
        }
        
    async def cleanup(self) -> None:
        """Cleanup any resources. Override if needed."""
        pass