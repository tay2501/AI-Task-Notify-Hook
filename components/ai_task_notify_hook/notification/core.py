"""Core notification functionality component.

This component handles the core logic for displaying Windows notifications.
Follows single responsibility principle and is designed for high reusability.
"""

from ai_task_notify_hook.models import NotificationLevel, NotificationRequest
from ai_task_notify_hook.validation import NotificationBackendError, NotificationError

try:
    from plyer import notification
except ImportError as exc:
    # Fallback handling for environments where plyer is unavailable
    notification = None
    import_error = exc


class StandardNotificationProvider:
    """Standard implementation of NotificationProvider protocol."""

    def send_notification(self, request: NotificationRequest) -> bool:
        """Send a notification.

        Args:
            request: The notification request to send

        Returns:
            True if notification was sent successfully, False otherwise

        Raises:
            NotificationBackendError: If plyer is not available or platform
                not supported
            NotificationError: For other notification failures
        """
        if notification is None:
            raise NotificationBackendError(
                "plyer library not properly imported", cause=import_error
            )

        try:
            # Map notification level to app icon if needed
            app_icon = self._get_icon_for_level(request.level)

            notification.notify(
                title=request.title,
                message=request.message,
                timeout=request.timeout,
                app_icon=app_icon,
            )
            return True

        except AttributeError as exc:
            raise NotificationBackendError(
                "plyer notification method not available on this platform", cause=exc
            ) from exc
        except Exception as exc:
            raise NotificationError(
                f"Failed to show notification: {exc}", cause=exc
            ) from exc

    def _get_icon_for_level(self, level: NotificationLevel) -> str | None:
        """Get system icon path based on notification level.

        Args:
            level: Notification level

        Returns:
            Icon path or None for default
        """
        # Could be extended to return platform-specific icons
        return None


# Convenience function
def show_notification(
    title: str,
    message: str,
    level: NotificationLevel = NotificationLevel.INFO,
    timeout: int = 10,
) -> None:
    """Display notification with simplified interface.

    Args:
        title: Notification title
        message: Notification message body
        level: Notification severity level
        timeout: Notification timeout in seconds

    Raises:
        NotificationBackendError: If notification backend is unavailable
        NotificationError: If notification fails to send

    Examples:
        >>> show_notification("Build Complete", "All tests passed")
        >>> show_notification("Error", "Build failed", level=NotificationLevel.ERROR)
    """
    provider = StandardNotificationProvider()
    request = NotificationRequest(
        title=title, message=message, level=level, timeout=timeout
    )
    provider.send_notification(request)
