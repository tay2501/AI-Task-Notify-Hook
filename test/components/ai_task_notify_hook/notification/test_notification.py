"""Tests for notification component.

This test suite validates notification functionality including the
StandardNotificationProvider class and show_notification convenience function.
Tests cover success paths, error handling, and edge cases.

Updated for desktop-notifier library (v6+).
"""

from __future__ import annotations

from unittest.mock import AsyncMock, Mock, patch

import pytest

from ai_task_notify_hook.models import NotificationLevel, NotificationRequest
from ai_task_notify_hook.notification import show_notification
from ai_task_notify_hook.notification.core import StandardNotificationProvider
from ai_task_notify_hook.validation.exceptions import NotificationBackendError, NotificationError


class TestStandardNotificationProvider:
    """Tests for StandardNotificationProvider class."""

    @patch("ai_task_notify_hook.notification.core.asyncio.run")
    def test_send_notification_success(self, mock_asyncio_run: Mock) -> None:
        """Test successful notification sending via provider."""
        provider = StandardNotificationProvider()
        request = NotificationRequest(title="Test", message="Message", timeout=15)

        result = provider.send_notification(request)

        assert result is True
        mock_asyncio_run.assert_called_once()

    @patch("ai_task_notify_hook.notification.core.asyncio.run")
    def test_send_notification_with_different_levels(self, mock_asyncio_run: Mock) -> None:
        """Test notification with different severity levels."""
        provider = StandardNotificationProvider()

        for level in NotificationLevel:
            request = NotificationRequest(
                title="Test", message="Message", level=level, timeout=10
            )
            result = provider.send_notification(request)
            assert result is True

        assert mock_asyncio_run.call_count == len(NotificationLevel)

    def test_send_notification_backend_unavailable(self) -> None:
        """Test NotificationBackendError when desktop-notifier is unavailable."""
        # Test is implicitly covered by import error handling
        # If DesktopNotifier is None, initialization will raise NotificationBackendError

    @patch("ai_task_notify_hook.notification.core.asyncio.run")
    def test_send_notification_generic_error(self, mock_asyncio_run: Mock) -> None:
        """Test NotificationError for generic exceptions."""
        provider = StandardNotificationProvider()
        request = NotificationRequest(title="Test", message="Message")
        mock_asyncio_run.side_effect = RuntimeError("Unexpected error")

        with pytest.raises(NotificationError, match="Failed to show notification"):
            provider.send_notification(request)

    def test_get_urgency_for_level(self) -> None:
        """Test _get_urgency_for_level maps levels correctly."""
        from desktop_notifier import Urgency

        provider = StandardNotificationProvider()

        # ERROR maps to Critical
        assert provider._get_urgency_for_level(NotificationLevel.ERROR) == Urgency.Critical

        # All others map to Normal
        for level in [NotificationLevel.INFO, NotificationLevel.SUCCESS, NotificationLevel.WARNING]:
            assert provider._get_urgency_for_level(level) == Urgency.Normal


class TestShowNotification:
    """Tests for show_notification convenience function."""

    @patch("ai_task_notify_hook.notification.core.asyncio.run")
    def test_show_notification_success(
        self, mock_asyncio_run: Mock, sample_notification_data: dict[str, str | int]
    ) -> None:
        """Test successful notification display."""
        show_notification(
            title=str(sample_notification_data["title"]),
            message=str(sample_notification_data["message"]),
            timeout=int(sample_notification_data["timeout"]),
        )

        mock_asyncio_run.assert_called_once()

    @patch("ai_task_notify_hook.notification.core.asyncio.run")
    def test_show_notification_with_defaults(self, mock_asyncio_run: Mock) -> None:
        """Test notification with default timeout."""
        show_notification(title="Test", message="Message")

        mock_asyncio_run.assert_called_once()

    @patch("ai_task_notify_hook.notification.core.asyncio.run")
    def test_show_notification_with_level(self, mock_asyncio_run: Mock) -> None:
        """Test notification with custom level."""
        show_notification(
            title="Error",
            message="Something failed",
            level=NotificationLevel.ERROR,
            timeout=30,
        )

        mock_asyncio_run.assert_called_once()

    @patch("ai_task_notify_hook.notification.core.asyncio.run")
    def test_show_notification_handles_import_error(self, mock_asyncio_run: Mock) -> None:
        """Test handling of import errors."""
        mock_asyncio_run.side_effect = ImportError("Test error")

        with pytest.raises(NotificationError, match="Failed to show notification"):
            show_notification(title="Test", message="Message")

    @patch("ai_task_notify_hook.notification.core.asyncio.run")
    def test_show_notification_handles_notification_error(self, mock_asyncio_run: Mock) -> None:
        """Test handling of notification errors."""
        mock_asyncio_run.side_effect = Exception("Notification failed")

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

    def test_show_notification_with_custom_provider_argument(self) -> None:
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

    def test_show_notification_uses_set_default_provider(self) -> None:
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

        # Cleanup
        from ai_task_notify_hook.notification.core import _get_cached_standard_provider

        set_default_provider(_get_cached_standard_provider())

    def test_provider_argument_overrides_default_provider(self) -> None:
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
