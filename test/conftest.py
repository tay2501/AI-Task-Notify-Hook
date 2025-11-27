"""Shared pytest fixtures and configuration for all tests.

Modern pytest patterns with:
- Type-safe fixtures using Python 3.13 type hints
- Pydantic v2 model fixtures
- Parametrized fixtures for comprehensive testing
- Reusable temporary file fixtures
"""

from __future__ import annotations

import json
from pathlib import Path  # noqa: TC003  # Path is used at runtime for fixtures
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from ai_task_notify_hook.config.models import ApplicationConfig, NotificationConfig
    from ai_task_notify_hook.models import NotificationLevel


# Pytest configuration
def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest markers and settings."""
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")


# ============================================================================
# Configuration Fixtures
# ============================================================================


@pytest.fixture
def tmp_config_file(tmp_path: Path) -> Path:
    """Create a temporary configuration file for testing.

    Args:
        tmp_path: Pytest's temporary directory fixture

    Returns:
        Path to the temporary config file
    """
    config_path = tmp_path / "config.json"
    config_data = {
        "version": "1.0.0",
        "debug": False,
        "notification": {"timeout": 10, "app_name": "Test App"},
    }
    config_path.write_text(json.dumps(config_data), encoding="utf-8")
    return config_path


@pytest.fixture
def sample_valid_config() -> dict[str, bool | str | dict[str, int | str]]:
    """Provide sample valid configuration data for testing.

    Returns:
        Dictionary with valid configuration parameters
    """
    return {
        "version": "1.0.0",
        "debug": False,
        "notification": {"timeout": 15, "app_name": "Test Application"},
    }


@pytest.fixture
def test_notification_config() -> NotificationConfig:
    """Provide a test NotificationConfig instance.

    Returns:
        NotificationConfig instance for testing
    """
    from ai_task_notify_hook.config.models import NotificationConfig

    return NotificationConfig(app_name="Test App", timeout=5)


@pytest.fixture
def test_application_config() -> ApplicationConfig:
    """Provide a test ApplicationConfig instance.

    Returns:
        ApplicationConfig instance for testing
    """
    from ai_task_notify_hook.config.models import ApplicationConfig, NotificationConfig

    return ApplicationConfig(
        version="1.0.0-test",
        debug=True,
        notification=NotificationConfig(app_name="Test App", timeout=5),
    )


# ============================================================================
# Notification Fixtures
# ============================================================================


@pytest.fixture
def sample_notification_data() -> dict[str, str | int]:
    """Provide sample notification data for testing.

    Returns:
        Dictionary with notification parameters
    """
    return {
        "title": "Test Notification",
        "message": "This is a test message",
        "timeout": 5,
    }


@pytest.fixture(params=["info", "success", "warning", "error"])
def notification_level_string(request: pytest.FixtureRequest) -> str:
    """Parametrized fixture providing all notification level strings.

    Args:
        request: Pytest fixture request object

    Returns:
        Notification level string
    """
    return str(request.param)


@pytest.fixture(params=["INFO", "SUCCESS", "WARNING", "ERROR"])
def notification_level_enum(request: pytest.FixtureRequest) -> NotificationLevel:
    """Parametrized fixture providing all NotificationLevel enum values.

    Args:
        request: Pytest fixture request object

    Returns:
        NotificationLevel enum value
    """
    from ai_task_notify_hook.models import NotificationLevel

    return NotificationLevel[str(request.param)]


# ============================================================================
# Temporary Path Fixtures
# ============================================================================


@pytest.fixture
def temp_json_file(tmp_path: Path) -> Path:
    """Create a temporary JSON file.

    Args:
        tmp_path: Pytest's temporary directory fixture

    Returns:
        Path to an empty temporary JSON file
    """
    json_file = tmp_path / "temp.json"
    json_file.write_text("{}", encoding="utf-8")
    return json_file


@pytest.fixture
def temp_invalid_json_file(tmp_path: Path) -> Path:
    """Create a temporary invalid JSON file for error testing.

    Args:
        tmp_path: Pytest's temporary directory fixture

    Returns:
        Path to a temporary file with invalid JSON
    """
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text("{invalid json}", encoding="utf-8")
    return invalid_file
