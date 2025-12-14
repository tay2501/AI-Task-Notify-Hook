"""Notification provider protocol definition.

This module defines the Protocol (PEP 544) for notification providers,
enabling structural subtyping and dependency injection. Follows the
Open/Closed Principle - open for extension, closed for modification.

Updated to async protocol for better performance and composition with
modern async notification libraries like desktop-notifier.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from ai_task_notify_hook.models import NotificationRequest


class NotificationProvider(Protocol):
    """Async protocol for notification providers.

    This protocol defines the async interface that all notification providers
    must implement. Using Protocol (PEP 544) enables structural subtyping,
    allowing any class with a compatible async `send_notification` method to
    be used as a provider without explicit inheritance.

    The async design enables better performance with modern notification
    libraries and allows for parallel notification sending via asyncio.gather().

    Examples:
        Standard implementation:
        >>> from ai_task_notify_hook.notification import StandardNotificationProvider
        >>> provider = StandardNotificationProvider()
        >>> isinstance(provider, NotificationProvider)  # doctest: +SKIP
        True

        Custom async implementation:
        >>> class EmailNotificationProvider:
        ...     async def send_notification(self, request: NotificationRequest) -> bool:
        ...         # Send email notification asynchronously
        ...         await send_email(request.title, request.message)
        ...         return True
        >>> provider = EmailNotificationProvider()  # doctest: +SKIP

    Note:
        Protocol is a static typing construct. Runtime isinstance() checks
        require `@runtime_checkable` decorator (not used here for performance).
    """

    async def send_notification(self, request: NotificationRequest) -> bool:
        """Send a notification asynchronously.

        Args:
            request: The notification request to send

        Returns:
            True if notification was sent successfully

        Raises:
            NotificationBackendError: If notification backend is unavailable
            NotificationError: If notification fails to send
        """
        ...
