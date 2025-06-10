"""
Request handlers for the IQA MCP server using PyIQA.
"""

import asyncio
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
import pyiqa
import torch
from ..utils.validation import validate_image_path
from ..utils.performance import monitor, cache
from ..core.exceptions import InvalidInputError, MetricError

def _get_available_metrics(metric_type: str = 'all') -> List[str]:
    """Get available metrics based on type."""
    if metric_type == 'fr':
        return pyiqa.get_fr_metrics()
    elif metric_type == 'nr':
        return pyiqa.get_nr_metrics()
    return pyiqa.get_all_metrics()

@monitor.track("handle_assess_image_quality")
async def handle_assess_image_quality(
    image_path: str,
    metrics: Optional[List[str]] = None,
    reference_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Handle image quality assessment requests using PyIQA metrics.
    
    Args:
        image_path: Path to the input image
        metrics: List of metrics to compute (if None, uses all available metrics)
        reference_path: Path to reference image (required for FR metrics)
        
    Returns:
        Dictionary containing computed metrics and scores
    """
    # Validate inputs
    is_valid, error = validate_image_path(image_path)
    if not is_valid:
        raise InvalidInputError(f"Invalid image path: {error}")
        
    if reference_path:
        is_valid, error = validate_image_path(reference_path)
        if not is_valid:
            raise InvalidInputError(f"Invalid reference image path: {error}")
            
    # Determine which metrics to compute
    if metrics is None:
        if reference_path:
            metrics = pyiqa.get_fr_metrics()
        else:
            metrics = pyiqa.get_nr_metrics()
    
    results = {}
    errors = {}
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Group metrics by whether they require reference
    fr_metrics = [m for m in metrics if m in pyiqa.get_fr_metrics()]
    nr_metrics = [m for m in metrics if m in pyiqa.get_nr_metrics()]
    
    # Check if reference is provided for FR metrics
    if fr_metrics and not reference_path:
        raise InvalidInputError(f"Reference image required for metrics: {fr_metrics}")
    
    # Compute no-reference metrics
    for metric_name in nr_metrics:
        try:
            # Try to get cached result first
            cache_key = f"{metric_name}:{image_path}"
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                results[metric_name] = cached_result
                continue
                
            # Create and compute metric
            metric = pyiqa.create_metric(metric_name, device=device)
            score = float(metric(image_path).cpu().numpy())
            results[metric_name] = score
            cache.put(cache_key, score)
            
        except Exception as e:
            errors[metric_name] = str(e)
            
    # Compute full-reference metrics
    for metric_name in fr_metrics:
        try:
            cache_key = f"{metric_name}:{image_path}:{reference_path}"
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                results[metric_name] = cached_result
                continue
                
            metric = pyiqa.create_metric(metric_name, device=device)
            score = float(metric(image_path, reference_path).cpu().numpy())
            results[metric_name] = score
            cache.put(cache_key, score)
            
        except Exception as e:
            errors[metric_name] = str(e)
              return {
        "scores": results,
        "errors": errors,
        "metadata": {
            "image_path": str(image_path),
            "reference_path": str(reference_path) if reference_path else None,
            "metrics_computed": list(results.keys()),
            "failed_metrics": list(errors.keys())
        }
    }

@monitor.track("handle_batch_assessment")
async def handle_batch_assessment(
    image_paths: List[str],
    metrics: Optional[List[str]] = None,
    reference_paths: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Handle batch image quality assessment requests.
    
    Args:
        image_paths: List of paths to input images
        metrics: List of metrics to compute
        reference_paths: List of paths to reference images (for FR metrics)
        
    Returns:
        List of dictionaries containing results for each image
    """
    if reference_paths and len(reference_paths) != len(image_paths):
        raise InvalidInputError(
            f"Number of reference images ({len(reference_paths)}) must match "
            f"number of test images ({len(image_paths)})"
        )
        
    async def process_single_image(idx: int) -> Dict[str, Any]:
        """Process a single image from the batch."""
        image_path = image_paths[idx]
        reference_path = reference_paths[idx] if reference_paths else None
        
        try:
            return await handle_assess_image_quality(
                image_path=image_path,
                metrics=metrics,
                reference_path=reference_path
            )
        except Exception as e:
            return {
                "scores": {},
                "errors": {"assessment_error": str(e)},
                "metadata": {
                    "image_path": str(image_path),
                    "reference_path": str(reference_path) if reference_path else None,
                    "metrics_computed": [],
                    "failed_metrics": ["all"]
                }
            }
    
    # Process images concurrently
    tasks = [process_single_image(i) for i in range(len(image_paths))]
    results = await asyncio.gather(*tasks)
    
    return results

@monitor.track("handle_get_metric_info")
async def handle_get_metric_info(metric_name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific metric.
    
    Args:
        metric_name: Name of the metric
        
    Returns:
        Dictionary containing metric information
    """
    if metric_name not in pyiqa.get_all_metrics():
        raise InvalidInputError(f"Unknown metric: {metric_name}")
        
    info = pyiqa.get_metric_info(metric_name)
    metric_type = "Full-reference" if metric_name in pyiqa.get_fr_metrics() else "No-reference"
    
    return {
        "name": metric_name,
        "type": metric_type,
        "info": info,
        "implementation": f"PyIQA {pyiqa.__version__}"
    }
    # Load and validate image
    image = load_image(image_path)
    if not validate_image(image):
        raise ValueError("Invalid image format or corrupted image file")

    # Compute requested metrics
    results = {}
    for metric in metrics:
        if metric not in indicators:
            raise ValueError(f"Unknown metric: {metric}")
        
        indicator = indicators[metric]
        score = await indicator.compute(image)
        results[metric] = float(score)  # Convert numpy types to Python native types
        
    return {
        "scores": results,
        "metadata": {
            "image_size": image.shape,
            "metrics_computed": metrics
        }
    }

async def handle_batch_assessment(
    image_paths: List[str],
    metrics: List[str],
    indicators: Dict[str, BaseIndicator]
) -> List[Dict[str, Any]]:
    """
    Handle batch image quality assessment requests.
    
    Args:
        image_paths: List of paths to input images
        metrics: List of metrics to compute
        indicators: Dictionary of available indicators
        
    Returns:
        List of dictionaries containing computed metrics for each image
    """
    results = []
    for image_path in image_paths:
        try:
            result = await handle_assess_image_quality(image_path, metrics, indicators)
            results.append({
                "image_path": image_path,
                "success": True,
                **result
            })
        except Exception as e:
            results.append({
                "image_path": image_path,
                "success": False,
                "error": str(e)
            })
    return results