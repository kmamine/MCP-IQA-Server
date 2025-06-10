"""
Utilities for image loading, preprocessing and manipulation.
"""

from typing import Optional, Tuple, Union
import numpy as np
from PIL import Image
import cv2
from pathlib import Path
from .validation import validate_image_path, validate_image_data
from ..core.constants import DEFAULT_IMAGE_SIZE

def load_image(path: Union[str, Path]) -> np.ndarray:
    """
    Load an image from file.
    
    Args:
        path: Path to image file
        
    Returns:
        Image as numpy array (HxWxC)
        
    Raises:
        ValueError: If image is invalid or can't be loaded
    """
    is_valid, error = validate_image_path(path)
    if not is_valid:
        raise ValueError(error)
        
    try:
        # Use PIL for broad format support
        with Image.open(path) as img:
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            return np.array(img)
    except Exception as e:
        raise ValueError(f"Failed to load image: {e}")

def preprocess_image(
    image: np.ndarray,
    target_size: Optional[int] = None,
    normalize: bool = True
) -> np.ndarray:
    """
    Preprocess image for quality assessment.
    
    Args:
        image: Input image
        target_size: Target size for resizing
        normalize: Whether to normalize pixel values to [0,1]
        
    Returns:
        Preprocessed image
        
    Raises:
        ValueError: If image is invalid
    """
    is_valid, error = validate_image_data(image)
    if not is_valid:
        raise ValueError(error)
        
    # Convert to float32 for processing
    img = image.astype(np.float32)
    
    # Resize if needed
    if target_size:
        img = resize_image(img, target_size)
        
    # Normalize to [0,1]
    if normalize:
        img /= 255.0
        
    return img

def resize_image(
    image: np.ndarray,
    target_size: int = DEFAULT_IMAGE_SIZE,
    keep_aspect: bool = True
) -> np.ndarray:
    """
    Resize image while optionally maintaining aspect ratio.
    
    Args:
        image: Input image
        target_size: Target size (for longer edge)
        keep_aspect: Whether to maintain aspect ratio
        
    Returns:
        Resized image
    """
    h, w = image.shape[:2]
    
    if keep_aspect:
        # Scale to target size while keeping aspect ratio
        if h > w:
            new_h = target_size
            new_w = int(round(w * target_size / h))
        else:
            new_w = target_size
            new_h = int(round(h * target_size / w))
    else:
        new_h = new_w = target_size
        
    return cv2.resize(
        image,
        (new_w, new_h),
        interpolation=cv2.INTER_AREA
    )

def center_crop(
    image: np.ndarray,
    target_size: Tuple[int, int]
) -> np.ndarray:
    """
    Perform center crop on image.
    
    Args:
        image: Input image
        target_size: Target size as (height, width)
        
    Returns:
        Cropped image
    """
    h, w = image.shape[:2]
    th, tw = target_size
    
    # Calculate crop coordinates
    i = int(round((h - th) / 2.))
    j = int(round((w - tw) / 2.))
    
    return image[i:i+th, j:j+tw]

def random_crop(
    image: np.ndarray,
    target_size: Tuple[int, int],
    seed: Optional[int] = None
) -> np.ndarray:
    """
    Perform random crop on image.
    
    Args:
        image: Input image
        target_size: Target size as (height, width)
        seed: Random seed for reproducibility
        
    Returns:
        Cropped image
    """
    if seed is not None:
        np.random.seed(seed)
        
    h, w = image.shape[:2]
    th, tw = target_size
    
    # Calculate random crop coordinates
    i = np.random.randint(0, h - th + 1)
    j = np.random.randint(0, w - tw + 1)
    
    return image[i:i+th, j:j+tw]

def adjust_gamma(image: np.ndarray, gamma: float = 1.0) -> np.ndarray:
    """
    Adjust image gamma.
    
    Args:
        image: Input image
        gamma: Gamma correction factor
        
    Returns:
        Gamma-corrected image
    """
    # Build lookup table
    invGamma = 1.0 / gamma
    table = np.array([
        ((i / 255.0) ** invGamma) * 255 for i in range(256)
    ]).astype(np.uint8)
    
    return cv2.LUT(image, table)