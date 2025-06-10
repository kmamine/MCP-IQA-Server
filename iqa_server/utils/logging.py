"""
Logging configuration and utilities.
"""

import logging
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from ..core.constants import LOG_FORMAT, DEFAULT_LOG_LEVEL

class JsonFormatter(logging.Formatter):
    """Format log records as JSON for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON string."""
        # Basic log data
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
            
        # Add extra fields from record
        if hasattr(record, 'extras'):
            log_data.update(record.extras)
            
        return json.dumps(log_data)

def setup_logging(
    level: str = DEFAULT_LOG_LEVEL,
    log_file: Optional[Path] = None,
    json_format: bool = False
) -> None:
    """
    Configure logging with console and optional file handlers.
    
    Args:
        level: Log level name
        log_file: Path to log file
        json_format: Whether to use JSON formatting
    """
    # Convert level name to logging constant
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Create formatters
    if json_format:
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(LOG_FORMAT)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Create file handler if log file specified
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

class ContextLogger:
    """Context manager for adding temporary context to logs."""
    
    def __init__(self, logger: logging.Logger, **context: Any):
        """
        Initialize with logger and context.
        
        Args:
            logger: Logger instance
            context: Key-value pairs to add to log context
        """
        self.logger = logger
        self.context = context
        self.previous_context: Optional[Dict] = None
        
    def __enter__(self) -> logging.Logger:
        """Add context to logger."""
        if hasattr(self.logger, 'extras'):
            self.previous_context = getattr(self.logger, 'extras')
        setattr(self.logger, 'extras', self.context)
        return self.logger
        
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Restore previous context."""
        if self.previous_context is not None:
            setattr(self.logger, 'extras', self.previous_context)
        else:
            delattr(self.logger, 'extras')

def get_logger(name: str) -> logging.Logger:
    """
    Get logger with given name.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)