"""
Pytest configuration and fixtures.
"""

import os
import pytest
from pathlib import Path
import numpy as np
from PIL import Image
import torch

@pytest.fixture
def sample_image_path(tmp_path) -> Path:
    """Create a sample test image."""
    image_path = tmp_path / "test_image.jpg"
    # Create a simple RGB test image
    img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    Image.fromarray(img).save(image_path)
    return image_path

@pytest.fixture
def reference_image_path(tmp_path) -> Path:
    """Create a sample reference image."""
    image_path = tmp_path / "reference_image.jpg"
    # Create a slightly different RGB image
    img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    Image.fromarray(img).save(image_path)
    return image_path

@pytest.fixture
def device():
    """Get available device (CPU/GPU)."""
    return torch.device('cuda' if torch.cuda.is_available() else 'cpu')
