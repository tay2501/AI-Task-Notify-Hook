"""Type checking integration tests using mypy.

This test module verifies that mypy type checking works correctly
for the entire codebase, ensuring type safety and catching potential
type-related bugs at the testing stage.
"""

import subprocess
from pathlib import Path

import pytest


class TestMypyIntegration:
    """Integration tests for mypy type checking."""

    def test_mypy_components(self) -> None:
        """Test mypy type checking for components directory."""
        result = subprocess.run(
            ["uv", "run", "mypy", "components/ai_task_notify_hook"],
            capture_output=True,
            text=True,
            check=False,
        )

        # Mypy should pass without errors
        assert result.returncode == 0, f"Mypy failed with errors:\n{result.stdout}\n{result.stderr}"

    def test_mypy_bases(self) -> None:
        """Test mypy type checking for bases directory."""
        result = subprocess.run(
            ["uv", "run", "mypy", "bases/ai_task_notify_hook"],
            capture_output=True,
            text=True,
            check=False,
        )

        # Mypy should pass without errors
        assert result.returncode == 0, f"Mypy failed with errors:\n{result.stdout}\n{result.stderr}"

    def test_mypy_test_directory(self) -> None:
        """Test mypy type checking for test directory."""
        result = subprocess.run(
            ["uv", "run", "mypy", "test"],
            capture_output=True,
            text=True,
            check=False,
        )

        # Mypy should pass without errors
        assert result.returncode == 0, f"Mypy failed with errors:\n{result.stdout}\n{result.stderr}"

    def test_mypy_strict_mode(self) -> None:
        """Test that mypy runs in strict mode as configured."""
        # Read pyproject.toml to verify strict mode is enabled
        pyproject_path = Path("pyproject.toml")
        assert pyproject_path.exists(), "pyproject.toml not found"

        content = pyproject_path.read_text(encoding="utf-8")
        assert "strict = true" in content, "Mypy strict mode should be enabled in pyproject.toml"


@pytest.mark.slow
class TestMypyFullProject:
    """Full project type checking tests (marked as slow)."""

    def test_mypy_entire_project(self) -> None:
        """Test mypy type checking for entire project.

        This test is marked as slow and can be skipped in fast test runs
        using: pytest -m "not slow"
        """
        result = subprocess.run(
            ["uv", "run", "mypy", "."],
            capture_output=True,
            text=True,
            check=False,
        )

        # Mypy should pass without errors for the entire project
        assert result.returncode == 0, f"Mypy failed with errors:\n{result.stdout}\n{result.stderr}"
