#!/usr/bin/env python3
"""
Logging configuration module for notify application.
Provides structlog setup with external YAML configuration and log rotation.
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


def load_logging_config(
    config_path: str | Path = "config/logging_config.yaml",
) -> dict[str, Any]:
    """Load logging configuration from YAML file.

    Args:
        config_path: Path to YAML configuration file

    Returns:
        Configuration dictionary

    Raises:
        FileNotFoundError: If configuration file doesn't exist
        yaml.YAMLError: If YAML parsing fails
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Logging configuration file not found: {config_path}")

    try:
        with config_path.open(encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return config or {}
    except yaml.YAMLError as exc:
        raise yaml.YAMLError(f"Failed to parse logging configuration: {exc}") from exc


def ensure_log_directory(log_dir: str | Path = "logs") -> None:
    """Ensure log directory exists.

    Args:
        log_dir: Directory path for log files
    """
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)


def setup_structlog(config: dict[str, Any]) -> None:
    """Configure structlog based on configuration dictionary.

    Args:
        config: Configuration dictionary containing structlog settings
    """
    structlog_config = config.get("structlog", {})

    # Build processors list from configuration
    processors = []
    for processor_config in structlog_config.get("processors", []):
        if isinstance(processor_config, str):
            # Simple processor name
            processor_name = processor_config
            processor = _get_processor_by_name(processor_name)
            if processor:
                processors.append(processor)
        elif isinstance(processor_config, dict):
            # Processor with parameters
            for processor_name, params in processor_config.items():
                processor = _get_processor_by_name(processor_name, params or {})
                if processor:
                    processors.append(processor)

    # Configure structlog
    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=structlog_config.get(
            "cache_logger_on_first_use", True
        ),
    )


def _get_processor_by_name(name: str, params: dict[str, Any] | None = None) -> Any:
    """Get processor instance by name.

    Args:
        name: Processor name (e.g., 'structlog.processors.TimeStamper')
        params: Parameters to pass to processor constructor

    Returns:
        Processor instance or None if not found
    """
    if params is None:
        params = {}

    try:
        # Split module and class name
        module_parts = name.split(".")
        if len(module_parts) < 2:
            return None

        # Get processor class
        obj = structlog
        for part in module_parts[1:]:  # Skip 'structlog'
            obj = getattr(obj, part, None)
            if obj is None:
                return None

        # Create instance
        if callable(obj):
            return obj(**params)
        return obj
    except (AttributeError, TypeError):
        return None


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

    # Set up stderr formatter for fallback
    stderr_formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(colors=False),
        ],
    )
    fallback_handler.setFormatter(stderr_formatter)

    try:
        # Load configuration
        config = load_logging_config(config_path)

        # Ensure log directory exists
        app_config = config.get("app_logging", {})
        log_dir = app_config.get("log_directory", "logs")
        ensure_log_directory(log_dir)

        # Configure standard library logging
        logging_config = {
            key: value
            for key, value in config.items()
            if key not in ("structlog", "app_logging")
        }
        logging.config.dictConfig(logging_config)

        # Configure structlog with production settings
        timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)
        shared_processors = [
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            timestamper,
        ]

        structlog.configure(
            processors=shared_processors
            + [
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        # Update formatters to use ProcessorFormatter
        for handler in logging.getLogger().handlers:
            if hasattr(handler, "formatter"):
                handler_name = getattr(handler, "name", "")
                if "file" in handler_name.lower() or hasattr(handler, "baseFilename"):
                    # File handlers get JSON formatter
                    def json_serializer(obj: dict, **kwargs: Any) -> str:
                        return orjson.dumps(obj).decode("utf-8")

                    formatter = structlog.stdlib.ProcessorFormatter(
                        foreign_pre_chain=shared_processors,
                        processors=[
                            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                            structlog.processors.JSONRenderer(
                                serializer=json_serializer
                            ),
                        ],
                    )
                else:
                    # Console handlers get colored output
                    formatter = structlog.stdlib.ProcessorFormatter(
                        foreign_pre_chain=shared_processors,
                        processors=[
                            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                            structlog.dev.ConsoleRenderer(colors=True),
                        ],
                    )
                handler.setFormatter(formatter)

    except Exception as exc:
        # Use fallback configuration
        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        root_logger.addHandler(fallback_handler)
        root_logger.setLevel(logging.INFO)

        # Log the configuration error using structlog
        fallback_logger = structlog.get_logger("log_config.fallback")
        fallback_logger.error(
            "Failed to load external logging configuration, using stderr fallback",
            error=str(exc),
            config_path=str(config_path),
            fallback_active=True,
        )


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """Get a configured structlog logger.

    Args:
        name: Logger name (defaults to calling module name)

    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


if __name__ == "__main__":
    # Test configuration
    configure_logging()
    logger = get_logger("test")
    logger.info("Logging configuration test", status="success")
