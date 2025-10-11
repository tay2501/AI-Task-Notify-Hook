"""Configuration loading with EAFP style.

This module handles loading configuration from JSON files,
following the "Easier to Ask for Forgiveness than Permission" approach.
"""

import json
from pathlib import Path

from ai_task_notify_hook.config.models import ApplicationConfig
from ai_task_notify_hook.validation.exceptions import ConfigurationError


def load_config(config_path: str | Path | None = None) -> ApplicationConfig:
    """Load configuration from JSON file with EAFP style.

    Args:
        config_path: Path to JSON configuration file.
                    Defaults to "config/config.json" if not specified.

    Returns:
        Validated ApplicationConfig instance.

    Raises:
        ConfigurationError: If configuration file exists but cannot be loaded.

    Examples:
        >>> config = load_config()  # Use default path
        >>> config = load_config("custom_config.json")  # Custom path
    """
    config_path = Path(config_path) if config_path else Path("config/config.json")

    # Return default configuration if file doesn't exist
    if not config_path.exists():
        return ApplicationConfig()

    # Try to load and validate configuration (EAFP style)
    try:
        with config_path.open(encoding="utf-8") as f:
            data = json.load(f)
        return ApplicationConfig.model_validate(data)
    except (json.JSONDecodeError, ValueError) as exc:
        raise ConfigurationError(
            f"Failed to load configuration from {config_path}: {exc}"
        ) from exc
    except OSError as exc:
        raise ConfigurationError(
            f"Failed to read configuration file {config_path}: {exc}"
        ) from exc


def validate_config_file(config_path: str | Path) -> bool:
    """Validate configuration file without loading it.

    Args:
        config_path: Path to JSON configuration file.

    Returns:
        True if configuration file is valid, False otherwise.

    Examples:
        >>> if validate_config_file("config.json"):
        ...     config = load_config("config.json")
    """
    config_path = Path(config_path)

    if not config_path.exists():
        return False

    try:
        with config_path.open(encoding="utf-8") as f:
            data = json.load(f)
        ApplicationConfig.model_validate(data)
        return True
    except (json.JSONDecodeError, ValueError, OSError):
        return False
