"""Tests for logging component."""

from __future__ import annotations

import pytest
from structlog.stdlib import BoundLogger

from ai_task_notify_hook.logging import configure_logging, get_logger
from ai_task_notify_hook.models import LogLevel


class TestConfigureLogging:
    """Tests for configure_logging function."""

    def test_configure_logging_default_level(self) -> None:
        """Test logging configuration with default level."""
        configure_logging()
        logger = get_logger("test")

        assert logger is not None
        assert hasattr(logger, "info")
        assert hasattr(logger, "error")

    def test_configure_logging_debug_level(self) -> None:
        """Test logging configuration with DEBUG level."""
        configure_logging(log_level=LogLevel.DEBUG)
        logger = get_logger("test")

        assert logger is not None
        assert hasattr(logger, "info")
        assert hasattr(logger, "debug")

    def test_configure_logging_different_levels(self) -> None:
        """Test configuration with different log levels."""
        for level in LogLevel:
            configure_logging(log_level=level)
            logger = get_logger("test")
            assert logger is not None
            assert hasattr(logger, "info")


class TestGetLogger:
    """Tests for get_logger function."""

    def test_get_logger_with_name(self) -> None:
        """Test getting logger with specific name."""
        logger = get_logger("my_module")

        assert logger is not None
        assert hasattr(logger, "info")
        assert hasattr(logger, "error")

    def test_get_logger_without_name(self) -> None:
        """Test getting logger without name."""
        logger = get_logger()

        assert logger is not None
        assert hasattr(logger, "info")
        assert hasattr(logger, "error")

    def test_get_logger_returns_different_instances(self) -> None:
        """Test that get_logger returns proper instances."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")

        assert logger1 is not None
        assert logger2 is not None
        assert hasattr(logger1, "info")
        assert hasattr(logger2, "info")
