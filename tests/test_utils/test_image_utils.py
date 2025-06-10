"""
Tests for image utility functions.
"""

import pytest
import numpy as np
from PIL import Image
from iqa_server.utils.image_utils import (
    load_image,
    preprocess_image,
    resize_image,
    center_crop,
    random_crop,
    adjust_gamma
)
from iqa_server.core.constants import DEFAULT_IMAGE_SIZE

@pytest.fixture
def sample_array():
    """Create a sample numpy array representing an RGB image."""
    return np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)

def test_load_image(sample_image_path):
    """Test image loading functionality."""
    img = load_image(sample_image_path)
    assert isinstance(img, np.ndarray)
    assert img.ndim == 3
    assert img.dtype == np.uint8
    
    with pytest.raises(ValueError):
        load_image("nonexistent.jpg")

def test_preprocess_image(sample_array):
    """Test image preprocessing."""
    # Test with normalization
    processed = preprocess_image(sample_array, normalize=True)
    assert processed.dtype == np.float32
    assert 0 <= processed.min() <= processed.max() <= 1
    
    # Test with resizing
    processed = preprocess_image(sample_array, target_size=64)
    assert processed.shape[:2] == (64, 64)

def test_resize_image(sample_array):
    """Test image resizing."""
    # Test with aspect ratio preservation
    resized = resize_image(sample_array, target_size=64, keep_aspect=True)
    assert max(resized.shape[:2]) == 64
    
    # Test without aspect ratio preservation
    resized = resize_image(sample_array, target_size=64, keep_aspect=False)
    assert resized.shape[:2] == (64, 64)

def test_center_crop(sample_array):
    """Test center cropping."""
    target_size = (50, 50)
    cropped = center_crop(sample_array, target_size)
    assert cropped.shape[:2] == target_size
    
    # Center crop should be deterministic
    cropped2 = center_crop(sample_array, target_size)
    np.testing.assert_array_equal(cropped, cropped2)

def test_random_crop(sample_array):
    """Test random cropping."""
    target_size = (50, 50)
    
    # Test with fixed seed for reproducibility
    crop1 = random_crop(sample_array, target_size, seed=42)
    crop2 = random_crop(sample_array, target_size, seed=42)
    assert crop1.shape[:2] == target_size
    np.testing.assert_array_equal(crop1, crop2)
    
    # Test that different seeds give different crops
    crop3 = random_crop(sample_array, target_size, seed=43)
    assert not np.array_equal(crop1, crop3)

def test_adjust_gamma(sample_array):
    """Test gamma adjustment."""
    # Test gamma = 1 (no change)
    adjusted = adjust_gamma(sample_array, gamma=1.0)
    np.testing.assert_array_equal(sample_array, adjusted)
    
    # Test gamma correction
    adjusted = adjust_gamma(sample_array, gamma=2.0)
    assert adjusted.dtype == sample_array.dtype
    assert adjusted.shape == sample_array.shape
    
    # Values should be different but in valid range
    assert adjusted.min() >= 0
    assert adjusted.max() <= 255
    assert not np.array_equal(sample_array, adjusted)
