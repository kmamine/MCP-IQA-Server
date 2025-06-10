"""
Initialize and register all available PyIQA indicators.
This module provides access to various image quality assessment metrics implemented
through the PyIQA library.
"""

from typing import Dict, List, Optional, Type
import pyiqa

from .base import BaseIndicator
from .traditional import (
    PSNRIndicator, SSIMIndicator, MSEIndicator,
    FIDIndicator, LPIPSIndicator
)
from .no_reference import (
    BRISQUEIndicator, NIQEIndicator, PIQIndicator,
    MUSIQIndicator, ILNIQEIndicator, DBCNNIndicator
)
from .interpretations import get_interpretation, INTERPRETATIONS

# Registry of available indicators
INDICATOR_REGISTRY: Dict[str, Type[BaseIndicator]] = {
    # Traditional metrics
    'psnr': PSNRIndicator,
    'ssim': SSIMIndicator,
    'mse': MSEIndicator,
    'fid': FIDIndicator,
    'lpips': LPIPSIndicator,
    
    # No-reference metrics
    'brisque': BRISQUEIndicator,
    'niqe': NIQEIndicator,
    'piq': PIQIndicator,
    'musiq': MUSIQIndicator,
    'ilniqe': ILNIQEIndicator,
    'dbcnn': DBCNNIndicator
}

def get_available_indicators(metric_type: Optional[str] = None) -> Dict[str, BaseIndicator]:
    """
    Get dictionary of available indicators, optionally filtered by type.
    
    Args:
        metric_type: Optional type filter ('fr' for full-reference,
                    'nr' for no-reference, or None for all)
    
    Returns:
        Dictionary mapping indicator names to initialized instances
    """
    if metric_type == 'fr':
        metrics = set(pyiqa.get_fr_metrics())
    elif metric_type == 'nr':
        metrics = set(pyiqa.get_nr_metrics())
    else:
        metrics = set(INDICATOR_REGISTRY.keys())
        
    return {
        name: cls() for name, cls in INDICATOR_REGISTRY.items()
        if name in metrics
    }

def get_indicator_metadata() -> List[Dict]:
    """
    Get metadata for all available indicators.
    
    Returns:
        List of dictionaries containing indicator metadata
    """
    metadata = []
    for name, cls in INDICATOR_REGISTRY.items():
        instance = cls()
        meta = instance.get_metadata()
        meta['id'] = name
        if name in INTERPRETATIONS:
            meta['interpretation'] = get_interpretation(name)
        metadata.append(meta)
    return metadata

async def initialize_indicators(
    metrics: Optional[List[str]] = None,
    device: Optional[str] = None
) -> Dict[str, BaseIndicator]:
    """
    Initialize requested indicators.
    
    Args:
        metrics: List of metric names to initialize (None for all)
        device: Optional device specification ('cuda' or 'cpu')
    
    Returns:
        Dictionary of initialized indicators
    """
    if metrics is None:
        metrics = list(INDICATOR_REGISTRY.keys())
        
    indicators = {}
    for name in metrics:
        if name not in INDICATOR_REGISTRY:
            continue
            
        indicator = INDICATOR_REGISTRY[name]()
        if device:
            indicator.device = device
        await indicator.initialize()
        indicators[name] = indicator
        
    return indicators
from .no_reference import BRISQUEIndicator, NRQMIndicator
from .perceptual import LPIPSIndicator, SSIMIndicator
from ..core.config import Config

# Registry of available indicators
INDICATOR_REGISTRY: Dict[str, Type[BaseIndicator]] = {
    'brisque': BRISQUEIndicator,
    'nrqm': NRQMIndicator,
    'lpips': LPIPSIndicator,
    'ssim': SSIMIndicator
}

def get_available_indicators() -> Dict[str, BaseIndicator]:
    """
    Get dictionary of all available indicators.
    
    Returns:
        Dictionary mapping indicator names to initialized instances
    """
    indicators = {}
    for name, cls in INDICATOR_REGISTRY.items():
        indicators[name] = cls()
    return indicators

def get_indicator_metadata() -> List[Dict]:
    """
    Get metadata for all available indicators.
    
    Returns:
        List of dictionaries containing indicator metadata
    """
    metadata = []
    for name, cls in INDICATOR_REGISTRY.items():
        instance = cls()
        meta = instance.get_metadata()
        meta['id'] = name
        metadata.append(meta)
    return metadata

async def initialize_indicators(config: Config) -> Dict[str, BaseIndicator]:
    """
    Initialize all configured indicators.
    
    Args:
        config: Configuration object specifying which indicators to use
        
    Returns:
        Dictionary of initialized indicators
    """
    indicators = {}
    enabled = config.get('enabled_indicators', list(INDICATOR_REGISTRY.keys()))
    
    for name in enabled:
        if name not in INDICATOR_REGISTRY:
            continue
            
        indicator = INDICATOR_REGISTRY[name]()
        await indicator.initialize()
        indicators[name] = indicator
        
    return indicators