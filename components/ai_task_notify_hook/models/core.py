"""Shared data models and enums for AI Task Notify Hook.

This module contains core data models and enumerations used across
all components. Models use Pydantic for validation and StrEnum for
better string handling, ensuring loose coupling.
"""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class NotificationLevel(StrEnum):
    """Notification severity levels.

    Using StrEnum (Python 3.11+) provides automatic string conversion
    and better type safety compared to regular Enum.
    """

    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class LogLevel(StrEnum):
    """Logging levels.

    Using StrEnum (Python 3.11+) provides automatic string conversion
    and better type safety compared to regular Enum.
    """

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class NotificationRequest(BaseModel):
    """Represents a notification request with Pydantic validation.

    Using Pydantic provides automatic validation, better error messages,
    and improved type safety compared to dataclasses.

    Attributes:
        title: Notification title text (non-empty, whitespace trimmed)
        message: Notification message body (non-empty, whitespace trimmed)
        level: Notification severity level
        timeout: Display timeout in seconds (1-300)
    """

    model_config = ConfigDict(frozen=True, strict=True)

    title: str = Field(min_length=1, description="Notification title")
    message: str = Field(min_length=1, description="Notification message body")
    level: NotificationLevel = NotificationLevel.INFO
    timeout: int = Field(default=10, ge=1, le=300, description="Display timeout in seconds")

    @field_validator("title", "message")
    @classmethod
    def strip_and_validate_text(cls, v: str) -> str:
        """Strip whitespace and validate text is not empty.

        Args:
            v: Input string value

        Returns:
            Stripped string value

        Raises:
            ValueError: If stripped string is empty
        """
        stripped = v.strip()
        if not stripped:
            raise ValueError("Text cannot be empty or whitespace-only")
        return stripped
