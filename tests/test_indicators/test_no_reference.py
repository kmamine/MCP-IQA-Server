"""
Tests for no-reference image quality assessment metrics.
"""

import pytest
import numpy as np
from iqa_server.indicators.no_reference import (
    BRISQUEIndicator,
    NIQEIndicator,
    PIQIndicator,
    MUSIQIndicator,
    ILNIQEIndicator,
    DBCNNIndicator
)

@pytest.mark.asyncio
async def test_brisque_indicator(sample_image_path):
    """Test BRISQUE metric computation."""
    indicator = BRISQUEIndicator()
    await indicator.initialize()
    
    score = await indicator.compute(sample_image_path)
    assert isinstance(score, float)
    assert 0 <= score <= 100  # Normalized BRISQUE score
    
    await indicator.cleanup()

@pytest.mark.asyncio
async def test_niqe_indicator(sample_image_path):
    """Test NIQE metric computation."""
    indicator = NIQEIndicator()
    await indicator.initialize()
    
    score = await indicator.compute(sample_image_path)
    assert isinstance(score, float)
    assert 0 <= score <= 100  # Normalized NIQE score
    
    await indicator.cleanup()

@pytest.mark.asyncio
async def test_piq_indicator(sample_image_path):
    """Test PIQ metric computation."""
    indicator = PIQIndicator()
    await indicator.initialize()
    
    score = await indicator.compute(sample_image_path)
    assert isinstance(score, float)
    assert 0 <= score <= 100  # Normalized PIQ score
    
    await indicator.cleanup()

@pytest.mark.asyncio
async def test_musiq_indicator(sample_image_path):
    """Test MUSIQ metric computation."""
    indicator = MUSIQIndicator()
    await indicator.initialize()
    
    score = await indicator.compute(sample_image_path)
    assert isinstance(score, float)
    assert 0 <= score <= 100  # Normalized MUSIQ score
    
    await indicator.cleanup()

@pytest.mark.asyncio
async def test_ilniqe_indicator(sample_image_path):
    """Test ILNIQE metric computation."""
    indicator = ILNIQEIndicator()
    await indicator.initialize()
    
    score = await indicator.compute(sample_image_path)
    assert isinstance(score, float)
    assert 0 <= score <= 100  # Normalized ILNIQE score
    
    await indicator.cleanup()

@pytest.mark.asyncio
async def test_dbcnn_indicator(sample_image_path):
    """Test DBCNN metric computation."""
    indicator = DBCNNIndicator()
    await indicator.initialize()
    
    score = await indicator.compute(sample_image_path)
    assert isinstance(score, float)
    assert 0 <= score <= 100  # Normalized DBCNN score
    
    await indicator.cleanup()

@pytest.mark.asyncio
async def test_no_reference_metrics_metadata():
    """Test metadata for no-reference metrics."""
    indicators = [
        (BRISQUEIndicator(), 'BRISQUE'),
        (NIQEIndicator(), 'NIQE'),
        (PIQIndicator(), 'PIQ'),
        (MUSIQIndicator(), 'MUSIQ'),
        (ILNIQEIndicator(), 'ILNIQE'),
        (DBCNNIndicator(), 'DBCNN')
    ]
    
    for indicator, name in indicators:
        metadata = indicator.get_metadata()
        assert metadata['name'] == name
        assert 'description' in metadata
        assert not metadata['requires_reference']  # No-reference metrics
        assert isinstance(metadata['is_initialized'], bool)

@pytest.mark.asyncio
async def test_batch_processing(sample_image_path):
    """Test batch processing for no-reference metrics."""
    indicators = [
        BRISQUEIndicator(),
        NIQEIndicator(),
        PIQIndicator(),
        MUSIQIndicator(),
        ILNIQEIndicator(),
        DBCNNIndicator()
    ]
    
    for indicator in indicators:
        await indicator.initialize()
        
        # Process the same image multiple times to simulate batch
        scores = []
        for _ in range(3):
            score = await indicator.compute(sample_image_path)
            scores.append(score)
            
        # Scores should be consistent for the same image
        assert len(set(scores)) == 1
        
        await indicator.cleanup()

@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling for invalid inputs."""
    indicators = [
        BRISQUEIndicator(),
        NIQEIndicator(),
        PIQIndicator(),
        MUSIQIndicator(),
        ILNIQEIndicator(),
        DBCNNIndicator()
    ]
    
    for indicator in indicators:
        await indicator.initialize()
        
        with pytest.raises(RuntimeError):
            # Should raise error for invalid image path
            await indicator.compute('nonexistent.jpg')
