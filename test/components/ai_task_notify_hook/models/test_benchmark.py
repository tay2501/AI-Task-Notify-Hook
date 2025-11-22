"""Benchmark tests for models.core module.

This test suite uses pytest-benchmark to measure performance of
NotificationRequest creation and validation operations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ai_task_notify_hook.models import NotificationLevel, NotificationRequest

if TYPE_CHECKING:
    from pytest_benchmark.fixture import BenchmarkFixture


class TestNotificationRequestBenchmark:
    """Benchmark tests for NotificationRequest."""

    def test_benchmark_notification_request_creation(self, benchmark: BenchmarkFixture) -> None:
        """Benchmark NotificationRequest creation with defaults."""

        def create_request() -> NotificationRequest:
            return NotificationRequest(title="Benchmark Test", message="Performance measurement")

        result = benchmark(create_request)
        assert result.title == "Benchmark Test"

    def test_benchmark_notification_request_with_validation(self, benchmark: BenchmarkFixture) -> None:
        """Benchmark NotificationRequest creation with custom values and validation."""

        def create_and_validate() -> NotificationRequest:
            return NotificationRequest(
                title="  Test Title  ",
                message="  Test Message  ",
                level=NotificationLevel.ERROR,
                timeout=30,
            )

        result = benchmark(create_and_validate)
        assert result.title == "Test Title"  # Whitespace stripped
        assert result.timeout == 30

    def test_benchmark_model_validate(self, benchmark: BenchmarkFixture) -> None:
        """Benchmark model_validate method with dict input."""
        data: dict[str, Any] = {
            "title": "Test",
            "message": "Message",
            "level": NotificationLevel.WARNING,
            "timeout": 25,
        }

        result = benchmark(NotificationRequest.model_validate, data)
        assert result.level == NotificationLevel.WARNING

    def test_benchmark_model_dump(self, benchmark: BenchmarkFixture) -> None:
        """Benchmark model serialization with model_dump."""
        request = NotificationRequest(
            title="Test", message="Message", level=NotificationLevel.SUCCESS, timeout=15
        )

        result: dict[str, Any] = benchmark(request.model_dump)
        assert result["level"] == "success"

    def test_benchmark_model_validate_json(self, benchmark: BenchmarkFixture) -> None:
        """Benchmark JSON deserialization with model_validate_json."""
        json_data = '{"title": "Test", "message": "Message", "level": "info", "timeout": 20}'

        result = benchmark(NotificationRequest.model_validate_json, json_data)
        assert result.timeout == 20

    def test_benchmark_model_dump_json(self, benchmark: BenchmarkFixture) -> None:
        """Benchmark JSON serialization with model_dump_json."""
        request = NotificationRequest(title="Test", message="Message", timeout=10)

        result: str = benchmark(request.model_dump_json)
        assert '"title":"Test"' in result
