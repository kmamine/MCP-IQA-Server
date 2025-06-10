"""
Utilities for input validation and error handling.
"""

import os
from pathlib import Path
from typing import List, Optional, Tuple, Union
import numpy as np
from PIL import Image
from ..core.constants import SUPPORTED_FORMATS, MAX_IMAGE_SIZE

def validate_image_path(path: Union[str, Path]) -> Tuple[bool, Optional[str]]:
    """
    Validate that a path points to a valid image file.
    
    Args:
        path: Path to image file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(path, (str, Path)):
        return False, "Image path must be a string or Path object"
        
    path = Path(path)
    
    if not path.exists():
        return False, f"Image file not found: {path}"
        
    if path.suffix.lower() not in SUPPORTED_FORMATS:
        return False, f"Unsupported image format: {path.suffix}"
        
    try:
        with Image.open(path) as img:
            img.verify()
    except Exception as e:
        return False, f"Invalid image file: {e}"
        
    return True, None

def validate_image_data(image: np.ndarray) -> Tuple[bool, Optional[str]]:
    """
    Validate that an image array has correct format and dimensions.
    
    Args:
        image: Image as numpy array
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(image, np.ndarray):
        return False, "Image must be a numpy array"
        
    if image.ndim not in (2, 3):
        return False, f"Invalid image dimensions: {image.ndim}"
        
    if image.ndim == 3 and image.shape[2] not in (1, 3, 4):
        return False, f"Invalid number of channels: {image.shape[2]}"
        
    if any(dim > MAX_IMAGE_SIZE for dim in image.shape[:2]):
        return False, f"Image dimensions exceed maximum size of {MAX_IMAGE_SIZE}"
        
    if image.dtype != np.uint8:
        return False, f"Invalid image data type: {image.dtype}"
        
    return True, None

def validate_metrics(
    metrics: List[str],
    available_metrics: List[str]
) -> Tuple[bool, Optional[str]]:
    """
    Validate that requested metrics are available.
    
    Args:
        metrics: List of requested metric names
        available_metrics: List of available metric names
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not metrics:
        return False, "No metrics specified"
        
    unknown_metrics = set(metrics) - set(available_metrics)
    if unknown_metrics:
        return False, f"Unknown metrics: {', '.join(unknown_metrics)}"
        
    return True, None

def validate_score(score: float, metric: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that a metric score is in the valid range.
    
    Args:
        score: Metric score value
        metric: Name of the metric
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(score, (int, float)):
        return False, f"Invalid score type: {type(score)}"
        
    # All our metrics are normalized to 0-100 range
    if not 0 <= score <= 100:
        return False, f"Score {score} out of valid range (0-100)"
        
    return True, None

def validate_batch_size(size: int, max_size: int = 100) -> Tuple[bool, Optional[str]]:
    """
    Validate batch size for batch processing.
    
    Args:
        size: Requested batch size
        max_size: Maximum allowed batch size
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(size, int):
        return False, "Batch size must be an integer"
        
    if size < 1:
        return False, "Batch size must be positive"
        
    if size > max_size:
        return False, f"Batch size {size} exceeds maximum of {max_size}"
        
    return True, None