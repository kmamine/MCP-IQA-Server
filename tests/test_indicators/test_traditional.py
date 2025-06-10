"""
Tests for traditional image quality assessment metrics.
"""

import pytest
import numpy as np
from iqa_server.indicators.traditional import (
    PSNRIndicator,
    SSIMIndicator,
    MSEIndicator,
    FIDIndicator,
    LPIPSIndicator
)

@pytest.mark.asyncio
async def test_psnr_indicator(sample_image_path, reference_image_path):
    """Test PSNR metric computation."""
    indicator = PSNRIndicator()
    await indicator.initialize()
    
    score = await indicator.compute(sample_image_path, reference_image_path)
    assert isinstance(score, float)
    assert score >= 0  # PSNR should always be non-negative
    
    await indicator.cleanup()

@pytest.mark.asyncio
async def test_ssim_indicator(sample_image_path, reference_image_path):
    """Test SSIM metric computation."""
    indicator = SSIMIndicator()
    await indicator.initialize()
    
    score = await indicator.compute(sample_image_path, reference_image_path)
    assert isinstance(score, float)
    assert 0 <= score <= 100  # Normalized SSIM score
    
    await indicator.cleanup()

@pytest.mark.asyncio
async def test_mse_indicator(sample_image_path, reference_image_path):
    """Test MSE metric computation."""
    indicator = MSEIndicator()
    await indicator.initialize()
    
    score = await indicator.compute(sample_image_path, reference_image_path)
    assert isinstance(score, float)
    assert score >= 0  # MSE should always be non-negative
    
    await indicator.cleanup()

@pytest.mark.asyncio
async def test_lpips_indicator(sample_image_path, reference_image_path):
    """Test LPIPS metric computation."""
    # Test with different network backbones
    for net_type in ['alex', 'vgg']:
        indicator = LPIPSIndicator(net_type=net_type)
        await indicator.initialize()
        
        score = await indicator.compute(sample_image_path, reference_image_path)
        assert isinstance(score, float)
        assert 0 <= score <= 100  # Normalized LPIPS score
        
        await indicator.cleanup()

@pytest.mark.asyncio
async def test_fid_indicator(sample_image_path, reference_image_path):
    """Test FID metric computation."""
    indicator = FIDIndicator()
    await indicator.initialize()
    
    score = await indicator.compute(sample_image_path, reference_image_path)
    assert isinstance(score, float)
    assert score >= 0  # FID should always be non-negative
    
    await indicator.cleanup()

@pytest.mark.asyncio
async def test_traditional_metrics_metadata():
    """Test metadata for traditional metrics."""
    indicators = [
        (PSNRIndicator(), 'PSNR'),
        (SSIMIndicator(), 'SSIM'),
        (MSEIndicator(), 'MSE'),
        (FIDIndicator(), 'FID'),
        (LPIPSIndicator(), 'LPIPS')
    ]
    
    for indicator, name in indicators:
        metadata = indicator.get_metadata()
        assert metadata['name'] == name
        assert 'description' in metadata
        assert 'requires_reference' in metadata
        assert isinstance(metadata['is_initialized'], bool)

@pytest.mark.asyncio
async def test_invalid_inputs():
    """Test error handling for invalid inputs."""
    indicators = [PSNRIndicator(), SSIMIndicator(), MSEIndicator(), FIDIndicator(), LPIPSIndicator()]
    
    for indicator in indicators:
        await indicator.initialize()
        
        with pytest.raises(ValueError):
            # Should raise error when reference is required but not provided
            await indicator.compute('test.jpg')
            
        with pytest.raises(RuntimeError):
            # Should raise error for invalid image paths
            await indicator.compute('invalid1.jpg', 'invalid2.jpg')
