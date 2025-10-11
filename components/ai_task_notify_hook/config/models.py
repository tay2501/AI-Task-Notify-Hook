"""Configuration models using Pydantic validation.

This module defines Pydantic models for configuration data,
providing automatic validation and type checking.
"""

from pydantic import BaseModel, ConfigDict, Field


class NotificationConfig(BaseModel):
    """Notification display settings with Pydantic validation."""

    model_config = ConfigDict(frozen=True, strict=True)

    app_name: str = Field(
        default="Claude Code",
        min_length=1,
        description="Application name displayed in notifications",
    )
    timeout: int = Field(
        default=10, ge=1, le=300, description="Notification timeout in seconds"
    )


class ApplicationConfig(BaseModel):
    """Application configuration with Pydantic validation."""

    model_config = ConfigDict(frozen=True, strict=True)

    version: str = Field(
        default="1.0.0",
        pattern=r"^\d+\.\d+\.\d+$",
        description="Version in semver format",
    )
    debug: bool = Field(default=False, description="Enable debug mode")
    notification: NotificationConfig = Field(
        default_factory=NotificationConfig, description="Notification settings"
    )
