"""
Interpretations and explanations for IQA metric scores.
"""

from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
import pyiqa

@dataclass
class ScoreRange:
    """Range of scores with interpretation."""
    min_val: float
    max_val: float
    description: str
    
    def contains(self, score: float) -> bool:
        """Check if a score falls within this range."""
        return self.min_val <= score <= self.max_val

@dataclass
class MetricInterpretation:
    """Interpretation guidelines for a metric."""
    name: str
    lower_better: bool
    description: str
    ranges: List[ScoreRange]
    
    def interpret(self, score: float) -> str:
        """Get interpretation for a specific score."""
        for range_ in self.ranges:
            if range_.contains(score):
                return range_.description
        return "Score out of expected ranges"

# Dictionary of metric interpretations
INTERPRETATIONS: Dict[str, MetricInterpretation] = {
    'psnr': MetricInterpretation(
        name='PSNR',
        lower_better=False,
        description='Peak Signal-to-Noise Ratio measures image fidelity',
        ranges=[
            ScoreRange(40, float('inf'), "Excellent quality (near perfect)"),
            ScoreRange(30, 40, "Good quality (minor imperfections)"),
            ScoreRange(20, 30, "Fair quality (noticeable degradation)"),
            ScoreRange(10, 20, "Poor quality (significant degradation)"),
            ScoreRange(0, 10, "Very poor quality (severe degradation)")
        ]
    ),
    'ssim': MetricInterpretation(
        name='SSIM',
        lower_better=False,
        description='Structural Similarity Index measures structural similarity',
        ranges=[
            ScoreRange(0.95, 1.0, "Excellent structural similarity"),
            ScoreRange(0.88, 0.95, "Good structural similarity"),
            ScoreRange(0.80, 0.88, "Fair structural similarity"),
            ScoreRange(0.70, 0.80, "Poor structural similarity"),
            ScoreRange(0, 0.70, "Very poor structural similarity")
        ]
    ),
    'lpips': MetricInterpretation(
        name='LPIPS',
        lower_better=True,
        description='Learned Perceptual Image Patch Similarity',
        ranges=[
            ScoreRange(0, 0.2, "Very similar images (minimal perceptual difference)"),
            ScoreRange(0.2, 0.4, "Similar images (minor perceptual differences)"),
            ScoreRange(0.4, 0.6, "Moderate perceptual differences"),
            ScoreRange(0.6, 0.8, "Significant perceptual differences"),
            ScoreRange(0.8, 1.0, "Very different images (major perceptual differences)")
        ]
    ),
    'brisque': MetricInterpretation(
        name='BRISQUE',
        lower_better=True,
        description='Blind/Referenceless Image Spatial Quality Evaluator',
        ranges=[
            ScoreRange(0, 20, "Excellent quality (highly natural images)"),
            ScoreRange(20, 40, "Good quality (natural images)"),
            ScoreRange(40, 60, "Fair quality (mildly distorted images)"),
            ScoreRange(60, 80, "Poor quality (distorted images)"),
            ScoreRange(80, 100, "Very poor quality (heavily distorted images)")
        ]
    ),
    'niqe': MetricInterpretation(
        name='NIQE',
        lower_better=True,
        description='Natural Image Quality Evaluator',
        ranges=[
            ScoreRange(0, 2, "Excellent quality (highly natural)"),
            ScoreRange(2, 4, "Good quality (natural)"),
            ScoreRange(4, 6, "Fair quality (mildly unnatural)"),
            ScoreRange(6, 8, "Poor quality (unnatural)"),
            ScoreRange(8, float('inf'), "Very poor quality (highly unnatural)")
        ]
    ),
    'musiq': MetricInterpretation(
        name='MUSIQ',
        lower_better=False,
        description='Multi-scale Image Quality Transformer',
        ranges=[
            ScoreRange(8, 10, "Excellent quality (best predicted MOS)"),
            ScoreRange(6, 8, "Good quality"),
            ScoreRange(4, 6, "Fair quality"),
            ScoreRange(2, 4, "Poor quality"),
            ScoreRange(0, 2, "Very poor quality (worst predicted MOS)")
        ]
    )
}

def get_interpretation(metric_name: str, score: Optional[float] = None) -> Dict[str, Any]:
    """
    Get interpretation information for a metric.
    
    Args:
        metric_name: Name of the metric
        score: Optional score to interpret
        
    Returns:
        Dictionary with interpretation information
    """
    if metric_name not in INTERPRETATIONS:
        raise ValueError(f"No interpretation available for metric: {metric_name}")
        
    interp = INTERPRETATIONS[metric_name]
    result = {
        "name": interp.name,
        "description": interp.description,
        "lower_better": interp.lower_better,
        "ranges": [(r.min_val, r.max_val, r.description) for r in interp.ranges]
    }
    
    if score is not None:
        result["score"] = score
        result["interpretation"] = interp.interpret(score)
        
    return result