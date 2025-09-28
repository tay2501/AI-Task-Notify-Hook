"""Logging component.

This component provides structured logging capabilities using structlog.
Designed for high reusability and loose coupling.
"""

from __future__ import annotations

import logging
import logging.config
import sys
from pathlib import Path
from typing import Any

try:
    import orjson  # type: ignore[import-untyped]
    import structlog
    import yaml
except ImportError as exc:
    print(f"Error: Required logging library not found: {exc}", file=sys.stderr)
    sys.exit(1)


def configure_logging(config_path: str | Path = "config/logging_config.yaml") -> None:
    """Configure logging system from external configuration file.

    Args:
        config_path: Path to YAML configuration file
    """
    # Set up minimal stderr fallback first
    fallback_handler = logging.StreamHandler(sys.stderr)
    fallback_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"
    )
    fallback_handler.setFormatter(fallback_formatter)

    # Configure basic structlog for fallback
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    config_path = Path(config_path)

    try:
        # Load configuration if available
        if config_path.exists():
            with config_path.open(encoding="utf-8") as file:
                config = yaml.safe_load(file) or {}

            # Ensure log directory exists
            app_config = config.get("app_logging", {})
            log_dir = app_config.get("log_directory", "logs")
            Path(log_dir).mkdir(parents=True, exist_ok=True)

            # Configure standard library logging
            logging_config = {
                key: value for key, value in config.items()
                if key not in ("structlog", "app_logging")
            }
            logging.config.dictConfig(logging_config)

    except Exception as exc:
        # Use fallback configuration
        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        root_logger.addHandler(fallback_handler)
        root_logger.setLevel(logging.INFO)


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """Get a configured structlog logger.

    Args:
        name: Logger name (defaults to calling module name)

    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)