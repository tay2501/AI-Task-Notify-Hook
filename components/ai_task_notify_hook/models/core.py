"""Shared data models and enums for AI Task Notify Hook.

This module contains core data models and enumerations used across
all components. Models are simple, frozen dataclasses with no dependencies
on other components, ensuring loose coupling.
"""

from dataclasses import dataclass
from enum import Enum


class NotificationLevel(Enum):
    """Notification severity levels."""

    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class LogLevel(Enum):
    """Logging levels."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass(frozen=True)
class NotificationRequest:
    """Represents a notification request.

    Attributes:
        title: Notification title text
        message: Notification message body
        level: Notification severity level
        timeout: Display timeout in seconds (1-300)
    """

    title: str
    message: str
    level: NotificationLevel = NotificationLevel.INFO
    timeout: int = 10

    def __post_init__(self) -> None:
        """Validate notification request data."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        if not self.message or not self.message.strip():
            raise ValueError("Message cannot be empty")
        if not 1 <= self.timeout <= 300:
            raise ValueError("Timeout must be between 1 and 300 seconds")
