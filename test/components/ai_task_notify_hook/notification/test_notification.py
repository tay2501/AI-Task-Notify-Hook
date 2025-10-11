"""Tests for notification component."""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

from ai_task_notify_hook.notification import show_notification


class TestShowNotification:
    """Tests for show_notification function."""

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
    def test_show_notification_with_defaults(
        self, mock_notification: Mock
    ) -> None:
        """Test notification with default timeout."""
        show_notification(title="Test", message="Message")

        mock_notification.notify.assert_called_once()
        call_kwargs = mock_notification.notify.call_args.kwargs
        assert call_kwargs["title"] == "Test"
        assert call_kwargs["message"] == "Message"
        assert call_kwargs["timeout"] == 10  # default

    @patch("ai_task_notify_hook.notification.core.notification")
    def test_show_notification_handles_import_error(
        self, mock_notification: Mock
    ) -> None:
        """Test handling of import errors."""
        from ai_task_notify_hook.validation.exceptions import NotificationError

        mock_notification.notify.side_effect = ImportError("Test error")

        with pytest.raises(NotificationError, match="Failed to show notification"):
            show_notification(title="Test", message="Message")

    @patch("ai_task_notify_hook.notification.core.notification")
    def test_show_notification_handles_notification_error(
        self, mock_notification: Mock
    ) -> None:
        """Test handling of notification errors."""
        from ai_task_notify_hook.validation.exceptions import NotificationError

        mock_notification.notify.side_effect = Exception("Notification failed")

        with pytest.raises(NotificationError, match="Failed to show notification"):
            show_notification(title="Test", message="Message")
