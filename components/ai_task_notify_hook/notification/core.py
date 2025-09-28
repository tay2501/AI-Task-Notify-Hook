"""Core notification functionality component.

This component handles the core logic for displaying Windows notifications.
Follows single responsibility principle and is designed for high reusability.
"""

from typing import Optional
import sys

try:
    from plyer import notification
except ImportError as exc:
    # Fallback handling for environments where plyer is unavailable
    notification = None
    import_error = exc


def show_notification(
    title: str,
    message: str,
    app_name: str = "Claude Code",
    timeout: int = 10
) -> None:
    """Display Windows notification using Plyer.

    Args:
        title: Notification title
        message: Notification message body
        app_name: Application name to display
        timeout: Notification timeout in seconds

    Raises:
        ImportError: If plyer library is not available
        AttributeError: If plyer notification method is not available
        Exception: For any other unexpected errors
    """
    if notification is None:
        raise ImportError(f"plyer library not properly imported: {import_error}")

    try:
        notification.notify(
            title=title,
            message=message,
            app_name=app_name,
            timeout=timeout
        )
    except AttributeError as exc:
        raise AttributeError(f"plyer notification method not available: {exc}")
    except Exception as exc:
        raise Exception(f"Failed to show notification: {exc}")