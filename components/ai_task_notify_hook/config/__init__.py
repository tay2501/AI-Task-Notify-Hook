"""Configuration management component.

This component handles configuration loading, validation, and management.
Follows single responsibility principle with high cohesion.
"""

from ai_task_notify_hook.config.loader import load_config, validate_config_file
from ai_task_notify_hook.config.models import ApplicationConfig, NotificationConfig
from ai_task_notify_hook.validation.exceptions import ConfigurationError

__all__ = [
    "ApplicationConfig",
    "ConfigurationError",
    "NotificationConfig",
    "load_config",
    "validate_config_file",
]
