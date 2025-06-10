"""
Configuration management for the IQA server.
"""

import os
import json
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

class ServerConfig(BaseModel):
    """Server configuration settings."""
    host: str = Field(default="localhost", description="Server host")
    port: int = Field(default=50051, description="Server port")
    max_workers: int = Field(default=10, description="Maximum number of worker threads")
    log_level: str = Field(default="INFO", description="Logging level")

class MetricsConfig(BaseModel):
    """Configuration for quality metrics."""
    enabled_indicators: List[str] = Field(
        default=["brisque", "nrqm", "lpips", "ssim"],
        description="List of enabled quality indicators"
    )
    cache_size: int = Field(
        default=1000,
        description="Maximum number of results to cache"
    )
    lpips_net: str = Field(
        default="alex",
        description="Network backbone for LPIPS ('alex' or 'vgg')"
    )

class Config:
    """Main configuration class."""
    
    def __init__(
        self,
        config_path: Optional[str] = None,
        env_prefix: str = "IQA_"
    ):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to JSON config file
            env_prefix: Prefix for environment variables
        """
        self.server = ServerConfig()
        self.metrics = MetricsConfig()
        self.env_prefix = env_prefix
        
        # Load config in order of precedence
        if config_path and os.path.exists(config_path):
            self.load_from_file(config_path)
        self.load_from_env()
        
    def load_from_file(self, config_path: str) -> None:
        """Load configuration from JSON file."""
        with open(config_path) as f:
            config = json.load(f)
            
        if "server" in config:
            self.server = ServerConfig(**config["server"])
        if "metrics" in config:
            self.metrics = MetricsConfig(**config["metrics"])
            
    def load_from_env(self) -> None:
        """Load configuration from environment variables."""
        for var, value in os.environ.items():
            if not var.startswith(self.env_prefix):
                continue
                
            # Remove prefix and convert to lowercase
            key = var[len(self.env_prefix):].lower()
            
            # Handle nested configs
            if key.startswith("server_"):
                setattr(self.server, key[7:], value)
            elif key.startswith("metrics_"):
                setattr(self.metrics, key[8:], value)
                
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        parts = key.split('.')
        
        # Handle nested configs
        if parts[0] == "server":
            return getattr(self.server, parts[1], default)
        elif parts[0] == "metrics":
            return getattr(self.metrics, parts[1], default)
            
        return default
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dictionary representation of config
        """
        return {
            "server": self.server.dict(),
            "metrics": self.metrics.dict()
        }