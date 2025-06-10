"""
Training utilities for MOS prediction models.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
from .predictor import MOSPredictor

class MOSDataset(Dataset):
    """Dataset for MOS prediction training."""
    
    def __init__(self, metrics: List[Dict[str, float]], scores: List[float]):
        """
        Initialize dataset.
        
        Args:
            metrics: List of metric dictionaries
            scores: List of MOS scores
        """
        self.features = []
        for metric_dict in metrics:
            features = []
            for metric in ['psnr', 'ssim', 'lpips', 'brisque', 'niqe']:
                features.append(metric_dict.get(metric, 0.0))
            self.features.append(features)
            
        self.features = torch.tensor(self.features, dtype=torch.float32)
        self.scores = torch.tensor(scores, dtype=torch.float32).view(-1, 1)
        
    def __len__(self) -> int:
        return len(self.scores)
        
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.features[idx], self.scores[idx]

def train_mos_model(
    train_metrics: List[Dict[str, float]],
    train_scores: List[float],
    val_metrics: Optional[List[Dict[str, float]]] = None,
    val_scores: Optional[List[float]] = None,
    batch_size: int = 32,
    epochs: int = 100,
    lr: float = 0.001,
    save_path: Optional[Path] = None
) -> MOSPredictor:
    """
    Train MOS prediction model.
    
    Args:
        train_metrics: Training set metrics
        train_scores: Training set MOS scores
        val_metrics: Validation set metrics
        val_scores: Validation set MOS scores
        batch_size: Training batch size
        epochs: Number of training epochs
        lr: Learning rate
        save_path: Path to save trained model
        
    Returns:
        Trained MOSPredictor model
    """
    # Create datasets
    train_dataset = MOSDataset(train_metrics, train_scores)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    if val_metrics and val_scores:
        val_dataset = MOSDataset(val_metrics, val_scores)
        val_loader = DataLoader(val_dataset, batch_size=batch_size)
    else:
        val_loader = None
        
    # Initialize model and optimizer
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = MOSPredictor().to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()
    
    # Training loop
    best_val_loss = float('inf')
    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        for features, targets in train_loader:
            features, targets = features.to(device), targets.to(device)
            
            optimizer.zero_grad()
            outputs = model(features)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            
        train_loss /= len(train_loader)
        
        # Validation
        if val_loader:
            model.eval()
            val_loss = 0.0
            with torch.no_grad():
                for features, targets in val_loader:
                    features, targets = features.to(device), targets.to(device)
                    outputs = model(features)
                    val_loss += criterion(outputs, targets).item()
                    
            val_loss /= len(val_loader)
            
            # Save best model
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                if save_path:
                    torch.save(model.state_dict(), save_path)
                    
            print(f'Epoch {epoch+1}: Train Loss = {train_loss:.4f}, Val Loss = {val_loss:.4f}')
        else:
            print(f'Epoch {epoch+1}: Train Loss = {train_loss:.4f}')
            if save_path:
                torch.save(model.state_dict(), save_path)
                
    return model