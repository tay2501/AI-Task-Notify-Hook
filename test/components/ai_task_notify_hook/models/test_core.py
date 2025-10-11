"""Tests for models.core module."""

import pytest

from ai_task_notify_hook.models import LogLevel, NotificationLevel, NotificationRequest


class TestNotificationLevel:
    """Tests for NotificationLevel enum."""

    def test_all_levels_exist(self) -> None:
        """Test that all notification levels are defined."""
        assert NotificationLevel.INFO.value == "info"
        assert NotificationLevel.SUCCESS.value == "success"
        assert NotificationLevel.WARNING.value == "warning"
        assert NotificationLevel.ERROR.value == "error"

    def test_enum_equality(self) -> None:
        """Test enum equality comparison."""
        assert NotificationLevel.INFO == NotificationLevel.INFO
        assert NotificationLevel.ERROR != NotificationLevel.WARNING


class TestLogLevel:
    """Tests for LogLevel enum."""

    def test_all_levels_exist(self) -> None:
        """Test that all log levels are defined."""
        assert LogLevel.DEBUG.value == "debug"
        assert LogLevel.INFO.value == "info"
        assert LogLevel.WARNING.value == "warning"
        assert LogLevel.ERROR.value == "error"
        assert LogLevel.CRITICAL.value == "critical"


class TestNotificationRequest:
    """Tests for NotificationRequest dataclass."""

    def test_create_with_defaults(self) -> None:
        """Test creating notification request with default values."""
        request = NotificationRequest(title="Test", message="Test message")

        assert request.title == "Test"
        assert request.message == "Test message"
        assert request.level == NotificationLevel.INFO
        assert request.timeout == 10

    def test_create_with_custom_values(self) -> None:
        """Test creating notification request with custom values."""
        request = NotificationRequest(
            title="Error",
            message="Something went wrong",
            level=NotificationLevel.ERROR,
            timeout=30,
        )

        assert request.title == "Error"
        assert request.message == "Something went wrong"
        assert request.level == NotificationLevel.ERROR
        assert request.timeout == 30

    def test_immutable(self) -> None:
        """Test that NotificationRequest is immutable (frozen dataclass)."""
        request = NotificationRequest(title="Test", message="Test message")

        with pytest.raises(AttributeError):
            request.title = "Modified"  # type: ignore[misc]

    def test_validation_empty_title(self) -> None:
        """Test validation fails for empty title."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            NotificationRequest(title="", message="Test message")

        with pytest.raises(ValueError, match="Title cannot be empty"):
            NotificationRequest(title="   ", message="Test message")

    def test_validation_empty_message(self) -> None:
        """Test validation fails for empty message."""
        with pytest.raises(ValueError, match="Message cannot be empty"):
            NotificationRequest(title="Test", message="")

        with pytest.raises(ValueError, match="Message cannot be empty"):
            NotificationRequest(title="Test", message="   ")

    def test_validation_timeout_too_low(self) -> None:
        """Test validation fails for timeout below minimum."""
        with pytest.raises(ValueError, match="Timeout must be between 1 and 300"):
            NotificationRequest(title="Test", message="Test message", timeout=0)

        with pytest.raises(ValueError, match="Timeout must be between 1 and 300"):
            NotificationRequest(title="Test", message="Test message", timeout=-5)

    def test_validation_timeout_too_high(self) -> None:
        """Test validation fails for timeout above maximum."""
        with pytest.raises(ValueError, match="Timeout must be between 1 and 300"):
            NotificationRequest(title="Test", message="Test message", timeout=301)

        with pytest.raises(ValueError, match="Timeout must be between 1 and 300"):
            NotificationRequest(title="Test", message="Test message", timeout=1000)

    def test_validation_timeout_edge_cases(self) -> None:
        """Test validation accepts edge case timeout values."""
        request_min = NotificationRequest(title="Test", message="Test", timeout=1)
        assert request_min.timeout == 1

        request_max = NotificationRequest(title="Test", message="Test", timeout=300)
        assert request_max.timeout == 300

    def test_equality(self) -> None:
        """Test equality comparison between notification requests."""
        request1 = NotificationRequest(
            title="Test", message="Message", level=NotificationLevel.INFO, timeout=10
        )
        request2 = NotificationRequest(
            title="Test", message="Message", level=NotificationLevel.INFO, timeout=10
        )
        request3 = NotificationRequest(
            title="Different",
            message="Message",
            level=NotificationLevel.INFO,
            timeout=10,
        )

        assert request1 == request2
        assert request1 != request3

    def test_repr(self) -> None:
        """Test string representation of notification request."""
        request = NotificationRequest(title="Test", message="Message")
        repr_str = repr(request)

        assert "NotificationRequest" in repr_str
        assert "title='Test'" in repr_str
        assert "message='Message'" in repr_str
