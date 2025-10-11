"""Shared pytest fixtures and configuration for all tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.fixture
def tmp_config_file(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary configuration file for testing.

    Args:
        tmp_path: Pytest's temporary directory fixture

    Yields:
        Path to the temporary config file
    """
    config_path = tmp_path / "config.json"
    config_data = {
        "version": "1.0.0",
        "debug": False,
        "notification": {"timeout": 10},
    }
    config_path.write_text(json.dumps(config_data), encoding="utf-8")
    yield config_path


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
