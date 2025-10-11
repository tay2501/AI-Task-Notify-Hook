"""Custom exception classes for AI Task Notify Hook.

This module defines a hierarchy of custom exceptions following Python best practices.
All exceptions inherit from a base exception for easy catching.
"""


class NotificationError(Exception):
    """Base exception for all notification-related errors.

    This is the base class for all custom exceptions in the application.
    Use this to catch any application-specific error.
    """

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message
            cause: Optional underlying exception that caused this error
        """
        super().__init__(message)
        self.message = message
        self.cause = cause

    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.cause:
            return f"{self.message} (caused by: {self.cause!r})"
        return self.message


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
