"""Logging component.

This component provides structured logging capabilities using structlog.
Simple, programmatic configuration following best practices.
"""

from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING, cast

import structlog

if TYPE_CHECKING:
    from structlog.stdlib import BoundLogger
    from structlog.typing import Processor

from ai_task_notify_hook.models import LogLevel


def configure_logging(log_level: LogLevel = LogLevel.INFO) -> None:
    """Configure logging system with structured logging.

    Uses structlog with console rendering for terminal and JSON for production.
    Follows structlog best practices with minimal configuration.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Examples:
        >>> configure_logging()  # Use INFO level
        >>> configure_logging(log_level=LogLevel.DEBUG)
    """
    # Configure standard library logging first
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stderr,
        level=getattr(logging, log_level.value.upper()),
    )

    # Shared processors for all environments
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
    ]

    # Choose renderer based on environment
    processors: list[Processor]
    if sys.stderr.isatty():
        # Pretty printing for terminal (respects FORCE_COLOR/NO_COLOR)
        processors = [
            *shared_processors,
            structlog.dev.ConsoleRenderer(),
        ]
    else:
        # JSON for production/containers
        processors = [
            *shared_processors,
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]

    # Configure structlog
    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> BoundLogger:
    """Get a configured structlog logger.

    Args:
        name: Logger name (defaults to calling module name)

    Returns:
        Configured structlog logger

    Examples:
        >>> logger = get_logger(__name__)
        >>> logger.info("Application started")
    """
    return cast("BoundLogger", structlog.get_logger(name))
