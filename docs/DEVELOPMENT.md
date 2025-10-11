# Development Guide for AI Task Notify Hook

## Overview
This document provides comprehensive guidance for developers working on the AI Task Notify Hook project. It covers architecture principles, coding standards, naming conventions, and development workflows.

**Last Updated**: 2025-01-11
**Project Version**: 1.0.0
**Architecture**: Polylith (Loose Theme)

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Development Environment Setup](#development-environment-setup)
3. [Project Structure](#project-structure)
4. [Naming Conventions](#naming-conventions)
5. [Coding Standards](#coding-standards)
6. [Component Design Principles](#component-design-principles)
7. [Testing Strategy](#testing-strategy)
8. [Common Development Tasks](#common-development-tasks)
9. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

### Polylith Architecture
This project follows the **Polylith Architecture** with the **loose theme**, optimized for Python monorepos.

#### Core Concepts
- **Components**: Reusable business logic building blocks (like LEGO bricks)
- **Bases**: Entry points for different execution contexts (CLI, server, etc.)
- **Projects**: Deployable artifacts combining components and bases
- **Development**: Shared development utilities and tools

#### Architecture Benefits
✅ **Code Reusability**: Components can be shared across multiple projects
✅ **Loose Coupling**: Components have minimal dependencies on each other
✅ **High Cohesion**: Related functionality is grouped together
✅ **Easy Testing**: Each component can be tested independently
✅ **Incremental Development**: Add/modify components without affecting others

### Workspace Structure
```
ai_task_notify_hook/
├── bases/                    # Entry points for different contexts
│   └── ai_task_notify_hook/
│       └── cli/              # Command-line interface base
│           └── core.py       # Main CLI entry point
├── components/               # Reusable business logic
│   └── ai_task_notify_hook/
│       ├── config/           # Configuration loading and validation
│       ├── logging/          # Structured logging setup
│       ├── models/           # Shared data models and enums
│       ├── notification/     # Core notification functionality
│       └── validation/       # Exception hierarchy
├── projects/                 # Deployable applications
│   ├── notify-cli/           # Full-featured CLI with rich output
│   ├── notify-server/        # FastAPI server for remote notifications
│   └── notify-tool/          # Minimal CLI for hook integration
├── development/              # Shared development tools (if any)
├── test/                     # Test files mirroring component structure
└── docs/                     # Documentation
```

---

## Development Environment Setup

### Prerequisites
- **Python**: 3.12 or higher
- **uv**: Modern Python package manager (recommended)
- **Git**: Version control

### Initial Setup
```bash
# Clone repository
git clone https://github.com/tay2501/AI-Task-Notify-Hook.git
cd AI-Task-Notify-Hook

# Install dependencies using uv
uv sync

# Verify installation
uv run poly info
```

### Development Tools
The project uses the following tools:
- **uv**: Fast Python package manager
- **polylith-cli**: Polylith workspace management
- **ruff**: Fast Python linter and formatter
- **mypy**: Static type checker
- **pytest**: Testing framework
- **sphinx**: Documentation generator

---

## Project Structure

### Components Detail

#### 1. **models** Component
**Purpose**: Shared data models and enumerations
**Dependencies**: None (zero-dependency design)
**Exports**:
- `NotificationLevel`: Enum for notification severity (INFO, SUCCESS, WARNING, ERROR)
- `LogLevel`: Enum for logging levels
- `NotificationRequest`: Immutable notification request dataclass

**Design Principles**:
- Frozen dataclasses for immutability
- Full type hints for mypy strict mode
- Validation in `__post_init__` methods
- No external dependencies

#### 2. **validation** Component
**Purpose**: Custom exception hierarchy
**Dependencies**: None
**Exports**:
- `NotificationError`: Base exception class
- `ConfigurationError`: Configuration-related errors
- `ValidationError`: Input validation errors
- `NotificationBackendError`: Platform notification errors

**Design Principles**:
- All exceptions inherit from `NotificationError`
- Exception chaining with `cause` parameter
- Zero validation logic (delegated to Pydantic)

#### 3. **config** Component
**Purpose**: Configuration loading and validation
**Dependencies**: models, validation, pydantic
**Exports**:
- `load_config()`: Load configuration from JSON with EAFP style
- `validate_config_file()`: Validate configuration without loading
- `NotificationConfig`: Pydantic model for notification settings
- `ApplicationConfig`: Pydantic model for application settings

**Design Principles**:
- EAFP style: "Easier to Ask for Forgiveness than Permission"
- Pydantic for validation
- Default configuration if file not found

#### 4. **logging** Component
**Purpose**: Structured logging with structlog
**Dependencies**: structlog
**Exports**:
- `configure_logging()`: Initialize logging system
- `get_logger()`: Get named logger instance

**Design Principles**:
- Structured logging with context
- JSON output for machine processing
- Console-friendly formatting for development

#### 5. **notification** Component
**Purpose**: Core notification functionality
**Dependencies**: models, validation, plyer
**Exports**:
- `show_notification()`: Display notification (simplified interface)
- `StandardNotificationProvider`: Platform notification provider

**Design Principles**:
- Platform abstraction via plyer
- Graceful degradation if backend unavailable
- Error handling with custom exceptions

### Bases Detail

#### **cli** Base
**Purpose**: Command-line interface entry point
**Dependencies**: config, logging, notification, models
**Entry Point**: `main()` function

**Responsibilities**:
- Parse command-line arguments
- Initialize logging
- Load configuration
- Invoke notification component
- Handle errors and exit codes

### Projects Detail

#### 1. **notify-tool**
**Target**: Minimal CLI for Claude Code hooks
**Features**: Basic notification display only
**Dependencies**: Minimal (plyer, pydantic, structlog)

#### 2. **notify-cli**
**Target**: Full-featured command-line tool
**Features**: Rich output, click commands, enhanced UI
**Dependencies**: Additional (click, rich)

#### 3. **notify-server**
**Target**: REST API server for remote notifications
**Features**: FastAPI endpoints, uvicorn server
**Dependencies**: Additional (fastapi, uvicorn)

---

## Naming Conventions

### General Python Conventions (PEP 8)
Following **PEP 8** and **PEP 423** for package naming:

| Element | Convention | Example |
|---------|-----------|---------|
| **Packages/Modules** | lowercase_with_underscores | `ai_task_notify_hook` |
| **Functions** | lowercase_with_underscores | `load_config`, `show_notification` |
| **Variables** | lowercase_with_underscores | `config_path`, `timeout_value` |
| **Constants** | UPPER_CASE_WITH_UNDERSCORES | `DEFAULT_TIMEOUT`, `MAX_RETRIES` |
| **Classes** | PascalCase | `NotificationConfig`, `StandardNotificationProvider` |
| **Private Functions** | _leading_underscore | `_internal_helper` |
| **Private Attributes** | _leading_underscore | `self._cache` |

### Polylith-Specific Conventions

#### Workspace Naming
- **Namespace**: `ai_task_notify_hook` (single top namespace)
- Follows PEP 423: lowercase with underscores
- Consistent across all bricks

#### Component Naming
- Use **descriptive, single-word names** when possible: `config`, `models`, `logging`
- Multi-word: Use underscores: `notification_handler` (if needed)
- Avoid generic names: ❌ `utils`, ❌ `helpers`

#### Base Naming
- Describe the entry point context: `cli`, `server`, `api`
- Keep simple: bases are entry points, not business logic

#### Project Naming
- Use **kebab-case**: `notify-tool`, `notify-cli`, `notify-server`
- Descriptive of deployment target

### File Naming
- **Python files**: `lowercase_with_underscores.py`
- **Test files**: `test_<module_name>.py` or `<module_name>_test.py`
- **Config files**: Descriptive names: `config.json`, `logging_config.yaml`

---

## Coding Standards

### Python Version
- **Minimum**: Python 3.12
- Use modern Python features (match statements, type hints with `|`, etc.)

### Type Hints
- **Required**: All functions must have complete type hints
- **Strict mode**: Code must pass `mypy --strict`
- Use `from __future__ import annotations` for forward references

```python
def load_config(config_path: str | Path | None = None) -> ApplicationConfig:
    """Load configuration from JSON file."""
    ...
```

### Error Handling Style
- **EAFP**: "Easier to Ask for Forgiveness than Permission"
- Use try/except blocks instead of checking conditions first

✅ **Good (EAFP)**:
```python
try:
    with config_path.open(encoding="utf-8") as f:
        data = json.load(f)
except (json.JSONDecodeError, OSError) as exc:
    raise ConfigurationError(f"Failed to load config: {exc}") from exc
```

❌ **Avoid (LBYL - Look Before You Leap)**:
```python
if not config_path.exists():
    raise ConfigurationError("File not found")
if not config_path.is_file():
    raise ConfigurationError("Not a file")
# ... more checks before attempting to read
```

### Code Formatting
- **Tool**: Ruff (replaces Black, isort, Flake8)
- **Line Length**: 99 characters
- **Quotes**: Double quotes (`"`) for strings and docstrings
- **Indentation**: 4 spaces

```bash
# Format code
uv run ruff format .

# Check and fix linting issues
uv run ruff check --fix .
```

### Import Organization
Ruff automatically organizes imports following this order:
1. Future imports
2. Standard library
3. Third-party packages
4. First-party (ai_task_notify_hook)
5. Local folder

```python
from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field

from ai_task_notify_hook.models import NotificationLevel
from ai_task_notify_hook.validation import ConfigurationError
```

### Docstrings
- **Style**: Google-style docstrings
- **Required**: All public functions, classes, and modules
- Include parameter types, return types, and exceptions

```python
def show_notification(
    title: str,
    message: str,
    level: NotificationLevel = NotificationLevel.INFO,
    timeout: int = 10,
) -> None:
    """Display notification with simplified interface.

    Args:
        title: Notification title
        message: Notification message body
        level: Notification severity level
        timeout: Notification timeout in seconds

    Raises:
        NotificationBackendError: If notification backend is unavailable
        NotificationError: If notification fails to send

    Examples:
        >>> show_notification("Build Complete", "All tests passed")
        >>> show_notification("Error", "Build failed", level=NotificationLevel.ERROR)
    """
    ...
```

### Comments
- **Language**: English only
- Use comments to explain **why**, not **what**
- Code should be self-documenting for the "what"

✅ **Good**:
```python
# Return default configuration if file doesn't exist
# (allows running without configuration file)
if not config_path.exists():
    return ApplicationConfig()
```

❌ **Avoid**:
```python
# Check if path exists
if not config_path.exists():
    # Return default config
    return ApplicationConfig()
```

---

## Component Design Principles

### 1. Single Responsibility Principle
Each component should have **one clear purpose**.

✅ Good: `config` component handles configuration loading
❌ Bad: `config` component also handles logging setup

### 2. Dependency Direction
- **models** → No dependencies (foundation)
- **validation** → No dependencies (exceptions only)
- **config** → Depends on models, validation
- **notification** → Depends on models, validation
- **bases** → Depend on necessary components

### 3. Zero-Dependency Core
The `models` and `validation` components should **never** import from other components.

### 4. Immutability by Default
- Use frozen dataclasses: `@dataclass(frozen=True)`
- Use Pydantic with `frozen=True`
- Avoid mutable default arguments

### 5. Loose Coupling, High Cohesion
- Components should be independently testable
- Related functionality stays together
- Minimal inter-component communication

---

## Testing Strategy

### Test Structure
Tests mirror the component structure:
```
test/
├── bases/
│   └── ai_task_notify_hook/
│       └── cli/
│           └── test_cli.py
├── components/
│   └── ai_task_notify_hook/
│       ├── config/
│       │   └── test_loader.py
│       ├── models/
│       │   └── test_core.py
│       └── notification/
│           └── test_notification.py
└── conftest.py
```

### Running Tests
```bash
# Run all tests with coverage
uv run pytest

# Run specific test file
uv run pytest test/components/ai_task_notify_hook/config/test_loader.py

# Run with verbose output
uv run pytest -v

# Skip slow tests
uv run pytest -m "not performance"
```

### Test Conventions
- **File naming**: `test_<module>.py` or `<module>_test.py`
- **Function naming**: `test_<functionality>()`
- **Class naming**: `Test<Functionality>`

### Test Categories
- **Unit tests**: Test individual functions/classes
- **Integration tests**: Test component interactions
- **Performance tests**: Marked with `@pytest.mark.performance`
- **Benchmark tests**: Use `pytest-benchmark`

---

## Common Development Tasks

### Creating a New Component
```bash
# Create component structure
uv run poly create component --name my_component

# This creates:
# - components/ai_task_notify_hook/my_component/
# - components/ai_task_notify_hook/my_component/__init__.py
# - components/ai_task_notify_hook/my_component/core.py
```

### Creating a New Base
```bash
# Create base structure
uv run poly create base --name my_base

# This creates:
# - bases/ai_task_notify_hook/my_base/
# - bases/ai_task_notify_hook/my_base/__init__.py
# - bases/ai_task_notify_hook/my_base/core.py
```

### Creating a New Project
```bash
# Create project structure
uv run poly create project --name my-project

# This creates:
# - projects/my-project/
# - projects/my-project/pyproject.toml
```

### Adding Dependencies
```bash
# Add production dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Sync environment after changes
uv sync
```

### Code Quality Checks
```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Auto-fix linting issues
uv run ruff check --fix .

# Type check
uv run mypy components bases

# Run all checks
make check  # If Makefile is configured
```

### Building Documentation
```bash
# Build Sphinx documentation
cd docs
uv run sphinx-build -b html source build

# Or use make (if available)
make html
```

---

## Troubleshooting

### Common Issues

#### Import Errors
**Problem**: `ModuleNotFoundError: No module named 'ai_task_notify_hook'`

**Solution**:
```bash
# Ensure virtual environment is activated
uv sync

# Verify project structure
uv run poly info
```

#### Ruff Errors
**Problem**: Import order violations

**Solution**:
```bash
# Auto-fix import issues
uv run ruff check --fix .
```

#### Type Checking Errors
**Problem**: mypy reports type errors

**Solution**:
1. Add type hints to all functions
2. Check `pyproject.toml` for mypy overrides
3. Use `# type: ignore` only as last resort

#### Polylith Structure Issues
**Problem**: Components not recognized

**Solution**:
1. Check `workspace.toml` configuration
2. Ensure `pyproject.toml` has correct `[tool.hatch.build]` settings
3. Run `uv sync` to refresh environment

---

## Best Practices Summary

### Do ✅
- Use type hints everywhere
- Follow EAFP error handling
- Write docstrings for all public APIs
- Keep components loosely coupled
- Test each component independently
- Use Ruff for formatting and linting
- Commit formatted code

### Don't ❌
- Don't create circular dependencies between components
- Don't add unnecessary dependencies to core components (models, validation)
- Don't use `# type: ignore` without a good reason
- Don't commit unformatted code
- Don't bypass validation in Pydantic models
- Don't use mutable default arguments

---

## Additional Resources

### Official Documentation
- [Polylith Documentation](https://polylith.gitbook.io/polylith)
- [Python Polylith Docs](https://davidvujic.github.io/python-polylith-docs/)
- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

### Project-Specific Docs
- [README.md](../README.md) - Project overview
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines (if exists)
- [Component READMEs](../components/) - Individual component documentation

---

## Questions?

If you encounter issues not covered in this guide:
1. Check existing GitHub issues
2. Review component-specific README files
3. Consult the Polylith documentation
4. Ask in project discussions

**Happy coding! 🚀**
