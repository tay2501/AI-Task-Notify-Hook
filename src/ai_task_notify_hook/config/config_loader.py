#!/usr/bin/env python3
"""
Configuration loader module for notification settings.
Provides type-safe configuration loading with validation and fallback.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    from .log_config import get_logger

    logger = get_logger("config_loader")
except ImportError:
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("config_loader")


@dataclass(frozen=True)
class NotificationConfig:
    """Notification display settings."""

    app_name: str = "Claude Code"
    timeout: int = 10

    def __post_init__(self) -> None:
        """Validate configuration values after initialization."""
        if not isinstance(self.app_name, str) or not self.app_name.strip():
            raise ValueError("app_name must be a non-empty string")

        if not isinstance(self.timeout, int) or self.timeout < 1 or self.timeout > 300:
            raise ValueError("timeout must be an integer between 1 and 300 seconds")


@dataclass(frozen=True)
class ApplicationConfig:
    """Application-level settings."""

    version: str = "1.0.0"
    debug: bool = False

    def __post_init__(self) -> None:
        """Validate configuration values after initialization."""
        if not isinstance(self.version, str) or not self.version.strip():
            raise ValueError("version must be a non-empty string")

        if not isinstance(self.debug, bool):
            raise ValueError("debug must be a boolean value")


@dataclass(frozen=True)
class Config:
    """Main configuration container."""

    notification: NotificationConfig = field(default_factory=NotificationConfig)
    application: ApplicationConfig = field(default_factory=ApplicationConfig)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Config:
        """Create Config instance from dictionary with validation.

        Args:
            data: Configuration dictionary

        Returns:
            Validated Config instance

        Raises:
            ValueError: If configuration is invalid
            KeyError: If required keys are missing
        """
        try:
            notification_data = data.get("notification", {})
            application_data = data.get("application", {})

            notification = NotificationConfig(
                app_name=notification_data.get("app_name", "Claude Code"),
                timeout=notification_data.get("timeout", 10),
            )

            application = ApplicationConfig(
                version=application_data.get("version", "1.0.0"),
                debug=application_data.get("debug", False),
            )

            return cls(notification=notification, application=application)

        except Exception as exc:
            raise ValueError(f"Invalid configuration data: {exc}") from exc


def load_config(config_path: str | Path = "config/config.json") -> Config:
    """Load configuration from JSON file with fallback to defaults.

    Args:
        config_path: Path to JSON configuration file

    Returns:
        Validated Config instance
    """
    config_path = Path(config_path)

    # Try to load from file
    if config_path.exists():
        try:
            with config_path.open(encoding="utf-8") as file:
                data = json.load(file)

            config = Config.from_dict(data)
            logger.info(
                "Configuration loaded successfully",
                config_file=str(config_path),
                app_name=config.notification.app_name,
                timeout=config.notification.timeout,
            )
            return config

        except json.JSONDecodeError as exc:
            logger.error(
                "Invalid JSON in configuration file",
                config_file=str(config_path),
                error=str(exc),
            )
        except ValueError as exc:
            logger.error(
                "Invalid configuration values",
                config_file=str(config_path),
                error=str(exc),
            )
        except Exception as exc:
            logger.error(
                "Failed to load configuration file",
                config_file=str(config_path),
                error=str(exc),
            )
    else:
        logger.info(
            "Configuration file not found, using defaults", config_file=str(config_path)
        )

    # Fallback to defaults
    config = Config()
    logger.info(
        "Using default configuration",
        app_name=config.notification.app_name,
        timeout=config.notification.timeout,
    )
    return config


def validate_config_file(config_path: str | Path = "config/config.json") -> bool:
    """Validate configuration file without loading it.

    Args:
        config_path: Path to JSON configuration file

    Returns:
        True if valid, False otherwise
    """
    config_path = Path(config_path)

    if not config_path.exists():
        logger.warning(
            "Configuration file does not exist", config_file=str(config_path)
        )
        return False

    try:
        with config_path.open(encoding="utf-8") as file:
            data = json.load(file)

        # Validate by trying to create Config instance
        Config.from_dict(data)
        logger.info("Configuration file is valid", config_file=str(config_path))
        return True

    except json.JSONDecodeError as exc:
        logger.error(
            "Invalid JSON syntax", config_file=str(config_path), error=str(exc)
        )
        return False
    except ValueError as exc:
        logger.error(
            "Invalid configuration values", config_file=str(config_path), error=str(exc)
        )
        return False
    except Exception as exc:
        logger.error(
            "Configuration validation failed",
            config_file=str(config_path),
            error=str(exc),
        )
        return False


def create_default_config(config_path: str | Path = "config/config.json") -> None:
    """Create default configuration file.

    Args:
        config_path: Path where to create the configuration file
    """
    config_path = Path(config_path)

    default_config = {
        "notification": {"app_name": "Claude Code", "timeout": 10},
        "application": {"version": "1.0.0", "debug": False},
    }

    try:
        with config_path.open("w", encoding="utf-8") as file:
            json.dump(default_config, file, indent=2, ensure_ascii=False)

        logger.info("Default configuration file created", config_file=str(config_path))

    except Exception as exc:
        logger.error(
            "Failed to create configuration file",
            config_file=str(config_path),
            error=str(exc),
        )
        raise


if __name__ == "__main__":
    # Test configuration loading
    try:
        config = load_config()
        print(f"App Name: {config.notification.app_name}")
        print(f"Timeout: {config.notification.timeout}")
        print(f"Version: {config.application.version}")
        print(f"Debug: {config.application.debug}")
        print("Configuration loading test successful")
    except Exception as exc:
        print(f"Configuration loading test failed: {exc}")
        sys.exit(1)
