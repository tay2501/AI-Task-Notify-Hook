"""Tests for models.core module.

This test suite validates the Pydantic models and enums used throughout
the application, ensuring strict validation, immutability, and proper
string handling according to Pydantic v2 best practices.
"""

from typing import Any

import pytest
from pydantic import ValidationError

from ai_task_notify_hook.models import LogLevel, NotificationLevel, NotificationRequest


# NotificationLevel tests
def test_notification_level_all_exist() -> None:
    """Test that all notification levels are defined."""
    assert NotificationLevel.INFO.value == "info"
    assert NotificationLevel.SUCCESS.value == "success"
    assert NotificationLevel.WARNING.value == "warning"
    assert NotificationLevel.ERROR.value == "error"


def test_notification_level_enum_equality() -> None:
    """Test enum equality comparison."""
    assert NotificationLevel.INFO == NotificationLevel.INFO
    assert NotificationLevel.ERROR != NotificationLevel.WARNING


def test_notification_level_str_conversion() -> None:
    """Test StrEnum automatic string conversion (Python 3.11+)."""
    level = NotificationLevel.INFO
    assert str(level) == "info"
    assert level == "info"  # StrEnum allows direct string comparison


# LogLevel tests
def test_log_level_all_exist() -> None:
    """Test that all log levels are defined."""
    assert LogLevel.DEBUG.value == "debug"
    assert LogLevel.INFO.value == "info"
    assert LogLevel.WARNING.value == "warning"
    assert LogLevel.ERROR.value == "error"
    assert LogLevel.CRITICAL.value == "critical"


def test_log_level_str_conversion() -> None:
    """Test StrEnum automatic string conversion (Python 3.11+)."""
    level = LogLevel.DEBUG
    assert str(level) == "debug"
    assert level == "debug"


# NotificationRequest tests
def test_notification_request_with_defaults() -> None:
    """Test creating notification request with default values."""
    request = NotificationRequest(title="Test", message="Test message")

    assert request.title == "Test"
    assert request.message == "Test message"
    assert request.level == NotificationLevel.INFO
    assert request.timeout == 10


def test_notification_request_with_custom_values() -> None:
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


def test_notification_request_immutable() -> None:
    """Test that NotificationRequest is immutable (Pydantic frozen model)."""
    request = NotificationRequest(title="Test", message="Test message")

    with pytest.raises(ValidationError, match="frozen"):
        request.title = "Modified"  # type: ignore[misc]


def test_notification_request_whitespace_stripping() -> None:
    """Test that whitespace is automatically stripped from title and message."""
    request = NotificationRequest(title="  Test  ", message="  Message  ")

    assert request.title == "Test"
    assert request.message == "Message"


def test_notification_request_empty_title() -> None:
    """Test validation fails for empty title."""
    with pytest.raises(ValueError, match="String should have at least 1 character|empty"):
        NotificationRequest(title="", message="Test message")


def test_notification_request_whitespace_only_title() -> None:
    """Test validation fails for whitespace-only title."""
    with pytest.raises(ValueError, match="empty"):
        NotificationRequest(title="   ", message="Test message")


def test_notification_request_empty_message() -> None:
    """Test validation fails for empty message."""
    with pytest.raises(ValueError, match="String should have at least 1 character|empty"):
        NotificationRequest(title="Test", message="")


def test_notification_request_whitespace_only_message() -> None:
    """Test validation fails for whitespace-only message."""
    with pytest.raises(ValueError, match="empty"):
        NotificationRequest(title="Test", message="   ")


def test_notification_request_timeout_zero() -> None:
    """Test validation fails for timeout of 0."""
    with pytest.raises(ValueError, match="greater than or equal to 1"):
        NotificationRequest(title="Test", message="Test message", timeout=0)


def test_notification_request_timeout_negative() -> None:
    """Test validation fails for negative timeout."""
    with pytest.raises(ValueError, match="greater than or equal to 1"):
        NotificationRequest(title="Test", message="Test message", timeout=-5)


def test_notification_request_timeout_too_high() -> None:
    """Test validation fails for timeout above maximum."""
    with pytest.raises(ValueError, match="less than or equal to 300"):
        NotificationRequest(title="Test", message="Test message", timeout=301)


def test_notification_request_timeout_way_too_high() -> None:
    """Test validation fails for very high timeout."""
    with pytest.raises(ValueError, match="less than or equal to 300"):
        NotificationRequest(title="Test", message="Test message", timeout=1000)


def test_notification_request_timeout_minimum_edge() -> None:
    """Test validation accepts minimum timeout value (1)."""
    request = NotificationRequest(title="Test", message="Test", timeout=1)
    assert request.timeout == 1


def test_notification_request_timeout_maximum_edge() -> None:
    """Test validation accepts maximum timeout value (300)."""
    request = NotificationRequest(title="Test", message="Test", timeout=300)
    assert request.timeout == 300


def test_notification_request_equality() -> None:
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


def test_notification_request_repr() -> None:
    """Test string representation of notification request."""
    request = NotificationRequest(title="Test", message="Message")
    repr_str = repr(request)

    assert "NotificationRequest" in repr_str
    assert "title='Test'" in repr_str
    assert "message='Message'" in repr_str


# Pydantic v2 Advanced Tests
@pytest.mark.parametrize(
    ("invalid_data", "expected_field"),
    [
        ({"title": "Test", "message": "Msg", "timeout": "not_an_int"}, "timeout"),
        ({"title": "Test", "message": "Msg", "level": "invalid"}, "level"),
        ({"title": 123, "message": "Msg"}, "title"),
        ({"title": "Test", "message": 456}, "message"),
    ],
)
def test_notification_request_strict_validation(
    invalid_data: dict[str, Any], expected_field: str
) -> None:
    """Test strict validation rejects type coercion in strict mode."""
    with pytest.raises(ValidationError) as exc_info:
        NotificationRequest.model_validate(invalid_data, strict=True)
    # Check if expected field appears in validation errors
    errors = exc_info.value.errors()
    assert any(err["loc"][0] == expected_field for err in errors), f"Expected error for field {expected_field}"


def test_notification_request_model_validate_json() -> None:
    """Test JSON validation with model_validate_json method."""
    json_data = '{"title": "Test", "message": "Message", "timeout": 20}'
    request = NotificationRequest.model_validate_json(json_data)

    assert request.title == "Test"
    assert request.message == "Message"
    assert request.timeout == 20


def test_notification_request_model_dump() -> None:
    """Test model serialization with model_dump method."""
    request = NotificationRequest(title="Test", message="Message", timeout=15)
    data = request.model_dump()

    assert data == {
        "title": "Test",
        "message": "Message",
        "level": "info",
        "timeout": 15,
    }


def test_notification_request_model_dump_json() -> None:
    """Test JSON serialization with model_dump_json method."""
    request = NotificationRequest(title="Test", message="Message")
    json_str = request.model_dump_json()

    assert '"title":"Test"' in json_str
    assert '"message":"Message"' in json_str


@pytest.mark.parametrize(
    "level",
    [NotificationLevel.INFO, NotificationLevel.SUCCESS, NotificationLevel.WARNING, NotificationLevel.ERROR],
)
def test_notification_request_all_levels(level: NotificationLevel) -> None:
    """Test NotificationRequest creation with all notification levels."""
    request = NotificationRequest(title="Test", message="Message", level=level)
    assert request.level == level
