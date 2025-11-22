"""Custom exception classes for AI Task Notify Hook.

This module defines a hierarchy of custom exceptions following Python best practices.
All exceptions inherit from a base exception for easy catching.

Use Python's standard exception chaining with 'raise ... from ...' syntax instead of
custom __init__ and __str__ methods. This provides better traceback and debugging.
"""


class NotificationError(Exception):
    """Base exception for all notification-related errors.

    This is the base class for all custom exceptions in the application.
    Use this to catch any application-specific error.

    Example:
        try:
            risky_operation()
        except SomeError as e:
            raise NotificationError("Operation failed") from e
    """


class ConfigurationError(NotificationError):
    """Raised when configuration is invalid, missing, or cannot be loaded.

    Examples:
        - Configuration file not found
        - Invalid JSON format
        - Missing required configuration fields
        - Configuration values out of valid range
    """


class ValidationError(NotificationError):
    """Raised when input validation fails.

    Examples:
        - Invalid notification title or message
        - Invalid timeout value
        - Invalid app name
    """


class NotificationBackendError(NotificationError):
    """Raised when the notification backend (plyer) fails.

    Examples:
        - Plyer library not available
        - Platform not supported
        - Notification service unavailable
        - Permission denied
    """
