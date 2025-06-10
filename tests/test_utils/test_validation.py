"""
Tests for validation utilities.
"""

import pytest
from pathlib import Path
import numpy as np
from PIL import Image
from iqa_server.utils.validation import (
    validate_image_path,
    validate_image_data,
    validate_metrics,
    validate_score,
    validate_batch_size
)
from iqa_server.core.constants import SUPPORTED_FORMATS, MAX_IMAGE_SIZE

def test_validate_image_path(tmp_path):
    """Test image path validation."""
    # Test valid image
    valid_path = tmp_path / "valid.jpg"
    img = Image.fromarray(np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8))
    img.save(valid_path)
    is_valid, error = validate_image_path(valid_path)
    assert is_valid
    assert error is None
    
    # Test nonexistent file
    is_valid, error = validate_image_path(tmp_path / "nonexistent.jpg")
    assert not is_valid
    assert "not found" in error.lower()
    
    # Test unsupported format
    invalid_path = tmp_path / "invalid.xyz"
    is_valid, error = validate_image_path(invalid_path)
    assert not is_valid
    assert "unsupported" in error.lower()

def test_validate_image_data():
    """Test image data validation."""
    # Valid RGB image
    valid_img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    is_valid, error = validate_image_data(valid_img)
    assert is_valid
    assert error is None
    
    # Invalid dimensions
    invalid_img = np.random.rand(100)  # 1D array
    is_valid, error = validate_image_data(invalid_img)
    assert not is_valid
    assert "dimensions" in error.lower()
    
    # Invalid channels
    invalid_img = np.random.rand(100, 100, 5)  # 5 channels
    is_valid, error = validate_image_data(invalid_img)
    assert not is_valid
    assert "channels" in error.lower()
    
    # Too large
    large_img = np.random.randint(0, 255, (MAX_IMAGE_SIZE + 1, MAX_IMAGE_SIZE + 1, 3), dtype=np.uint8)
    is_valid, error = validate_image_data(large_img)
    assert not is_valid
    assert "dimensions exceed" in error.lower()

def test_validate_metrics():
    """Test metric validation."""
    available_metrics = ['psnr', 'ssim', 'lpips']
    
    # Valid metrics
    is_valid, error = validate_metrics(['psnr', 'ssim'], available_metrics)
    assert is_valid
    assert error is None
    
    # Empty metrics list
    is_valid, error = validate_metrics([], available_metrics)
    assert not is_valid
    assert "no metrics" in error.lower()
    
    # Unknown metrics
    is_valid, error = validate_metrics(['unknown'], available_metrics)
    assert not is_valid
    assert "unknown metrics" in error.lower()

def test_validate_score():
    """Test score validation."""
    # Valid scores
    is_valid, error = validate_score(50.0, 'psnr')
    assert is_valid
    assert error is None
    
    # Invalid type
    is_valid, error = validate_score("50", 'psnr')
    assert not is_valid
    assert "type" in error.lower()
    
    # Out of range
    is_valid, error = validate_score(150.0, 'psnr')
    assert not is_valid
    assert "range" in error.lower()

def test_validate_batch_size():
    """Test batch size validation."""
    # Valid batch size
    is_valid, error = validate_batch_size(50)
    assert is_valid
    assert error is None
    
    # Invalid type
    is_valid, error = validate_batch_size(1.5)
    assert not is_valid
    assert "integer" in error.lower()
    
    # Too small
    is_valid, error = validate_batch_size(0)
    assert not is_valid
    assert "positive" in error.lower()
    
    # Too large
    is_valid, error = validate_batch_size(1000)
    assert not is_valid
    assert "exceeds maximum" in error.lower()
