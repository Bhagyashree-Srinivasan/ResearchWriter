"""Logging utilities for the MCP server."""

import logging
from ..config.settings import settings

def configure_logging():
    """
    Configure logging for the MCP server and external libraries.
    
    This fucntion sets up logging levels for:
    - Root logger (main application)
    - External libraries (opik, hhtpx, etc.)
    """
    #Configure root logger
    logging.getLogger().setLevel(settings.log_level)
    
    #configure logging for external libraries to respect our dependency log level
    logging.getLogger("opik").setLevel(settings.log_level_dependencies)
    logging.getLogger("hhtpx").setLevel(settings.log_level_dependencies)
    logging.getLogger("openai").setLevel(settings.log_level_dependencies)
    logging.getLogger("fastmcp").setLevel(settings.log_level_dependencies)
    logging.getLogger("google").setLevel(settings.log_level_dependencies)