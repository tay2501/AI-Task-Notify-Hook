"""Configuration loading with EAFP style.

This module handles loading configuration from JSON files,
following the "Easier to Ask for Forgiveness than Permission" approach.

Updated with Pydantic v2 performance optimizations:
- TypeAdapter caching for reuse across multiple load calls
- Direct JSON validation with model_validate_json() for better performance
"""

from functools import lru_cache
from pathlib import Path

from pydantic import TypeAdapter

from ai_task_notify_hook.config.models import ApplicationConfig
from ai_task_notify_hook.validation.exceptions import ConfigurationError


@lru_cache(maxsize=1)
def _get_config_adapter() -> TypeAdapter[ApplicationConfig]:
    """Get cached TypeAdapter for ApplicationConfig validation.

    Uses functools.lru_cache to reuse the TypeAdapter instance across
    multiple load_config() calls, improving performance by avoiding
    repeated validator construction.

    Returns:
        Cached TypeAdapter instance for ApplicationConfig
    """
    return TypeAdapter(ApplicationConfig)


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
    # Use model_validate_json() for better performance (10-30% faster)
    # by validating JSON directly without intermediate dict conversion
    try:
        json_data = config_path.read_bytes()
        # Use cached TypeAdapter for improved performance on repeated calls
        adapter = _get_config_adapter()
        return adapter.validate_json(json_data)
    except ValueError as exc:
        # Pydantic ValidationError is a subclass of ValueError
        raise ConfigurationError(
            f"Failed to load configuration from {config_path}: {exc}"
        ) from exc
    except OSError as exc:
        raise ConfigurationError(
            f"Failed to read configuration file {config_path}: {exc}"
        ) from exc


def validate_config_file(config_path: str | Path) -> bool:
    """Validate configuration file without loading it.

    Uses cached TypeAdapter for improved performance.

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
        json_data = config_path.read_bytes()
        adapter = _get_config_adapter()
        adapter.validate_json(json_data)
        return True
    except (ValueError, OSError):
        return False
