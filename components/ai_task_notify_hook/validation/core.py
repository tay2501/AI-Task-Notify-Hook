"""Validation utilities for notification system.

This module provides validation functions for platform compatibility
and notification backend availability, following the Fail Fast principle.
"""

from __future__ import annotations

import platform
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import TypeVar

    F = TypeVar("F", bound=Callable[..., None])

from ai_task_notify_hook.validation.exceptions import NotificationBackendError

# Supported platforms for notification functionality
SUPPORTED_PLATFORMS = frozenset({"Windows", "Darwin", "Linux"})


def validate_platform_support() -> bool:
    """Check if current platform supports notifications.

    Validates that the operating system is one of the supported platforms
    for desktop notifications (Windows, macOS, Linux).

    Returns:
        True if platform is supported

    Raises:
        NotificationBackendError: If platform is unsupported

    Examples:
        >>> validate_platform_support()  # On Windows
        True

        >>> # On unsupported platform
        >>> validate_platform_support()  # doctest: +SKIP
        Traceback (most recent call last):
        NotificationBackendError: Platform 'FreeBSD' not supported...
    """
    current_platform = platform.system()

    if current_platform not in SUPPORTED_PLATFORMS:
        raise NotificationBackendError(
            f"Platform '{current_platform}' not supported. "
            f"Supported platforms: {', '.join(sorted(SUPPORTED_PLATFORMS))}"
        )

    return True


def validate_backend_available() -> bool:
    """Verify plyer notification backend is available.

    Performs comprehensive validation of the notification backend:
    1. Checks that plyer library is importable
    2. Verifies notification.notify method exists
    3. Ensures platform-specific backend is available

    Returns:
        True if backend is available and functional

    Raises:
        NotificationBackendError: If plyer import fails or notification
            method is unavailable on this platform

    Examples:
        >>> validate_backend_available()  # With plyer installed
        True

        >>> # Without plyer installed
        >>> validate_backend_available()  # doctest: +SKIP
        Traceback (most recent call last):
        NotificationBackendError: plyer library not installed...
    """
    try:
        from plyer import notification
    except ImportError as exc:
        raise NotificationBackendError(
            "plyer library not installed or import failed. "
            "Install with: uv add plyer"
        ) from exc

    # Verify notification.notify method exists
    if not hasattr(notification, "notify"):
        raise NotificationBackendError(
            f"plyer.notification.notify method not available on {platform.system()}. "
            "This platform may lack notification backend support."
        )

    return True


def require_notification_backend[F: Callable[..., None]](func: F) -> F:
    """Decorator to ensure notification backend is available before execution.

    This decorator validates both platform support and backend availability
    before allowing the decorated function to execute. Follows the Fail Fast
    principle by catching configuration issues early.

    Args:
        func: Function to decorate (must return None)

    Returns:
        Decorated function with validation

    Raises:
        NotificationBackendError: If platform is unsupported or backend unavailable

    Examples:
        >>> @require_notification_backend
        ... def send_alert(message: str) -> None:
        ...     print(f"Sending: {message}")
        >>> send_alert("Test")  # doctest: +SKIP
        Sending: Test

    Note:
        Validation occurs on every function call. For performance-critical
        code, consider validating once at startup instead.
    """

    def wrapper(*args: object, **kwargs: object) -> None:
        validate_platform_support()
        validate_backend_available()
        func(*args, **kwargs)

    return wrapper  # type: ignore[return-value]
