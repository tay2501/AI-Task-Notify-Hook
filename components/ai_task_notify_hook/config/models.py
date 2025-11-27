"""Configuration models using Pydantic validation.

This module defines Pydantic models for configuration data,
providing automatic validation and type checking.

Updated with Pydantic v2 best practices:
- BaseConfig with shared settings (extra='forbid', frozen=True)
- Annotated pattern for reusable field constraints
- Declarative field constraints for Rust engine optimization
"""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class BaseConfig(BaseModel):
    """Base configuration model with shared Pydantic v2 settings.

    Provides common configuration for all config models:
    - extra='forbid': Reject unknown fields to catch typos early
    - frozen=True: Immutable config objects for safety
    - strict=True: Strict type checking, no coercion
    - validate_default=True: Validate default values
    - str_strip_whitespace=True: Auto-trim string inputs
    """

    model_config = ConfigDict(
        extra="forbid",  # Fail fast on unknown fields (catch typos)
        frozen=True,  # Immutable configuration
        strict=True,  # Strict type checking
        validate_default=True,  # Validate defaults
        str_strip_whitespace=True,  # Auto-trim strings
    )


# Reusable annotated types using Pydantic v2 pattern
AppName = Annotated[str, Field(min_length=1, max_length=100)]
TimeoutSeconds = Annotated[int, Field(ge=1, le=300)]
SemverVersion = Annotated[str, Field(pattern=r"^\d+\.\d+\.\d+$")]


class NotificationConfig(BaseConfig):
    """Notification display settings with Pydantic validation.

    Inherits common configuration from BaseConfig and adds
    notification-specific settings.
    """

    app_name: AppName = "Claude Code"
    timeout: TimeoutSeconds = 10


class ApplicationConfig(BaseConfig):
    """Application configuration with Pydantic validation.

    Inherits common configuration from BaseConfig and adds
    application-level settings.
    """

    version: SemverVersion = "1.0.0"
    debug: bool = False
    notification: NotificationConfig = Field(default_factory=NotificationConfig)
