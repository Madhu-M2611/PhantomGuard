"""
Logging utilities for PhantomGuard Agent
"""

import sys
from pathlib import Path
from loguru import logger

def setup_logging(log_level: str = "INFO", log_file: str = None):
    """Setup logging configuration"""

    # Remove default handler
    logger.remove()

    # Console handler
    logger.add(
        sys.stdout,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )

    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        logger.add(
            log_file,
            level=log_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            rotation="10 MB",
            retention="30 days",
            encoding="utf-8"
        )

def get_logger(name: str):
    """Get a logger instance"""
    return logger.bind(name=name)