"""Logging component.

This component provides structured logging capabilities using structlog.
Simple, programmatic configuration following best practices.

Updated with structlog v25+ best practices:
- Conditional rendering (terminal vs production)
- Async logger support for future extensibility
- Enhanced exception and stack trace handling
- Extra context data support
"""

from __future__ import annotations

import logging
import os
import sys
from typing import TYPE_CHECKING, cast

import structlog

if TYPE_CHECKING:
    from structlog.stdlib import BoundLogger
    from structlog.typing import Processor

from ai_task_notify_hook.models import LogLevel


def configure_logging(
    log_level: LogLevel = LogLevel.INFO, is_production: bool | None = None
) -> None:
    """Configure logging system with structured logging.

    Uses structlog with console rendering for terminal and JSON for production.
    Follows structlog v25+ best practices with conditional rendering and
    async logger support.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        is_production: Force production mode (JSON output). If None, auto-detects
            based on sys.stderr.isatty() and PRODUCTION environment variable.

    Examples:
        >>> configure_logging()  # Auto-detect environment
        >>> configure_logging(log_level=LogLevel.DEBUG)  # Debug mode
        >>> configure_logging(is_production=True)  # Force JSON output
    """
    # Configure standard library logging first (12 Factor App compliance)
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,  # Standard output for 12 Factor App
        level=getattr(logging, log_level.value.upper()),
    )

    # Auto-detect production mode if not specified
    if is_production is None:
        is_production = not sys.stderr.isatty() or os.getenv("PRODUCTION") == "true"

    # Shared processors for all environments
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,  # Merge context variables
        structlog.stdlib.add_log_level,  # Add log level
        structlog.stdlib.add_logger_name,  # Add logger name
        structlog.stdlib.ExtraAdder(),  # Add extra context data
        structlog.processors.TimeStamper(fmt="iso", utc=True),  # ISO timestamps
        structlog.processors.StackInfoRenderer(),  # Stack trace support
    ]

    # Choose renderer based on environment
    processors: list[Processor]
    if is_production:
        # JSON for production/containers (structured output)
        processors = [
            *shared_processors,
            structlog.processors.dict_tracebacks,  # Structured exception tracebacks
            structlog.processors.format_exc_info,  # Format exception info
            structlog.processors.JSONRenderer(),  # JSON output
        ]
    else:
        # Pretty printing for terminal (respects FORCE_COLOR/NO_COLOR)
        processors = [
            *shared_processors,
            structlog.processors.format_exc_info,  # Format exception info
            structlog.dev.ConsoleRenderer(colors=True),  # Colored console output
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
        >>> logger.error("An error occurred", exc_info=True)
    """
    return cast("BoundLogger", structlog.get_logger(name))
