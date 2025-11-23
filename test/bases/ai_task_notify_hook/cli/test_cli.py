"""Tests for CLI base component."""

from __future__ import annotations

import sys
from unittest.mock import Mock, patch

import pytest

from ai_task_notify_hook.cli.core import main
from ai_task_notify_hook.validation import NotificationError


class TestMain:
    """Tests for main CLI function."""

    @patch("ai_task_notify_hook.cli.core.show_notification")
    @patch("ai_task_notify_hook.cli.core.load_config")
    @patch("ai_task_notify_hook.cli.core.configure_logging")
    def test_main_success(
        self,
        mock_configure_logging: Mock,
        mock_load_config: Mock,
        mock_show_notification: Mock,
    ) -> None:
        """Test successful CLI execution."""
        mock_config = Mock()
        mock_config.version = "1.0.0"
        mock_config.notification.timeout = 10
        mock_load_config.return_value = mock_config

        test_args = ["notify", "Test Title", "Test Message"]
        with patch.object(sys, "argv", test_args):
            main()

        mock_configure_logging.assert_called_once()
        mock_load_config.assert_called_once()
        mock_show_notification.assert_called_once_with(
            title="Test Title", message="Test Message", timeout=10
        )

    @patch("ai_task_notify_hook.cli.core.show_notification")
    @patch("ai_task_notify_hook.cli.core.load_config")
    @patch("ai_task_notify_hook.cli.core.configure_logging")
    def test_main_with_custom_timeout(
        self,
        mock_configure_logging: Mock,
        mock_load_config: Mock,
        mock_show_notification: Mock,
    ) -> None:
        """Test CLI execution with custom timeout."""
        mock_config = Mock()
        mock_config.version = "1.0.0"
        mock_config.notification.timeout = 10
        mock_load_config.return_value = mock_config

        test_args = ["notify", "Title", "Message", "--timeout", "30"]
        with patch.object(sys, "argv", test_args):
            main()

        mock_show_notification.assert_called_once_with(
            title="Title", message="Message", timeout=30
        )

    @patch("ai_task_notify_hook.cli.core.show_notification")
    @patch("ai_task_notify_hook.cli.core.load_config")
    @patch("ai_task_notify_hook.cli.core.configure_logging")
    def test_main_keyboard_interrupt(
        self,
        mock_configure_logging: Mock,
        mock_load_config: Mock,
        mock_show_notification: Mock,
    ) -> None:
        """Test handling of keyboard interrupt."""
        mock_config = Mock()
        mock_config.version = "1.0.0"
        mock_config.notification.timeout = 10
        mock_load_config.return_value = mock_config
        mock_show_notification.side_effect = KeyboardInterrupt()

        test_args = ["notify", "Title", "Message"]
        with patch.object(sys, "argv", test_args):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    @patch("ai_task_notify_hook.cli.core.show_notification")
    @patch("ai_task_notify_hook.cli.core.load_config")
    @patch("ai_task_notify_hook.cli.core.configure_logging")
    def test_main_runtime_error(
        self,
        mock_configure_logging: Mock,
        mock_load_config: Mock,
        mock_show_notification: Mock,
    ) -> None:
        """Test handling of notification errors."""
        mock_config = Mock()
        mock_config.version = "1.0.0"
        mock_config.notification.timeout = 10
        mock_load_config.return_value = mock_config
        mock_show_notification.side_effect = NotificationError("Test error")

        test_args = ["notify", "Title", "Message"]
        with patch.object(sys, "argv", test_args):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
