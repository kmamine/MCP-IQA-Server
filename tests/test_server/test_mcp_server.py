"""
Tests for the MCP server implementation.
"""

import pytest
from pathlib import Path
import json
from iqa_server.server.mcp_server import IQAServer
from iqa_server.core.config import Config
from iqa_server.core.exceptions import InvalidInputError

@pytest.fixture
async def server():
    """Create and initialize a test server instance."""
    server = IQAServer()
    await server.startup()
    yield server
    await server.shutdown()

def test_get_tools(server):
    """Test tool registration and retrieval."""
    tools = server.get_tools()
    assert len(tools) > 0
    
    # Check essential tools are present
    tool_names = {tool.name for tool in tools}
    assert "assess_image_quality" in tool_names
    assert "batch_assessment" in tool_names
    assert "get_available_metrics" in tool_names
    assert "get_metric_interpretation" in tool_names

@pytest.mark.asyncio
async def test_assess_image_quality(server, sample_image_path):
    """Test single image quality assessment."""
    result = await server.handle_tool_call({
        "name": "assess_image_quality",
        "parameters": {
            "image_path": str(sample_image_path),
            "metrics": ["brisque", "niqe"]  # No-reference metrics
        }
    })
    
    assert "scores" in result
    assert "metadata" in result
    assert len(result["scores"]) == 2
    assert all(isinstance(score, float) for score in result["scores"].values())

@pytest.mark.asyncio
async def test_batch_assessment(server, sample_image_path, reference_image_path):
    """Test batch image quality assessment."""
    result = await server.handle_tool_call({
        "name": "batch_assessment",
        "parameters": {
            "image_paths": [str(sample_image_path)] * 3,  # Process same image 3 times
            "metrics": ["brisque", "niqe"],
            "reference_paths": [str(reference_image_path)] * 3
        }
    })
    
    assert isinstance(result, list)
    assert len(result) == 3
    for item in result:
        assert "scores" in item
        assert "metadata" in item
        assert len(item["scores"]) == 2

@pytest.mark.asyncio
async def test_get_available_metrics(server):
    """Test metric information retrieval."""
    result = await server.handle_tool_call({
        "name": "get_available_metrics",
        "parameters": {}
    })
    
    assert "fr_metrics" in result
    assert "nr_metrics" in result
    assert "all_metrics" in result
    assert isinstance(result["fr_metrics"], list)
    assert isinstance(result["nr_metrics"], list)
    assert len(result["all_metrics"]) == len(result["fr_metrics"]) + len(result["nr_metrics"])

@pytest.mark.asyncio
async def test_get_metric_interpretation(server):
    """Test metric interpretation."""
    result = await server.handle_tool_call({
        "name": "get_metric_interpretation",
        "parameters": {
            "metric_name": "brisque",
            "score": 25.5
        }
    })
    
    assert "metric" in result
    assert "interpretation" in result
    assert "better_direction" in result
    assert "ranges" in result

@pytest.mark.asyncio
async def test_error_handling(server):
    """Test error handling for invalid inputs."""
    with pytest.raises(InvalidInputError):
        await server.handle_tool_call({
            "name": "assess_image_quality",
            "parameters": {
                "image_path": "nonexistent.jpg",
                "metrics": ["invalid_metric"]
            }
        })

@pytest.mark.asyncio
async def test_server_cleanup(server):
    """Test server cleanup on shutdown."""
    assert len(server._metrics) > 0  # Should have some metrics initialized
    await server.shutdown()
    assert len(server._metrics) == 0  # Should be cleared after shutdown
