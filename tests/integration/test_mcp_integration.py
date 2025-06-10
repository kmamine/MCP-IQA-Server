"""
Integration tests for the IQA server.
"""

import pytest
import asyncio
import numpy as np
from pathlib import Path
from PIL import Image
import torch
from iqa_server.server.mcp_server import IQAServer
from iqa_server.core.config import Config
from iqa_server.utils.validation import validate_image_path
from iqa_server.core.constants import DEFAULT_FR_METRICS, DEFAULT_NR_METRICS

@pytest.fixture
async def server():
    """Create and initialize a test server instance."""
    server = IQAServer()
    await server.startup()
    yield server
    await server.shutdown()

@pytest.mark.asyncio
async def test_full_quality_assessment_workflow(server, sample_image_path, reference_image_path):
    """Test a complete image quality assessment workflow."""
    # 1. Get available metrics
    metrics_info = await server.handle_tool_call({
        "name": "get_available_metrics",
        "parameters": {}
    })
    
    assert len(metrics_info["fr_metrics"]) > 0
    assert len(metrics_info["nr_metrics"]) > 0
    
    # 2. Assess image quality without reference
    no_ref_result = await server.handle_tool_call({
        "name": "assess_image_quality",
        "parameters": {
            "image_path": str(sample_image_path),
            "metrics": DEFAULT_NR_METRICS
        }
    })
    
    assert "scores" in no_ref_result
    assert len(no_ref_result["scores"]) == len(DEFAULT_NR_METRICS)
    
    # 3. Assess image quality with reference
    full_ref_result = await server.handle_tool_call({
        "name": "assess_image_quality",
        "parameters": {
            "image_path": str(sample_image_path),
            "reference_path": str(reference_image_path),
            "metrics": DEFAULT_FR_METRICS
        }
    })
    
    assert "scores" in full_ref_result
    assert len(full_ref_result["scores"]) == len(DEFAULT_FR_METRICS)
    
    # 4. Get interpretations for scores
    for metric, score in {**no_ref_result["scores"], **full_ref_result["scores"]}.items():
        interp_result = await server.handle_tool_call({
            "name": "get_metric_interpretation",
            "parameters": {
                "metric_name": metric,
                "score": score
            }
        })
        
        assert "interpretation" in interp_result
        assert "better_direction" in interp_result
        assert "ranges" in interp_result

@pytest.mark.asyncio
async def test_batch_processing_workflow(server, tmp_path):
    """Test batch processing workflow."""
    # Create multiple test images
    image_paths = []
    ref_paths = []
    for i in range(3):
        # Test image
        img_path = tmp_path / f"test_{i}.jpg"
        img = Image.fromarray(np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8))
        img.save(img_path)
        image_paths.append(str(img_path))
        
        # Reference image
        ref_path = tmp_path / f"ref_{i}.jpg"
        ref = Image.fromarray(np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8))
        ref.save(ref_path)
        ref_paths.append(str(ref_path))
    
    # Test batch processing with different metric combinations
    test_cases = [
        (DEFAULT_NR_METRICS, None),  # No-reference metrics
        (DEFAULT_FR_METRICS, ref_paths),  # Full-reference metrics
        (DEFAULT_NR_METRICS + DEFAULT_FR_METRICS, ref_paths)  # Combined metrics
    ]
    
    for metrics, refs in test_cases:
        result = await server.handle_tool_call({
            "name": "batch_assessment",
            "parameters": {
                "image_paths": image_paths,
                "metrics": metrics,
                "reference_paths": refs
            }
        })
        
        assert len(result) == len(image_paths)
        for item in result:
            assert "scores" in item
            assert "metadata" in item
            assert len(item["scores"]) == len(metrics)

@pytest.mark.asyncio
async def test_error_handling_and_recovery(server, sample_image_path):
    """Test error handling and recovery in realistic scenarios."""
    # 1. Test with invalid image path
    try:
        await server.handle_tool_call({
            "name": "assess_image_quality",
            "parameters": {
                "image_path": "nonexistent.jpg",
                "metrics": DEFAULT_NR_METRICS
            }
        })
    except Exception as e:
        assert "not found" in str(e).lower()
    
    # 2. Test with invalid metric
    try:
        await server.handle_tool_call({
            "name": "assess_image_quality",
            "parameters": {
                "image_path": str(sample_image_path),
                "metrics": ["invalid_metric"]
            }
        })
    except Exception as e:
        assert "unknown" in str(e).lower()
    
    # 3. Verify server still works after errors
    result = await server.handle_tool_call({
        "name": "assess_image_quality",
        "parameters": {
            "image_path": str(sample_image_path),
            "metrics": DEFAULT_NR_METRICS
        }
    })
    
    assert "scores" in result
    assert len(result["scores"]) == len(DEFAULT_NR_METRICS)
