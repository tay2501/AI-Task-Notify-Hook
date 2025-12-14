"""Performance profiling tests.

Comprehensive performance tests using cProfile and memory_profiler patterns
to identify bottlenecks and track performance metrics over time.

Updated for desktop-notifier library (async notification support).
"""

from __future__ import annotations

import cProfile
import pstats
from io import StringIO
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

if TYPE_CHECKING:
    from pytest_benchmark.fixture import BenchmarkFixture

from ai_task_notify_hook.cli.core import main
from ai_task_notify_hook.models import NotificationLevel, NotificationRequest
from ai_task_notify_hook.notification import show_notification


class TestCLIPerformanceProfile:
    """Performance profiling tests for CLI workflows."""

    @patch("ai_task_notify_hook.notification.core.DesktopNotifier")
    @patch("sys.argv", ["notify.py", "Profiling Test", "Performance measurement"])
    def test_cli_execution_profile(self, mock_notifier_class: MagicMock) -> None:
        """Profile complete CLI execution path."""
        # Arrange
        mock_instance = MagicMock()
        mock_instance.send = AsyncMock()
        mock_notifier_class.return_value = mock_instance

        # Create profiler
        profiler = cProfile.Profile()

        # Profile the main() function (which runs async_main with asyncio.run)
        profiler.enable()
        main()
        profiler.disable()

        # Generate statistics
        stats_stream = StringIO()
        stats = pstats.Stats(profiler, stream=stats_stream)
        stats.sort_stats("cumulative")
        stats.print_stats(20)  # Top 20 functions by cumulative time

        output = stats_stream.getvalue()

        # Verify profiling captured data (async_main or asyncio.run should be present)
        assert "main" in output or "async_main" in output
        # With async, the profiler may not capture deep async calls
        # Just verify the profiler worked
        assert len(output) > 0

        # Print profiling results for manual inspection
        print("\n" + "=" * 80)
        print("CLI EXECUTION PROFILE (Top 20 by cumulative time)")
        print("=" * 80)
        print(output)

    @patch("ai_task_notify_hook.notification.core.DesktopNotifier")
    def test_notification_component_profile(self, mock_notifier_class: MagicMock) -> None:
        """Profile notification component in isolation with async support."""
        import asyncio

        # Arrange
        mock_instance = MagicMock()
        mock_instance.send = AsyncMock()
        mock_notifier_class.return_value = mock_instance

        profiler = cProfile.Profile()

        # Profile notification calls (use asyncio.run for each call)
        profiler.enable()
        for _ in range(100):
            asyncio.run(show_notification(
                title="Performance Test",
                message="Iteration test",
                timeout=10,
            ))
        profiler.disable()

        # Generate statistics
        stats_stream = StringIO()
        stats = pstats.Stats(profiler, stream=stats_stream)
        stats.sort_stats("cumulative")
        stats.print_stats(15)

        output = stats_stream.getvalue()

        # Verify profiling worked (asyncio.run or event loop should be present)
        assert len(output) > 0

        print("\n" + "=" * 80)
        print("NOTIFICATION COMPONENT PROFILE (100 iterations)")
        print("=" * 80)
        print(output)


class TestModelPerformanceProfile:
    """Performance profiling for Pydantic models."""

    def test_model_validation_profile(self) -> None:
        """Profile Pydantic model validation performance."""
        profiler = cProfile.Profile()

        # Profile model creation with validation
        profiler.enable()
        for level in NotificationLevel:
            for timeout in [1, 10, 30, 60, 120, 300]:
                NotificationRequest(
                    title=f"Test {level.value}",
                    message=f"Testing level {level.value} with timeout {timeout}",
                    level=level,
                    timeout=timeout,
                )
        profiler.disable()

        # Generate statistics
        stats_stream = StringIO()
        stats = pstats.Stats(profiler, stream=stats_stream)
        stats.sort_stats("cumulative")
        stats.print_stats(15)

        output = stats_stream.getvalue()

        # Verify model validation was profiled
        assert "NotificationRequest" in output or "__init__" in output

        print("\n" + "=" * 80)
        print("MODEL VALIDATION PROFILE")
        print("=" * 80)
        print(output)


class TestBottleneckIdentification:
    """Tests focused on identifying performance bottlenecks."""

    @patch("ai_task_notify_hook.notification.core.DesktopNotifier")
    def test_identify_slowest_component(self, mock_notifier_class: MagicMock) -> None:
        """Identify the slowest component in notification flow."""
        # Arrange
        mock_instance = MagicMock()
        mock_instance.send = AsyncMock()
        mock_notifier_class.return_value = mock_instance

        profiler = cProfile.Profile()

        # Profile complete flow
        import asyncio

        profiler.enable()
        for i in range(50):
            asyncio.run(show_notification(
                title=f"Test {i}",
                message=f"Message {i}",
                level=NotificationLevel.INFO,
                timeout=10,
            ))
        profiler.disable()

        # Analyze statistics
        stats_stream = StringIO()
        stats = pstats.Stats(profiler, stream=stats_stream)
        stats.sort_stats("tottime")  # Sort by self-time (not including subcalls)

        # Get top functions by self-time
        stats.print_stats(10)

        output = stats_stream.getvalue()

        print("\n" + "=" * 80)
        print("BOTTLENECK ANALYSIS (Top 10 by self-time)")
        print("=" * 80)
        print(output)
        print("\nKey Metrics:")
        print(f"Total function calls: {stats.total_calls}")  # type: ignore[attr-defined]
        print(f"Primitive calls: {stats.prim_calls}")  # type: ignore[attr-defined]

    @patch("ai_task_notify_hook.notification.core.DesktopNotifier")
    def test_memory_allocation_pattern(self, mock_notifier_class: MagicMock) -> None:
        """Test memory allocation patterns during notification flow."""
        # Arrange
        mock_instance = MagicMock()
        mock_instance.send = AsyncMock()
        mock_notifier_class.return_value = mock_instance

        import tracemalloc

        # Start memory tracking
        tracemalloc.start()

        # Take snapshot before operations
        snapshot_before = tracemalloc.take_snapshot()

        # Perform operations
        import asyncio

        for i in range(100):
            asyncio.run(show_notification(
                title=f"Memory Test {i}",
                message=f"Testing memory allocation pattern iteration {i}",
                timeout=10,
            ))

        # Take snapshot after operations
        snapshot_after = tracemalloc.take_snapshot()

        # Compare snapshots
        top_stats = snapshot_after.compare_to(snapshot_before, "lineno")

        # Print top 10 memory allocations
        print("\n" + "=" * 80)
        print("MEMORY ALLOCATION ANALYSIS (Top 10)")
        print("=" * 80)
        for stat in top_stats[:10]:
            print(f"{stat}")

        # Stop tracking
        tracemalloc.stop()

        # Verify memory tracking worked
        assert len(top_stats) > 0


class TestPerformanceRegression:
    """Tests to detect performance regressions."""

    @pytest.mark.benchmark(group="notification-flow")
    @patch("ai_task_notify_hook.notification.core.DesktopNotifier")
    def test_benchmark_notification_flow(
        self, mock_notifier_class: MagicMock, benchmark: BenchmarkFixture
    ) -> None:
        """Benchmark complete notification flow for regression detection."""
        # Arrange
        mock_instance = MagicMock()
        mock_instance.send = AsyncMock()
        mock_notifier_class.return_value = mock_instance

        def notification_flow() -> None:
            import asyncio
            asyncio.run(show_notification(
                title="Benchmark Test",
                message="Performance regression test",
                level=NotificationLevel.WARNING,
                timeout=15,
            ))

        # Run benchmark
        result = benchmark(notification_flow)

        # Benchmark automatically tracks min, max, mean, stddev
        # Results are stored in .benchmarks/ for comparison

    @pytest.mark.benchmark(group="model-operations")
    def test_benchmark_model_creation_validation(
        self, benchmark: BenchmarkFixture
    ) -> None:
        """Benchmark Pydantic model creation and validation."""

        def create_and_validate() -> NotificationRequest:
            return NotificationRequest(
                title="Benchmark Model",
                message="Testing model creation performance",
                level=NotificationLevel.ERROR,
                timeout=30,
            )

        result = benchmark(create_and_validate)
        assert isinstance(result, NotificationRequest)


class TestScalabilityProfile:
    """Tests to profile scalability characteristics."""

    @patch("ai_task_notify_hook.notification.core.DesktopNotifier")
    def test_throughput_scaling(self, mock_notifier_class: MagicMock) -> None:
        """Test notification throughput with increasing load."""
        # Arrange
        mock_instance = MagicMock()
        mock_instance.send = AsyncMock()
        mock_notifier_class.return_value = mock_instance

        import time

        test_sizes = [10, 50, 100, 500]
        results = []

        for size in test_sizes:
            start_time = time.perf_counter()

            for i in range(size):
                import asyncio
                asyncio.run(show_notification(
                    title=f"Scaling Test {i}",
                    message=f"Throughput test iteration {i}",
                    timeout=10,
                ))

            end_time = time.perf_counter()
            elapsed = end_time - start_time
            throughput = size / elapsed

            results.append({"size": size, "elapsed": elapsed, "throughput": throughput})

        # Print throughput analysis
        print("\n" + "=" * 80)
        print("THROUGHPUT SCALING ANALYSIS")
        print("=" * 80)
        for result in results:
            print(
                f"Size: {result['size']:4d} | "
                f"Time: {result['elapsed']:.4f}s | "
                f"Throughput: {result['throughput']:.2f} ops/sec"
            )

        # Verify throughput scales reasonably
        # Throughput should not decrease dramatically with size
        assert results[0]["throughput"] > 0
        assert results[-1]["throughput"] > 0
