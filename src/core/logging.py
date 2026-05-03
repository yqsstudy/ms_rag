"""Logging configuration"""

import logging
import sys
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class LoggingSetup:
    """Logging setup utility"""

    @staticmethod
    def setup(
        level: str = "INFO",
        log_format: str = "json",
        log_file: Optional[str] = None,
    ) -> logging.Logger:
        """Setup logging configuration"""
        # Create logger
        logger = logging.getLogger("ms_rag")
        logger.setLevel(getattr(logging, level.upper()))

        # Clear existing handlers
        logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))

        if log_format == "json":
            formatter = logging.Formatter(
                '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
                '"module": "%(name)s", "message": "%(message)s"}'
            )
        else:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (optional)
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
            )
            file_handler.setLevel(getattr(logging, level.upper()))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger


def get_logger(name: str = "ms_rag") -> logging.Logger:
    """Get logger instance"""
    return logging.getLogger(name)


def setup_logging(
    level: str = "INFO",
    log_format: str = "json",
    log_file: Optional[str] = None,
) -> logging.Logger:
    """Setup logging"""
    return LoggingSetup.setup(level, log_format, log_file)
