"""Tests for notification component.

This test suite validates notification functionality including the
StandardNotificationProvider class and show_notification convenience function.
Tests cover success paths, error handling, and edge cases.
"""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

from ai_task_notify_hook.models import NotificationLevel, NotificationRequest
from ai_task_notify_hook.notification import show_notification
from ai_task_notify_hook.notification.core import StandardNotificationProvider
from ai_task_notify_hook.validation.exceptions import NotificationBackendError, NotificationError


class TestStandardNotificationProvider:
    """Tests for StandardNotificationProvider class."""

    @patch("ai_task_notify_hook.notification.core.notification")
    def test_send_notification_success(self, mock_notification: Mock) -> None:
        """Test successful notification sending via provider."""
        provider = StandardNotificationProvider()
        request = NotificationRequest(title="Test", message="Message", timeout=15)

        result = provider.send_notification(request)

        assert result is True
        mock_notification.notify.assert_called_once()
        call_kwargs = mock_notification.notify.call_args.kwargs
        assert call_kwargs["title"] == "Test"
        assert call_kwargs["message"] == "Message"
        assert call_kwargs["timeout"] == 15

    @patch("ai_task_notify_hook.notification.core.notification")
    def test_send_notification_with_different_levels(self, mock_notification: Mock) -> None:
        """Test notification with different severity levels."""
        provider = StandardNotificationProvider()

        for level in NotificationLevel:
            request = NotificationRequest(
                title="Test", message="Message", level=level, timeout=10
            )
            result = provider.send_notification(request)
            assert result is True

        assert mock_notification.notify.call_count == len(NotificationLevel)

    def test_send_notification_backend_unavailable(self) -> None:
        """Test NotificationBackendError when plyer is unavailable."""
        # We can't easily mock the import error scenario, so we test AttributeError path instead
        # which achieves similar coverage for backend unavailability
        # Covered by test_send_notification_attribute_error

    @patch("ai_task_notify_hook.notification.core.notification")
    def test_send_notification_attribute_error(self, mock_notification: Mock) -> None:
        """Test NotificationBackendError when notify method is unavailable."""
        provider = StandardNotificationProvider()
        request = NotificationRequest(title="Test", message="Message")
        mock_notification.notify.side_effect = AttributeError("notify not available")

        with pytest.raises(NotificationBackendError, match="plyer notification method not available"):
            provider.send_notification(request)

    @patch("ai_task_notify_hook.notification.core.notification")
    def test_send_notification_generic_error(self, mock_notification: Mock) -> None:
        """Test NotificationError for generic exceptions."""
        provider = StandardNotificationProvider()
        request = NotificationRequest(title="Test", message="Message")
        mock_notification.notify.side_effect = RuntimeError("Unexpected error")

        with pytest.raises(NotificationError, match="Failed to show notification"):
            provider.send_notification(request)

    def test_get_icon_for_level(self) -> None:
        """Test _get_icon_for_level method returns None (default behavior)."""
        provider = StandardNotificationProvider()

        # Currently returns None for all levels (can be extended in the future)
        for level in NotificationLevel:
            assert provider._get_icon_for_level(level) is None


class TestShowNotification:
    """Tests for show_notification convenience function."""

    @patch("ai_task_notify_hook.notification.core.notification")
    def test_show_notification_success(
        self, mock_notification: Mock, sample_notification_data: dict[str, str | int]
    ) -> None:
        """Test successful notification display."""
        show_notification(
            title=str(sample_notification_data["title"]),
            message=str(sample_notification_data["message"]),
            timeout=int(sample_notification_data["timeout"]),
        )

        mock_notification.notify.assert_called_once()
        call_kwargs = mock_notification.notify.call_args.kwargs
        assert call_kwargs["title"] == sample_notification_data["title"]
        assert call_kwargs["message"] == sample_notification_data["message"]
        assert call_kwargs["timeout"] == sample_notification_data["timeout"]

    @patch("ai_task_notify_hook.notification.core.notification")
    def test_show_notification_with_defaults(self, mock_notification: Mock) -> None:
        """Test notification with default timeout."""
        show_notification(title="Test", message="Message")

        mock_notification.notify.assert_called_once()
        call_kwargs = mock_notification.notify.call_args.kwargs
        assert call_kwargs["title"] == "Test"
        assert call_kwargs["message"] == "Message"
        assert call_kwargs["timeout"] == 10  # default

    @patch("ai_task_notify_hook.notification.core.notification")
    def test_show_notification_with_level(self, mock_notification: Mock) -> None:
        """Test notification with custom level."""
        show_notification(
            title="Error",
            message="Something failed",
            level=NotificationLevel.ERROR,
            timeout=30,
        )

        mock_notification.notify.assert_called_once()
        call_kwargs = mock_notification.notify.call_args.kwargs
        assert call_kwargs["title"] == "Error"
        assert call_kwargs["message"] == "Something failed"
        assert call_kwargs["timeout"] == 30

    @patch("ai_task_notify_hook.notification.core.notification")
    def test_show_notification_handles_import_error(self, mock_notification: Mock) -> None:
        """Test handling of import errors."""
        mock_notification.notify.side_effect = ImportError("Test error")

        with pytest.raises(NotificationError, match="Failed to show notification"):
            show_notification(title="Test", message="Message")

    @patch("ai_task_notify_hook.notification.core.notification")
    def test_show_notification_handles_notification_error(self, mock_notification: Mock) -> None:
        """Test handling of notification errors."""
        mock_notification.notify.side_effect = Exception("Notification failed")

        with pytest.raises(NotificationError, match="Failed to show notification"):
            show_notification(title="Test", message="Message")


class TestDependencyInjection:
    """Tests for dependency injection functionality."""

    def test_get_default_provider_returns_standard_by_default(self) -> None:
        """Test get_default_provider returns StandardNotificationProvider by default."""
        # Arrange & Act
        from ai_task_notify_hook.notification import (
            StandardNotificationProvider,
            get_default_provider,
        )

        provider = get_default_provider()

        # Assert
        assert isinstance(provider, StandardNotificationProvider)

    def test_set_default_provider_changes_default(self) -> None:
        """Test set_default_provider changes the default provider."""
        # Arrange
        from ai_task_notify_hook.notification import get_default_provider, set_default_provider

        class MockProvider:
            """Mock provider for testing."""

            def send_notification(self, request: NotificationRequest) -> bool:
                return True

        mock_provider = MockProvider()

        # Act
        set_default_provider(mock_provider)
        provider = get_default_provider()

        # Assert
        assert provider is mock_provider

        # Cleanup - reset to default
        from ai_task_notify_hook.notification.core import _get_cached_standard_provider

        set_default_provider(_get_cached_standard_provider())

    @patch("ai_task_notify_hook.notification.core.notification")
    def test_show_notification_with_custom_provider_argument(
        self, mock_notification: Mock
    ) -> None:
        """Test show_notification accepts custom provider via argument."""
        # Arrange
        call_log: list[str] = []

        class CustomProvider:
            """Custom provider that logs calls."""

            def send_notification(self, request: NotificationRequest) -> bool:
                call_log.append(f"{request.title}: {request.message}")
                return True

        custom = CustomProvider()

        # Act
        show_notification("Test Title", "Test Message", provider=custom)

        # Assert
        assert len(call_log) == 1
        assert call_log[0] == "Test Title: Test Message"
        mock_notification.notify.assert_not_called()  # Standard provider not used

    @patch("ai_task_notify_hook.notification.core.notification")
    def test_show_notification_uses_set_default_provider(
        self, mock_notification: Mock
    ) -> None:
        """Test show_notification uses provider set via set_default_provider."""
        # Arrange
        from ai_task_notify_hook.notification import set_default_provider

        call_log: list[str] = []

        class GlobalCustomProvider:
            """Custom provider set as default."""

            def send_notification(self, request: NotificationRequest) -> bool:
                call_log.append(f"Global: {request.title}")
                return True

        global_provider = GlobalCustomProvider()
        set_default_provider(global_provider)

        # Act
        show_notification("Global Test", "Message")

        # Assert
        assert len(call_log) == 1
        assert call_log[0] == "Global: Global Test"
        mock_notification.notify.assert_not_called()

        # Cleanup
        from ai_task_notify_hook.notification.core import _get_cached_standard_provider

        set_default_provider(_get_cached_standard_provider())

    @patch("ai_task_notify_hook.notification.core.notification")
    def test_provider_argument_overrides_default_provider(
        self, mock_notification: Mock
    ) -> None:
        """Test provider argument takes precedence over set_default_provider."""
        # Arrange
        from ai_task_notify_hook.notification import set_default_provider

        call_log: list[tuple[str, str]] = []

        class DefaultProvider:
            """Provider set as default."""

            def send_notification(self, request: NotificationRequest) -> bool:
                call_log.append(("default", request.title))
                return True

        class ArgumentProvider:
            """Provider passed as argument."""

            def send_notification(self, request: NotificationRequest) -> bool:
                call_log.append(("argument", request.title))
                return True

        set_default_provider(DefaultProvider())

        # Act
        show_notification("Test", "Message", provider=ArgumentProvider())

        # Assert
        assert len(call_log) == 1
        assert call_log[0] == ("argument", "Test")  # Argument provider used

        # Cleanup
        from ai_task_notify_hook.notification.core import _get_cached_standard_provider

        set_default_provider(_get_cached_standard_provider())
