"""Tests for validation.core module.

Comprehensive tests for platform and backend validation functionality,
following AAA (Arrange-Act-Assert) pattern and best practices.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from ai_task_notify_hook.validation import (
    NotificationBackendError,
    require_notification_backend,
    validate_backend_available,
    validate_platform_support,
)


class TestValidatePlatformSupport:
    """Tests for validate_platform_support function."""

    @patch("ai_task_notify_hook.validation.core.platform.system")
    def test_validate_platform_windows(self, mock_system: MagicMock) -> None:
        """Test validation passes on Windows platform."""
        # Arrange
        mock_system.return_value = "Windows"

        # Act & Assert
        assert validate_platform_support() is True

    @patch("ai_task_notify_hook.validation.core.platform.system")
    def test_validate_platform_macos(self, mock_system: MagicMock) -> None:
        """Test validation passes on macOS (Darwin) platform."""
        # Arrange
        mock_system.return_value = "Darwin"

        # Act & Assert
        assert validate_platform_support() is True

    @patch("ai_task_notify_hook.validation.core.platform.system")
    def test_validate_platform_linux(self, mock_system: MagicMock) -> None:
        """Test validation passes on Linux platform."""
        # Arrange
        mock_system.return_value = "Linux"

        # Act & Assert
        assert validate_platform_support() is True

    @patch("ai_task_notify_hook.validation.core.platform.system")
    def test_validate_platform_unsupported(self, mock_system: MagicMock) -> None:
        """Test validation fails on unsupported platforms."""
        # Arrange
        mock_system.return_value = "FreeBSD"

        # Act & Assert
        with pytest.raises(NotificationBackendError, match="Platform 'FreeBSD' not supported"):
            validate_platform_support()

    @patch("ai_task_notify_hook.validation.core.platform.system")
    def test_validate_platform_error_message_includes_supported(
        self, mock_system: MagicMock
    ) -> None:
        """Test error message includes list of supported platforms."""
        # Arrange
        mock_system.return_value = "SunOS"

        # Act & Assert
        # Error message lists platforms alphabetically: Darwin, Linux, Windows
        with pytest.raises(
            NotificationBackendError, match=r"Supported platforms:.*Darwin.*Linux.*Windows"
        ):
            validate_platform_support()


class TestValidateBackendAvailable:
    """Tests for validate_backend_available function."""

    @patch("ai_task_notify_hook.validation.core.platform.system")
    def test_validate_backend_available_success(self, mock_system: MagicMock) -> None:
        """Test validation passes when plyer is properly installed."""
        # Arrange
        mock_system.return_value = "Windows"

        # Act & Assert
        # Real plyer import - should succeed in test environment
        assert validate_backend_available() is True

    def test_validate_backend_import_error(self) -> None:
        """Test validation fails when plyer cannot be imported."""
        # Arrange - mock builtins.__import__ to simulate missing plyer
        original_import = __builtins__["__import__"]  # type: ignore[index]

        def mock_import(name: str, *args: object, **kwargs: object) -> object:
            if name == "plyer":
                raise ImportError("No module named 'plyer'")
            return original_import(name, *args, **kwargs)

        # Act & Assert
        with (
            patch("builtins.__import__", side_effect=mock_import),
            pytest.raises(NotificationBackendError, match="plyer library not installed"),
        ):
            validate_backend_available()

    @patch("ai_task_notify_hook.validation.core.platform.system")
    def test_validate_backend_no_notify_method(self, mock_system: MagicMock) -> None:
        """Test validation fails when notification.notify method is missing."""
        # Arrange
        mock_system.return_value = "Linux"
        mock_notification = MagicMock(spec=[])  # Empty spec - no 'notify' method

        # Act & Assert
        with (
            patch.dict("sys.modules", {"plyer": MagicMock(notification=mock_notification)}),
            pytest.raises(NotificationBackendError, match="notify method not available"),
        ):
            validate_backend_available()


class TestRequireNotificationBackendDecorator:
    """Tests for require_notification_backend decorator."""

    @patch("ai_task_notify_hook.validation.core.validate_backend_available")
    @patch("ai_task_notify_hook.validation.core.validate_platform_support")
    def test_decorator_validates_before_execution(
        self, mock_platform: MagicMock, mock_backend: MagicMock
    ) -> None:
        """Test decorator validates platform and backend before function execution."""
        # Arrange
        mock_platform.return_value = True
        mock_backend.return_value = True

        @require_notification_backend
        def test_func() -> None:
            """Test function."""

        # Act
        test_func()

        # Assert
        mock_platform.assert_called_once()
        mock_backend.assert_called_once()

    @patch("ai_task_notify_hook.validation.core.validate_backend_available")
    @patch(
        "ai_task_notify_hook.validation.core.validate_platform_support",
        side_effect=NotificationBackendError("Platform not supported"),
    )
    def test_decorator_propagates_platform_error(
        self, mock_platform: MagicMock, mock_backend: MagicMock
    ) -> None:
        """Test decorator propagates platform validation errors."""
        # Arrange
        @require_notification_backend
        def test_func() -> None:
            """Test function."""

        # Act & Assert
        with pytest.raises(NotificationBackendError, match="Platform not supported"):
            test_func()

        mock_platform.assert_called_once()
        mock_backend.assert_not_called()  # Should fail before backend check

    @patch(
        "ai_task_notify_hook.validation.core.validate_backend_available",
        side_effect=NotificationBackendError("Backend unavailable"),
    )
    @patch("ai_task_notify_hook.validation.core.validate_platform_support")
    def test_decorator_propagates_backend_error(
        self, mock_platform: MagicMock, mock_backend: MagicMock
    ) -> None:
        """Test decorator propagates backend validation errors."""
        # Arrange
        mock_platform.return_value = True

        @require_notification_backend
        def test_func() -> None:
            """Test function."""

        # Act & Assert
        with pytest.raises(NotificationBackendError, match="Backend unavailable"):
            test_func()

        mock_platform.assert_called_once()
        mock_backend.assert_called_once()

    @patch("ai_task_notify_hook.validation.core.validate_backend_available")
    @patch("ai_task_notify_hook.validation.core.validate_platform_support")
    def test_decorator_passes_arguments_to_function(
        self, mock_platform: MagicMock, mock_backend: MagicMock
    ) -> None:
        """Test decorator correctly passes arguments to decorated function."""
        # Arrange
        mock_platform.return_value = True
        mock_backend.return_value = True
        result_container: dict[str, object] = {"called": False, "args": None, "kwargs": None}

        @require_notification_backend
        def test_func(*args: object, **kwargs: object) -> None:
            """Test function that captures arguments."""
            result_container["called"] = True
            result_container["args"] = args
            result_container["kwargs"] = kwargs

        # Act
        test_func("arg1", "arg2", key1="value1", key2="value2")

        # Assert
        assert result_container["called"] is True
        assert result_container["args"] == ("arg1", "arg2")
        assert result_container["kwargs"] == {"key1": "value1", "key2": "value2"}
