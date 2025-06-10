#!/usr/bin/env python3
"""
Main entry point for the IQA MCP server using PyIQA for image quality assessment.
"""

import asyncio
import logging
import click
from pathlib import Path
from typing import Optional

from .core.config import Config
from .core.constants import DEFAULT_HOST, DEFAULT_PORT
from .server.mcp_server import IQAServer
from .utils.logging import setup_logging, get_logger

logger = get_logger(__name__)

async def run_server(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    config_path: Optional[Path] = None
) -> None:
    """
    Run the IQA MCP server.
    
    Args:
        host: Server host
        port: Server port
        config_path: Path to config file
    """
    # Load configuration
    config = Config(config_path=config_path) if config_path else Config()
    
    # Initialize server
    server = IQAServer(config=config)
    
    try:
        # Start server
        await server.startup()
        await server.serve(host=host, port=port)
        
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise
        
    finally:
        # Cleanup
        await server.shutdown()

@click.command()
@click.option(
    "--host",
    default=DEFAULT_HOST,
    help="Server host"
)
@click.option(
    "--port",
    default=DEFAULT_PORT,
    help="Server port"
)
@click.option(
    "--config",
    type=click.Path(exists=True, path_type=Path),
    help="Path to config file"
)
@click.option(
    "--log-level",
    default="INFO",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    help="Logging level"
)
@click.option(
    "--log-file",
    type=click.Path(dir_okay=False, path_type=Path),
    help="Log file path"
)
@click.option(
    "--json-logs",
    is_flag=True,
    help="Enable JSON formatted logging"
)
def main(
    host: str,
    port: int,
    config: Optional[Path],
    log_level: str,
    log_file: Optional[Path],
    json_logs: bool
) -> None:
    """Run the IQA MCP server with PyIQA metrics."""
    # Setup logging
    setup_logging(
        level=log_level,
        log_file=log_file,
        json_format=json_logs
    )
    
    logger.info(f"Starting IQA server with PyIQA on {host}:{port}")
    
    try:
        asyncio.run(run_server(
            host=host,
            port=port,
            config_path=config
        ))
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
from mcp.server import Server
from mcp.server.models import InitializationArgs
from mcp.types import Tool, TextContent

# Core server setup with proper MCP integration
# Tool definitions for all metrics
# Error handling and logging
# GPU detection and configuration