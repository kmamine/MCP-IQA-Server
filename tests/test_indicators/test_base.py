"""
Tests for the base indicator functionality.
"""

import pytest
import numpy as np
import torch
import pyiqa
from iqa_server.indicators.base import BaseIndicator

@pytest.mark.asyncio
async def test_base_indicator_initialization():
    """Test basic initialization of BaseIndicator."""
    indicator = BaseIndicator('psnr')  # Use PSNR as a test metric
    assert indicator.name == 'psnr'
    assert indicator.iqa_metric is None
    assert not indicator._is_initialized
    assert isinstance(indicator.device, torch.device)

@pytest.mark.asyncio
async def test_base_indicator_initialize():
    """Test initialization of PyIQA metric."""
    indicator = BaseIndicator('psnr')
    await indicator.initialize()
    assert indicator._is_initialized
    assert indicator.iqa_metric is not None

@pytest.mark.asyncio
async def test_compute_no_reference_metric(sample_image_path):
    """Test computing a no-reference metric."""
    indicator = BaseIndicator('niqe')  # NIQE doesn't require reference
    await indicator.initialize()
    score = await indicator.compute(sample_image_path)
    assert isinstance(score, float)
    assert 0 <= score <= 100  # Normalized score

@pytest.mark.asyncio
async def test_compute_reference_metric(sample_image_path, reference_image_path):
    """Test computing a full-reference metric."""
    indicator = BaseIndicator('psnr')  # PSNR requires reference
    await indicator.initialize()
    score = await indicator.compute(sample_image_path, reference_image_path)
    assert isinstance(score, float)
    assert score >= 0  # PSNR is always non-negative

@pytest.mark.asyncio
async def test_cleanup():
    """Test cleanup of resources."""
    indicator = BaseIndicator('psnr')
    await indicator.initialize()
    await indicator.cleanup()
    assert indicator.iqa_metric is None

def test_get_metadata():
    """Test metadata retrieval."""
    indicator = BaseIndicator('psnr')
    metadata = indicator.get_metadata()
    assert isinstance(metadata, dict)
    assert 'name' in metadata
    assert 'description' in metadata
    assert 'requires_reference' in metadata

@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling for invalid inputs."""
    indicator = BaseIndicator('psnr')
    await indicator.initialize()
    
    with pytest.raises(ValueError):
        # PSNR requires reference, should raise error without one
        await indicator.compute('nonexistent.jpg')
        
    with pytest.raises(RuntimeError):
        # Should raise error for invalid image path
        await indicator.compute('invalid.jpg', 'ref.jpg')
