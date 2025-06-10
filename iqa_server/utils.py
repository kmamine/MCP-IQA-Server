"""
IQA Server Utilities Module

Contains utility functions for working with IQA models and the MCP server.
"""

from typing import Dict, Any, Optional
import json

def format_model_info(model_info: Dict[str, Any], include_names: bool = True) -> str:
    """Format model information into a readable string."""
    parts = []
    
    # Add type and category
    parts.append(f"Type: {model_info['type']}")
    if "category" in model_info:
        parts.append(f"Category: {model_info['category']}")
    
    # Add names if requested
    if include_names and "names" in model_info:
        parts.append(f"Names: {', '.join(model_info['names'])}")
    
    # Add description
    if "description" in model_info:
        parts.append(f"Description: {model_info['description']}")
    
    # Add any additional notes
    if "note" in model_info:
        parts.append(f"Note: {model_info['note']}")
    
    if "paper_info" in model_info:
        parts.append(f"Paper Info: {model_info['paper_info']}")
    
    if "backward_support" in model_info:
        parts.append(f"Backward Support: {'Yes' if model_info['backward_support'] else 'No'}")
    
    return "\n".join(parts)

def generate_model_comparison(model1_info: Dict[str, Any], model2_info: Dict[str, Any]) -> str:
    """Generate a comparison between two IQA models."""
    comparison = ["Model Comparison:"]
    
    # Compare types
    comparison.append(f"\nTypes:")
    comparison.append(f"- Model 1: {model1_info['type']}")
    comparison.append(f"- Model 2: {model2_info['type']}")
    
    # Compare categories
    if "category" in model1_info or "category" in model2_info:
        comparison.append(f"\nCategories:")
        comparison.append(f"- Model 1: {model1_info.get('category', 'N/A')}")
        comparison.append(f"- Model 2: {model2_info.get('category', 'N/A')}")
    
    # Compare descriptions
    comparison.append(f"\nDescriptions:")
    comparison.append(f"- Model 1: {model1_info['description']}")
    comparison.append(f"- Model 2: {model2_info['description']}")
    
    # Compare additional properties
    for prop in ["note", "paper_info", "backward_support"]:
        if prop in model1_info or prop in model2_info:
            comparison.append(f"\n{prop.title()}:")
            comparison.append(f"- Model 1: {model1_info.get(prop, 'N/A')}")
            comparison.append(f"- Model 2: {model2_info.get(prop, 'N/A')}")
    
    return "\n".join(comparison)

def format_search_results(results: list[Dict[str, Any]], compact: bool = False) -> str:
    """Format search results into a readable string."""
    if not results:
        return "No models found matching the search criteria."
    
    formatted = ["Search Results:"]
    
    for result in results:
        model_key = result["key"]
        model_info = result["info"]
        
        if compact:
            formatted.append(f"\n{model_key}: {model_info['description']}")
        else:
            formatted.append(f"\n{model_key}:")
            for line in format_model_info(model_info).split("\n"):
                formatted.append(f"  {line}")
    
    return "\n".join(formatted)

def generate_usage_example(model_name: str, model_info: Optional[Dict[str, Any]] = None) -> str:
    """Generate a usage example for a specific model."""
    example = [f"# Basic usage example for {model_name}"]
    example.append("import pyiqa")
    example.append(f"\n# Create the metric")
    example.append(f"metric = pyiqa.create_metric('{model_name}')")
    
    example.append(f"\n# Get score range (if available)")
    example.append("try:")
    example.append(f"    print(f\"Score range for {model_name}: {{metric.score_range}}\")")
    example.append("except:")
    example.append("    print(\"Score range not available for this metric\")")
    
    if model_info and model_info["type"] == "FR":
        example.append(f"\n# For Full Reference methods:")
        example.append("score = metric(img_test, img_ref)")
        example.append("\n# For batch processing:")
        example.append("scores = metric(batch_test, batch_ref)")
    else:
        example.append(f"\n# For No Reference methods:")
        example.append("score = metric(img_test)")
        example.append("\n# For batch processing:")
        example.append("scores = metric(batch_imgs)")
    
    return "\n".join(example)
