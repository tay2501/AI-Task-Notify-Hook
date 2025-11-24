"""Validation component public interface.

Provides custom exception classes and validation utilities.
Combines Pydantic model validation with platform/backend checks.
"""

from ai_task_notify_hook.validation.core import (
    require_notification_backend,
    validate_backend_available,
    validate_platform_support,
)
from ai_task_notify_hook.validation.exceptions import (
    ConfigurationError,
    NotificationBackendError,
    NotificationError,
    ValidationError,
)

__all__ = [
    # Exceptions
    "ConfigurationError",
    "NotificationBackendError",
    "NotificationError",
    "ValidationError",
    # Validation functions
    "require_notification_backend",
    "validate_backend_available",
    "validate_platform_support",
]
