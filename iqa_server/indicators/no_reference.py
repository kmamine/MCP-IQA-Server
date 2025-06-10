"""
No-reference image quality assessment indicators using PyIQA.
These metrics do not require a reference image for comparison.

This module provides implementations of various no-reference IQA metrics using PyIQA:
- BRISQUE: Blind/Referenceless Image Spatial Quality Evaluator
- NIQE: Natural Image Quality Evaluator
- PIQ: Perceptual Image Quality
- MUSIQ: Multi-scale Image Quality Transformer
- ILNIQE: Integrated Local NIQE
- DBCNN: Deep Bilinear CNN
"""

from typing import Any, Dict, Optional
import torch
import pyiqa
from .base import BaseIndicator

class BRISQUEIndicator(BaseIndicator):
    """Blind/Referenceless Image Spatial Quality Evaluator."""
    
    def __init__(self):
        super().__init__(metric_name='brisque')

class NIQEIndicator(BaseIndicator):
    """Natural Image Quality Evaluator."""
    
    def __init__(self):
        super().__init__(metric_name='niqe')

class PIQIndicator(BaseIndicator):
    """Perceptual Image Quality."""
    
    def __init__(self):
        super().__init__(metric_name='piq')

class MUSIQIndicator(BaseIndicator):
    """Multi-scale Image Quality Transformer."""
    
    def __init__(self):
        super().__init__(metric_name='musiq')
        
class ILNIQEIndicator(BaseIndicator):
    """Integrated Local NIQE."""
    
    def __init__(self):
        super().__init__(metric_name='ilniqe')

class DBCNNIndicator(BaseIndicator):
    """Deep Bilinear CNN for Image Quality Assessment."""
    
    def __init__(self):
        super().__init__(metric_name='dbcnn')