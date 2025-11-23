"""Shared pytest fixtures and configuration for all tests."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, cast

import pytest

if TYPE_CHECKING:
    from pathlib import Path


# Pytest configuration
def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest markers."""
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")


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
        "notification": {"timeout": 10},
    }
    config_path.write_text(json.dumps(config_data), encoding="utf-8")
    return config_path


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


@pytest.fixture
def sample_valid_config() -> dict[str, bool | str | dict[str, int]]:
    """Provide sample valid configuration data for testing.

    Returns:
        Dictionary with valid configuration parameters
    """
    return {
        "version": "1.0.0",
        "debug": False,
        "notification": {"timeout": 15},
    }


@pytest.fixture(params=["info", "success", "warning", "error"])
def notification_level_string(request: pytest.FixtureRequest) -> str:
    """Parametrized fixture providing all notification level strings.

    Args:
        request: Pytest fixture request object

    Returns:
        Notification level string
    """
    return cast("str", request.param)
