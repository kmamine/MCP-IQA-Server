#!/usr/bin/env python3
"""
Tests for the IQA MCP Server
"""

import json
import pytest
from mcp.types import AnyUrl, Resource, TextContent
from iqa_server import IQAServer
from iqa_server.models import model_database

@pytest.fixture
async def server():
    """Create a server instance for testing."""
    return IQAServer()

class TestModelDatabase:
    """Test suite for the IQA Model Database."""
    
    def test_get_all_models(self):
        """Test retrieving all models."""
        models = model_database.get_all_models()
        assert "fr_methods" in models
        assert "nr_methods" in models
        assert "specific_methods" in models
    
    def test_get_fr_models(self):
        """Test retrieving FR models."""
        fr_models = model_database.get_fr_models()
        assert all(model["type"] == "FR" for model in fr_models.values())
    
    def test_get_nr_models(self):
        """Test retrieving NR models."""
        nr_models = model_database.get_nr_models()
        assert all(model["type"] == "NR" for model in nr_models.values())
    
    def test_get_specific_models(self):
        """Test retrieving specific models."""
        specific_models = model_database.get_specific_models()
        assert all(model["type"] == "Specific" for model in specific_models.values())
    
    def test_search_models(self):
        """Test model search functionality."""
        # Test searching by name
        ssim_results = model_database.search_models("ssim")
        assert any("ssim" in model["key"] for model in ssim_results)
        
        # Test searching by type
        fr_results = model_database.search_models("", "FR")
        assert all(model["info"]["type"] == "FR" for model in fr_results)
        
        # Test searching by category
        color_results = model_database.search_models("color")
        assert any("Color IQA" in model["info"]["category"] for model in color_results)
    
    def test_get_model_info(self):
        """Test retrieving specific model information."""
        # Test existing model
        lpips_info = model_database.get_model_info("lpips")
        assert lpips_info["type"] == "FR"
        assert "lpips" in lpips_info["names"]
        
        # Test non-existent model
        empty_info = model_database.get_model_info("non_existent_model")
        assert empty_info == {}
    
    def test_list_model_names(self):
        """Test listing model names."""
        # Test all models
        all_names = model_database.list_model_names()
        assert len(all_names) > 0
        assert isinstance(all_names, list)
        
        # Test FR models
        fr_names = model_database.list_model_names("FR")
        assert all(name in all_names for name in fr_names)
        
        # Test sorting
        assert fr_names == sorted(fr_names)

class TestIQAServer:
    """Test suite for the IQA MCP Server."""
    
    @pytest.mark.asyncio
    async def test_list_resources(self, server):
        """Test that list_resources returns the expected resources."""
        resources = await server.server.list_resources()()
        assert len(resources) == 4
        assert all(isinstance(r, Resource) for r in resources)
        assert any(r.uri == "iqa://models/all" for r in resources)
        
        # Test resource properties
        for resource in resources:
            assert resource.mimeType == "application/json"
            assert resource.description is not None
            assert resource.name is not None
            assert resource.uri.startswith("iqa://models/")

    @pytest.mark.asyncio
    async def test_read_resource(self, server):
        """Test that read_resource returns valid JSON for all resources."""
        uris = [
            "iqa://models/all",
            "iqa://models/fr",
            "iqa://models/nr",
            "iqa://models/specific"
        ]
        
        for uri in uris:
            result = await server.server.read_resource()(AnyUrl(uri))
            data = json.loads(result)
            assert isinstance(data, dict)
            
            # Test data validity
            if uri == "iqa://models/fr":
                assert all(model["type"] == "FR" for model in data.values())
            elif uri == "iqa://models/nr":
                assert all(model["type"] == "NR" for model in data.values())
            elif uri == "iqa://models/specific":
                assert all(model["type"] == "Specific" for model in data.values())

    @pytest.mark.asyncio
    async def test_list_tools(self, server):
        """Test that list_tools returns the expected tools."""
        tools = await server.server.list_tools()()
        assert len(tools) == 4
        tool_names = {tool.name for tool in tools}
        assert tool_names == {"search_models", "get_model_info", "list_model_names", "get_usage_example"}

    @pytest.mark.asyncio
    async def test_call_tool_search_models(self, server):
        """Test the search_models tool."""
        # Test search by name
        result = await server.server.call_tool()("search_models", {"query": "ssim"})
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        data = json.loads(result[0].text)
        assert len(data) > 0
        assert any("ssim" in model["key"] for model in data)
        
        # Test search by type
        result = await server.server.call_tool()("search_models", {"query": "", "model_type": "FR"})
        data = json.loads(result[0].text)
        assert all(model["info"]["type"] == "FR" for model in data)

    @pytest.mark.asyncio
    async def test_call_tool_get_model_info(self, server):
        """Test the get_model_info tool."""
        # Test existing model
        result = await server.server.call_tool()("get_model_info", {"model_name": "lpips"})
        assert len(result) == 1
        data = json.loads(result[0].text)
        assert data["type"] == "FR"
        assert "lpips" in data["names"]
        
        # Test non-existent model
        result = await server.server.call_tool()("get_model_info", {"model_name": "non_existent"})
        assert "not found" in result[0].text

    @pytest.mark.asyncio
    async def test_call_tool_list_model_names(self, server):
        """Test the list_model_names tool."""
        # Test all models
        result = await server.server.call_tool()("list_model_names", {})
        names = json.loads(result[0].text)
        assert isinstance(names, list)
        assert len(names) > 0
        
        # Test FR models
        result = await server.server.call_tool()("list_model_names", {"model_type": "FR"})
        fr_names = json.loads(result[0].text)
        assert all(name in names for name in fr_names)

    @pytest.mark.asyncio
    async def test_call_tool_get_usage_example(self, server):
        """Test the get_usage_example tool."""
        result = await server.server.call_tool()("get_usage_example", {"model_name": "ssim"})
        assert len(result) == 1
        example = result[0].text
        assert "import pyiqa" in example
        assert "ssim" in example
        assert "metric = pyiqa.create_metric('ssim')" in example
