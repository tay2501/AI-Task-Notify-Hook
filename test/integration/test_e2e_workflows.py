"""End-to-End Integration Tests.

Comprehensive integration tests that validate the full application workflow
from CLI entry point through all components to notification display.
Tests cover success paths and all error scenarios for 100% coverage.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from ai_task_notify_hook.cli.core import main
from ai_task_notify_hook.validation import (
    ConfigurationError,
    NotificationBackendError,
    NotificationError,
)


class TestE2ESuccessWorkflow:
    """End-to-end tests for successful notification workflows."""

    @patch("ai_task_notify_hook.notification.core.notification")
    @patch("sys.argv", ["notify.py", "Test Title", "Test Message"])
    def test_complete_workflow_with_defaults(self, mock_notification: MagicMock) -> None:
        """Test complete workflow from CLI to notification with default config."""
        # Act - Run the full application
        main()

        # Assert - Notification was sent with correct parameters
        mock_notification.notify.assert_called_once()
        call_kwargs = mock_notification.notify.call_args.kwargs
        assert call_kwargs["title"] == "Test Title"
        assert call_kwargs["message"] == "Test Message"
        assert call_kwargs["timeout"] == 10  # Default from config

    @patch("ai_task_notify_hook.notification.core.notification")
    @patch("sys.argv", ["notify.py", "Custom", "Message", "--timeout", "30"])
    def test_complete_workflow_with_custom_timeout(
        self, mock_notification: MagicMock
    ) -> None:
        """Test complete workflow with custom timeout parameter."""
        # Act
        main()

        # Assert
        mock_notification.notify.assert_called_once()
        call_kwargs = mock_notification.notify.call_args.kwargs
        assert call_kwargs["title"] == "Custom"
        assert call_kwargs["message"] == "Message"
        assert call_kwargs["timeout"] == 30

    @patch("ai_task_notify_hook.notification.core.notification")
    @patch("sys.argv", ["notify.py", "Integration", "Test with multiple words"])
    def test_workflow_with_multiword_message(self, mock_notification: MagicMock) -> None:
        """Test workflow handles multi-word messages correctly."""
        # Act
        main()

        # Assert
        mock_notification.notify.assert_called_once()
        call_kwargs = mock_notification.notify.call_args.kwargs
        assert call_kwargs["message"] == "Test with multiple words"


class TestE2EErrorHandling:
    """End-to-end tests for error handling and exit codes."""

    @patch("sys.argv", ["notify.py", "Test", "Message"])
    @patch("ai_task_notify_hook.cli.core.show_notification")
    def test_keyboard_interrupt_handling(
        self, mock_show_notification: MagicMock
    ) -> None:
        """Test KeyboardInterrupt results in exit code 1."""
        # Arrange
        mock_show_notification.side_effect = KeyboardInterrupt()

        # Act & Assert
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    @patch("sys.argv", ["notify.py", "Test", "Message"])
    @patch("ai_task_notify_hook.cli.core.show_notification")
    def test_notification_backend_error_handling(
        self, mock_show_notification: MagicMock
    ) -> None:
        """Test NotificationBackendError results in exit code 2."""
        # Arrange - Simulate platform not supported
        mock_show_notification.side_effect = NotificationBackendError(
            "Platform 'FreeBSD' not supported"
        )

        # Act & Assert
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 2

    @patch("sys.argv", ["notify.py", "Test", "Message"])
    @patch("ai_task_notify_hook.cli.core.show_notification")
    def test_configuration_error_handling(
        self, mock_show_notification: MagicMock
    ) -> None:
        """Test ConfigurationError results in exit code 3."""
        # Arrange - Simulate config error during notification
        # Note: ConfigurationError can only be caught if raised inside try block
        mock_show_notification.side_effect = ConfigurationError(
            "Invalid configuration value"
        )

        # Act & Assert
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 3

    @patch("sys.argv", ["notify.py", "Test", "Message"])
    @patch("ai_task_notify_hook.notification.core.NotificationRequest")
    def test_validation_error_handling(self, mock_request_class: MagicMock) -> None:
        """Test ValidationError results in exit code 4."""
        # Arrange - Simulate Pydantic validation failure
        # Trigger a real validation error by creating invalid request
        from ai_task_notify_hook.models import NotificationRequest

        def raise_validation_error(*args: object, **kwargs: object) -> None:
            # Trigger real validation error with invalid timeout
            NotificationRequest(title="Test", message="Message", timeout=9999)

        mock_request_class.side_effect = raise_validation_error

        # Act & Assert
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 4

    @patch("sys.argv", ["notify.py", "Test", "Message"])
    @patch("ai_task_notify_hook.cli.core.show_notification")
    def test_generic_notification_error_handling(
        self, mock_show_notification: MagicMock
    ) -> None:
        """Test NotificationError results in exit code 1."""
        # Arrange - Simulate generic notification failure
        mock_show_notification.side_effect = NotificationError(
            "Failed to show notification: Connection timeout"
        )

        # Act & Assert
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1


class TestE2EComponentIntegration:
    """Integration tests validating component interactions."""

    @patch("ai_task_notify_hook.notification.core.notification")
    @patch("sys.argv", ["notify.py", "Component Test", "All systems integrated"])
    def test_config_logging_notification_integration(
        self, mock_notification: MagicMock
    ) -> None:
        """Test integration between config, logging, and notification components."""
        # Act - This tests the full component stack
        main()

        # Assert - All components worked together successfully
        mock_notification.notify.assert_called_once()

        # Verify notification received correct data from config
        call_kwargs = mock_notification.notify.call_args.kwargs
        assert call_kwargs["title"] == "Component Test"
        assert call_kwargs["message"] == "All systems integrated"
        # Default timeout comes from config component
        assert isinstance(call_kwargs["timeout"], int)
        assert call_kwargs["timeout"] > 0

    @patch("ai_task_notify_hook.notification.core.notification")
    @patch("sys.argv", ["notify.py", "Validation Test", "Testing validation layer"])
    def test_validation_component_integration(
        self, mock_notification: MagicMock
    ) -> None:
        """Test that validation component is properly integrated."""
        # Act
        main()

        # Assert - Validation passed and notification was sent
        mock_notification.notify.assert_called_once()

    @patch("ai_task_notify_hook.notification.core.notification")
    @patch("sys.argv", ["notify.py", "Provider Test", "Testing DI pattern"])
    def test_provider_dependency_injection_integration(
        self, mock_notification: MagicMock
    ) -> None:
        """Test that default provider is used correctly through DI pattern."""
        # Act - Use default provider through DI
        main()

        # Assert - Standard provider was used
        mock_notification.notify.assert_called_once()
        call_kwargs = mock_notification.notify.call_args.kwargs
        assert call_kwargs["title"] == "Provider Test"
        assert call_kwargs["message"] == "Testing DI pattern"


class TestE2EEdgeCases:
    """Integration tests for edge cases and boundary conditions."""

    @patch("sys.argv", ["notify.py", "", "Empty title test"])
    def test_empty_title_validation_error(self) -> None:
        """Test empty title triggers validation error (exit code 4)."""
        # Act & Assert - Empty title should fail validation
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 4

    @patch("sys.argv", ["notify.py", "Valid Title", ""])
    def test_empty_message_validation_error(self) -> None:
        """Test empty message triggers validation error (exit code 4)."""
        # Act & Assert - Empty message should fail validation
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 4

    @patch("ai_task_notify_hook.notification.core.notification")
    @patch("sys.argv", ["notify.py", "Title", "Message", "--timeout", "1"])
    def test_minimum_timeout_boundary(self, mock_notification: MagicMock) -> None:
        """Test minimum timeout value (boundary condition)."""
        # Act
        main()

        # Assert
        mock_notification.notify.assert_called_once()
        call_kwargs = mock_notification.notify.call_args.kwargs
        assert call_kwargs["timeout"] == 1

    @patch("ai_task_notify_hook.notification.core.notification")
    @patch(
        "sys.argv",
        ["notify.py", "Long Title " * 20, "Long Message " * 50, "--timeout", "300"],
    )
    def test_maximum_values_boundary(self, mock_notification: MagicMock) -> None:
        """Test maximum timeout and long strings (boundary conditions)."""
        # Act
        main()

        # Assert
        mock_notification.notify.assert_called_once()
        call_kwargs = mock_notification.notify.call_args.kwargs
        assert call_kwargs["timeout"] == 300
        assert len(call_kwargs["title"]) > 100
        assert len(call_kwargs["message"]) > 500
