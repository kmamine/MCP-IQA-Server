"""
Model definitions for Image Quality Assessment methods.

This module contains detailed descriptions and technical information about
various IQA models supported by the server.
"""

from typing import Dict, Any

# Full Reference (FR) Methods
FR_METHODS = {
    "topiq_fr": {
        "type": "FR",
        "names": ["topiq_fr", "topiq_fr-pipal"],
        "description": "TOPIQ Full Reference method - Proposed in the TOPIQ paper",
        "category": "General FR",
        "how_it_works": "TOPIQ uses a vision transformer architecture with multi-scale feature extraction...",
        "technical_details": {
            "architecture": "Vision Transformer based",
            "features": "Multi-scale semantic features from pre-trained models",
            "comparison_method": "Cosine similarity in feature space",
            "training_required": False,
            "key_innovation": "Training-free approach using foundation model features"
        },
        "use_cases": ["General image quality assessment", "Perceptual similarity measurement", "Content-aware quality evaluation"]
    },
    # ... (additional FR methods will be included)
}

# No Reference (NR) Methods
NR_METHODS = {
    "qalign": {
        "type": "NR",
        "names": ["qalign"],
        "description": "Q-Align - Large vision-language models with quality and aesthetic options",
        "category": "General NR",
        "how_it_works": "Q-Align leverages large vision-language models (LVLMs) for image quality assessment...",
        "technical_details": {
            "architecture": "Large Vision-Language Model (LVLM)",
            "training_approach": "Instruction tuning with quality annotations",
            "assessment_types": ["Technical quality", "Aesthetic quality"],
            "vision_encoder": "Pre-trained vision transformer",
            "language_model": "Large language model for quality reasoning",
            "output_format": "Natural language descriptions and scores",
            "key_innovation": "Multi-modal quality assessment with language understanding"
        },
        "use_cases": ["Comprehensive quality assessment", "Aesthetic evaluation", "Multi-modal analysis", "Explainable quality scores"]
    },
    # ... (additional NR methods will be included)
}
