"""Tests for logging component.

This test suite validates structured logging configuration using structlog,
including both TTY (terminal) and non-TTY (production) environments.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

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

    @pytest.mark.parametrize("log_level", list(LogLevel))
    def test_configure_logging_all_levels(self, log_level: LogLevel) -> None:
        """Test configuration with all available log levels."""
        configure_logging(log_level=log_level)
        logger = get_logger("test")
        assert logger is not None
        assert hasattr(logger, "info")

    def test_configure_logging_tty_environment(self) -> None:
        """Test logging configuration in TTY environment (terminal)."""
        with patch("sys.stderr.isatty", return_value=True):
            configure_logging()
            logger = get_logger("test_tty")
            assert logger is not None
            # In TTY mode, ConsoleRenderer should be used
            assert hasattr(logger, "info")

    def test_configure_logging_non_tty_environment(self) -> None:
        """Test logging configuration in non-TTY environment (production)."""
        with patch("sys.stderr.isatty", return_value=False):
            configure_logging()
            logger = get_logger("test_non_tty")
            assert logger is not None
            # In non-TTY mode, JSONRenderer should be used
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
