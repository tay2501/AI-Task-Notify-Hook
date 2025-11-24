"""Notification component public interface.

Provides notification functionality with dependency injection support
via the NotificationProvider Protocol.
"""

from .core import (
    StandardNotificationProvider,
    get_default_provider,
    set_default_provider,
    show_notification,
)
from .protocol import NotificationProvider

__all__ = [
    # Protocol (for type hints and custom implementations)
    "NotificationProvider",
    # Standard implementation
    "StandardNotificationProvider",
    # Provider management (dependency injection)
    "get_default_provider",
    "set_default_provider",
    # Core functionality
    "show_notification",
]
