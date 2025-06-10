"""
Constants used throughout the IQA server.
"""

from enum import Enum
from typing import Dict, List, Set, Tuple
from pathlib import Path
import pyiqa

# Paths
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
CONFIG_TEMPLATES_DIR = DATA_DIR / "config_templates"
SAMPLE_IMAGES_DIR = DATA_DIR / "sample_images"
MODELS_DIR = ROOT_DIR / "models"

# Image processing
MAX_IMAGE_SIZE = 4096  # Maximum dimension of input images
DEFAULT_IMAGE_SIZE = 224  # Default size for neural network inputs
SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}

# Server settings
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 50051
DEFAULT_MAX_WORKERS = 10
DEFAULT_CACHE_SIZE = 1000
CACHE_TIMEOUT = 3600  # 1 hour in seconds
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DEFAULT_LOG_LEVEL = 'INFO'

# PyIQA metric groupings
FR_METRICS: List[str] = pyiqa.get_fr_metrics()
NR_METRICS: List[str] = pyiqa.get_nr_metrics()
ALL_METRICS: List[str] = pyiqa.get_all_metrics()

# Default metrics to use if none specified
DEFAULT_FR_METRICS: List[str] = ['psnr', 'ssim', 'lpips']
DEFAULT_NR_METRICS: List[str] = ['niqe', 'brisque']

# Batch processing
MAX_BATCH_SIZE = 100
DEFAULT_BATCH_SIZE = 16

# GPU settings
MIN_GPU_MEMORY = 2048  # Minimum GPU memory required in MB
CUDA_VISIBLE_DEVICES = '0'  # Default GPU device

class MetricRange(Enum):
    """Range of values for different metrics."""
    ZERO_TO_ONE = "0-1"
    ZERO_TO_HUNDRED = "0-100"
    MINUS_ONE_TO_ONE = "-1-1"
    DB = "db"  # For PSNR

METRIC_RANGES = {
    "brisque": MetricRange.ZERO_TO_HUNDRED,
    "nrqm": MetricRange.ZERO_TO_HUNDRED,
    "lpips": MetricRange.ZERO_TO_ONE,
    "ssim": MetricRange.ZERO_TO_ONE,
    "psnr": MetricRange.DB,
    "niqe": MetricRange.ZERO_TO_HUNDRED,
    "musiq": MetricRange.ZERO_TO_HUNDRED,    "fid": MetricRange.ZERO_TO_HUNDRED,
}

METRIC_INTERPRETATIONS = {
    "brisque": {
        "better": "lower",
        "ranges": {
            (0, 20): "Excellent quality",
            (20, 40): "Good quality",
            (40, 60): "Fair quality",
            (60, 80): "Poor quality",
            (80, 100): "Very poor quality"
        }
    },
    "niqe": {
        "better": "lower",
        "ranges": {
            (0, 20): "Excellent quality",
            (20, 40): "Good quality",
            (40, 60): "Fair quality",
            (60, 80): "Poor quality",
            (80, 100): "Very poor quality"
        }
    },
    "lpips": {
        "better": "lower",
        "ranges": {
            (0, 0.2): "Very similar images",
            (0.2, 0.4): "Similar images",
            (0.4, 0.6): "Moderate differences",
            (0.6, 0.8): "Significant differences",
            (0.8, 1.0): "Very different images"
        }
    },
    "ssim": {
        "better": "higher",
        "ranges": {
            (0.95, 1.0): "Excellent structural similarity",
            (0.88, 0.95): "Good structural similarity",
            (0.80, 0.88): "Fair structural similarity",
            (0.70, 0.80): "Poor structural similarity",
            (0, 0.70): "Very poor structural similarity"
        }
    },
    "psnr": {
        "better": "higher",
        "ranges": {
            (40, float('inf')): "Excellent quality",
            (30, 40): "Good quality",
            (20, 30): "Fair quality",
            (10, 20): "Poor quality",
            (0, 10): "Very poor quality"
        }
    }
}

# Paths
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
CONFIG_TEMPLATES_DIR = DATA_DIR / "config_templates"
SAMPLE_IMAGES_DIR = DATA_DIR / "sample_images"
MODELS_DIR = ROOT_DIR / "models"

# Image processing
SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
MAX_IMAGE_SIZE = 4096  # Maximum dimension of input images
DEFAULT_IMAGE_SIZE = 224  # Default size for neural network inputs

# Metrics
class MetricRange(Enum):
    """Range of values for different metrics."""
    ZERO_TO_ONE = "0-1"
    ZERO_TO_HUNDRED = "0-100"
    MINUS_ONE_TO_ONE = "-1-1"

METRIC_RANGES = {
    "brisque": MetricRange.ZERO_TO_HUNDRED,
    "nrqm": MetricRange.ZERO_TO_HUNDRED,
    "lpips": MetricRange.ZERO_TO_HUNDRED,
    "ssim": MetricRange.ZERO_TO_HUNDRED
}

METRIC_INTERPRETATIONS = {
    "brisque": {
        "better": "lower",
        "ranges": {
            (0, 20): "Excellent quality",
            (20, 40): "Good quality",
            (40, 60): "Fair quality",
            (60, 80): "Poor quality",
            (80, 100): "Very poor quality"
        }
    },
    "nrqm": {
        "better": "higher",
        "ranges": {
            (0, 20): "Very poor quality",
            (20, 40): "Poor quality",
            (40, 60): "Fair quality",
            (60, 80): "Good quality",
            (80, 100): "Excellent quality"
        }
    },
    "lpips": {
        "better": "lower",
        "ranges": {
            (0, 20): "Very similar",
            (20, 40): "Similar",
            (40, 60): "Moderately different",
            (60, 80): "Different",
            (80, 100): "Very different"
        }
    },
    "ssim": {
        "better": "higher",
        "ranges": {
            (0, 20): "Very low structural similarity",
            (20, 40): "Low structural similarity",
            (40, 60): "Moderate structural similarity",
            (60, 80): "High structural similarity",
            (80, 100): "Very high structural similarity"
        }
    }
}

# Server defaults
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 50051
DEFAULT_MAX_WORKERS = 10
DEFAULT_TIMEOUT = 30  # seconds

# Cache settings
DEFAULT_CACHE_SIZE = 1000
CACHE_TIMEOUT = 3600  # 1 hour

# Logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_LOG_LEVEL = "INFO"