#!/usr/bin/env python3
"""Main IQA-Server MCP implementation."""

import asyncio
import logging
from typing import Any, Sequence
from mcp.server import Server
from mcp.server.models import InitializationArgs
from mcp.types import Tool, TextContent

# Core server setup with proper MCP integration
# Tool definitions for all metrics
# Error handling and logging
# GPU detection and configuration