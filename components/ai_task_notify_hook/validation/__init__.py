"""Validation component public interface.

Provides custom exception classes.
All validation is handled by Pydantic models.
"""

from ai_task_notify_hook.validation.exceptions import (
    ConfigurationError,
    NotificationBackendError,
    NotificationError,
    ValidationError,
)

__all__ = [
    "ConfigurationError",
    "NotificationBackendError",
    "NotificationError",
    "ValidationError",
]
