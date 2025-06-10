"""
Mean Opinion Score (MOS) predictor based on image quality metrics.
"""

import torch
import torch.nn as nn
from pathlib import Path
from typing import Dict, List, Optional

class MOSPredictor(nn.Module):
    """Neural network for predicting Mean Opinion Scores."""
    
    def __init__(self, input_size: int = 5):
        """
        Initialize MOS predictor.
        
        Args:
            input_size: Number of input metrics
        """
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass."""
        return self.model(x) * 100  # Scale to 0-100

class MOSEstimator:
    """High-level interface for MOS prediction."""
    
    def __init__(self, model_path: Optional[Path] = None):
        """
        Initialize MOS estimator.
        
        Args:
            model_path: Path to pre-trained model weights
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = MOSPredictor().to(self.device)
        if model_path and model_path.exists():
            self.model.load_state_dict(torch.load(model_path))
        self.model.eval()
        
    def predict(self, metrics: Dict[str, float]) -> float:
        """
        Predict MOS from quality metrics.
        
        Args:
            metrics: Dictionary of metric scores
            
        Returns:
            Predicted MOS score (0-100)
        """
        # Extract features from standard metrics
        features = []
        for metric in ['psnr', 'ssim', 'lpips', 'brisque', 'niqe']:
            if metric in metrics:
                features.append(metrics[metric])
            else:
                features.append(0.0)
                
        x = torch.tensor(features, dtype=torch.float32).to(self.device)
        
        with torch.no_grad():
            score = self.model(x.unsqueeze(0)).item()
            
        return score
        
    def batch_predict(self, batch_metrics: List[Dict[str, float]]) -> List[float]:
        """Predict MOS scores for multiple images."""
        features = []
        for metrics in batch_metrics:
            image_features = []
            for metric in ['psnr', 'ssim', 'lpips', 'brisque', 'niqe']:
                if metric in metrics:
                    image_features.append(metrics[metric])
                else:
                    image_features.append(0.0)
            features.append(image_features)
            
        x = torch.tensor(features, dtype=torch.float32).to(self.device)
        
        with torch.no_grad():
            scores = self.model(x).cpu().numpy().flatten().tolist()
            
        return scores