"""Core notification functionality component.

This component handles the core logic for displaying desktop notifications.
Follows single responsibility principle and is designed for high reusability.

Supports dependency injection via NotificationProvider Protocol for extensibility
(e.g., Email, SMS, Slack notifications).

Updated to use desktop-notifier library (v6+) for modern, cross-platform notifications
with better platform API support and future extensibility.
"""

from __future__ import annotations

import asyncio
import sys
from functools import lru_cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_task_notify_hook.notification.protocol import NotificationProvider

from ai_task_notify_hook.models import NotificationLevel, NotificationRequest
from ai_task_notify_hook.validation import NotificationBackendError, NotificationError

try:
    from desktop_notifier import DesktopNotifier, Urgency
except ImportError as exc:
    # Fallback handling for environments where desktop-notifier is unavailable
    DesktopNotifier = None  # type: ignore[misc,assignment]
    Urgency = None  # type: ignore[misc,assignment]
    import_error = exc


class StandardNotificationProvider:
    """Standard implementation of NotificationProvider protocol using desktop-notifier.

    Uses desktop-notifier library which provides:
    - Modern platform APIs (no deprecated APIs like macOS NSUserNotificationCenter)
    - Better cross-platform support (Windows, macOS, Linux)
    - Interactive features (buttons, reply fields) for future extensibility
    - Pure Python implementation (no compiled extensions)
    """

    def __init__(self, app_name: str = "AI Task Notify Hook") -> None:
        """Initialize notification provider.

        Args:
            app_name: Application name shown in notifications

        Raises:
            NotificationBackendError: If desktop-notifier is not available
        """
        if DesktopNotifier is None:
            raise NotificationBackendError(
                "desktop-notifier library not properly imported"
            ) from import_error

        self._notifier = DesktopNotifier(app_name=app_name)

    def send_notification(self, request: NotificationRequest) -> bool:
        """Send a notification.

        Args:
            request: The notification request to send

        Returns:
            True if notification was sent successfully, False otherwise

        Raises:
            NotificationBackendError: If desktop-notifier is not available
            NotificationError: For other notification failures
        """
        try:
            # Map notification level to urgency
            urgency = self._get_urgency_for_level(request.level)

            # Prepare timeout (Linux only, in milliseconds)
            timeout_ms: int | None = None
            if sys.platform.startswith("linux"):
                timeout_ms = request.timeout * 1000  # Convert seconds to milliseconds

            # Send notification using asyncio
            # Note: timeout is only supported on Linux
            if timeout_ms is not None:
                asyncio.run(
                    self._notifier.send(
                        title=request.title,
                        message=request.message,
                        urgency=urgency,
                        timeout=timeout_ms,
                    )
                )
            else:
                asyncio.run(
                    self._notifier.send(
                        title=request.title,
                        message=request.message,
                        urgency=urgency,
                    )
                )
            return True

        except Exception as exc:
            raise NotificationError(f"Failed to show notification: {exc}") from exc

    @staticmethod
    def _get_urgency_for_level(level: NotificationLevel) -> Urgency:
        """Map notification level to desktop-notifier urgency.

        Args:
            level: Notification level from our model

        Returns:
            Urgency level for desktop-notifier
        """
        if Urgency is None:
            raise NotificationBackendError("desktop-notifier not available")

        # Map levels to urgency (ERROR is the highest severity in NotificationLevel)
        if level == NotificationLevel.ERROR:
            return Urgency.Critical
        return Urgency.Normal


# Global default provider (supports dependency injection)
_default_provider: NotificationProvider | None = None


@lru_cache(maxsize=1)
def _get_cached_standard_provider() -> StandardNotificationProvider:
    """Get cached standard notification provider instance.

    Uses functools.lru_cache for zero-overhead singleton pattern.
    This prevents unnecessary instance creation on every notification call,
    improving performance by caching the DesktopNotifier instance.

    Returns:
        Singleton StandardNotificationProvider instance
    """
    return StandardNotificationProvider()


def set_default_provider(provider: NotificationProvider) -> None:
    """Set custom notification provider for dependency injection.

    This function enables dependency injection by allowing custom providers
    (e.g., EmailNotificationProvider, SlackNotificationProvider) to replace
    the standard desktop notification provider.

    Args:
        provider: Custom provider implementation conforming to
            NotificationProvider Protocol

    Examples:
        >>> class EmailNotificationProvider:
        ...     def send_notification(self, request):
        ...         print(f"Email: {request.title}")
        ...         return True
        >>> set_default_provider(EmailNotificationProvider())  # doctest: +SKIP
        >>> show_notification("Test", "Message")  # Uses email provider  # doctest: +SKIP

    Note:
        This affects all subsequent calls to show_notification().
        Use the `provider` argument in show_notification() for one-time overrides.
    """
    global _default_provider
    _default_provider = provider


def get_default_provider() -> NotificationProvider:
    """Get the current default notification provider.

    Returns the custom provider set via set_default_provider(), or the
    standard provider if no custom provider is configured.

    Returns:
        Current default notification provider

    Examples:
        >>> provider = get_default_provider()  # doctest: +SKIP
        >>> isinstance(provider, StandardNotificationProvider)  # doctest: +SKIP
        True
    """
    if _default_provider is not None:
        return _default_provider
    return _get_cached_standard_provider()


# Convenience function with dependency injection support
def show_notification(
    title: str,
    message: str,
    level: NotificationLevel = NotificationLevel.INFO,
    timeout: int = 10,
    provider: NotificationProvider | None = None,
) -> None:
    """Display notification with simplified interface.

    Supports dependency injection via optional provider argument.
    If no provider is specified, uses the default provider
    (set via set_default_provider() or StandardNotificationProvider).

    Args:
        title: Notification title
        message: Notification message body
        level: Notification severity level
        timeout: Notification timeout in seconds (Linux only, ignored on Windows/macOS)
        provider: Optional custom provider (overrides default)

    Raises:
        NotificationBackendError: If notification backend is unavailable
        NotificationError: If notification fails to send

    Examples:
        Standard usage:
        >>> show_notification("Build Complete", "All tests passed")  # doctest: +SKIP

        With severity level:
        >>> show_notification("Error", "Build failed", level=NotificationLevel.ERROR)  # doctest: +SKIP

        With custom provider (dependency injection):
        >>> custom = EmailNotificationProvider()  # doctest: +SKIP
        >>> show_notification("Alert", "Server down", provider=custom)  # doctest: +SKIP

    Note:
        The timeout parameter is only supported on Linux. On Windows and macOS,
        notifications follow platform-specific timeout behavior.
    """
    notification_provider = provider or get_default_provider()
    request = NotificationRequest(
        title=title, message=message, level=level, timeout=timeout
    )
    notification_provider.send_notification(request)
