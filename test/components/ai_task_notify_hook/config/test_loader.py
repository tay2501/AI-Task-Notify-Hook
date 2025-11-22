"""Tests for config loader module.

This test suite validates configuration loading and validation functionality,
including EAFP-style error handling, default configuration fallback, and
edge cases for file I/O operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from ai_task_notify_hook.config import load_config, validate_config_file
from ai_task_notify_hook.config.models import ApplicationConfig
from ai_task_notify_hook.validation.exceptions import ConfigurationError


class TestLoadConfig:
    """Tests for load_config function."""

    def test_load_default_config_when_file_not_exists(
        self, tmp_path: Path
    ) -> None:
        """Test loading default config when file doesn't exist."""
        non_existent = tmp_path / "nonexistent.json"
        config = load_config(non_existent)

        assert isinstance(config, ApplicationConfig)
        assert config.version == "1.0.0"
        assert config.debug is False

    def test_load_config_from_valid_file(self, tmp_config_file: Path) -> None:
        """Test loading config from valid JSON file."""
        config = load_config(tmp_config_file)

        assert isinstance(config, ApplicationConfig)
        assert config.version == "1.0.0"
        assert config.debug is False
        assert config.notification.timeout == 10

    def test_load_config_with_custom_values(self, tmp_path: Path) -> None:
        """Test loading config with custom values."""
        config_path = tmp_path / "custom.json"
        config_data = {
            "version": "2.0.0",
            "debug": True,
            "notification": {"timeout": 30},
        }
        config_path.write_text(json.dumps(config_data), encoding="utf-8")

        config = load_config(config_path)

        assert config.version == "2.0.0"
        assert config.debug is True
        assert config.notification.timeout == 30

    def test_load_config_invalid_json(self, tmp_path: Path) -> None:
        """Test error handling for invalid JSON."""
        config_path = tmp_path / "invalid.json"
        config_path.write_text("{ invalid json }", encoding="utf-8")

        with pytest.raises(ConfigurationError, match="Failed to load"):
            load_config(config_path)

    def test_load_config_invalid_values(self, tmp_path: Path) -> None:
        """Test error handling for invalid configuration values."""
        config_path = tmp_path / "invalid_values.json"
        config_data = {"version": "invalid version format", "debug": "not a bool"}
        config_path.write_text(json.dumps(config_data), encoding="utf-8")

        with pytest.raises(ConfigurationError, match="Failed to load"):
            load_config(config_path)

    def test_load_config_os_error(self, tmp_path: Path) -> None:
        """Test error handling for OS-level errors (e.g., permission denied)."""
        config_path = tmp_path / "config.json"
        config_path.write_text('{"version": "1.0.0"}', encoding="utf-8")

        # Mock pathlib.Path.open to raise OSError
        with patch("pathlib.Path.open", side_effect=OSError("Permission denied")):
            with pytest.raises(ConfigurationError, match="Failed to read configuration file"):
                load_config(config_path)


class TestValidateConfigFile:
    """Tests for validate_config_file function."""

    def test_validate_valid_config(self, tmp_config_file: Path) -> None:
        """Test validation of valid config file."""
        assert validate_config_file(tmp_config_file) is True

    def test_validate_nonexistent_file(self, tmp_path: Path) -> None:
        """Test validation of non-existent file."""
        assert validate_config_file(tmp_path / "nonexistent.json") is False

    def test_validate_invalid_json(self, tmp_path: Path) -> None:
        """Test validation of invalid JSON file."""
        config_path = tmp_path / "invalid.json"
        config_path.write_text("{ invalid }", encoding="utf-8")

        assert validate_config_file(config_path) is False

    def test_validate_invalid_schema(self, tmp_path: Path) -> None:
        """Test validation of file with invalid schema."""
        config_path = tmp_path / "invalid_schema.json"
        # Pydantic allows extra fields by default, so use invalid type
        config_data = {"version": 123}  # version should be string
        config_path.write_text(json.dumps(config_data), encoding="utf-8")

        assert validate_config_file(config_path) is False
