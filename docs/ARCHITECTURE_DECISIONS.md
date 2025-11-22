# Architecture Decision Record (ADR)

**Project**: AI Task Notify Hook
**Last Updated**: 2025-01-11
**Architecture**: Polylith (Loose Theme)

---

## Table of Contents

1. [Core Architecture Decisions](#core-architecture-decisions)
2. [Component Design Principles](#component-design-principles)
3. [Naming Conventions](#naming-conventions)
4. [Development Guidelines](#development-guidelines)
5. [Future Considerations](#future-considerations)

---

## Core Architecture Decisions

### ADR-001: Polylith Architecture with Loose Theme

**Status**: ✅ Accepted
**Date**: 2025-01-11

**Context**:
We need a maintainable, testable architecture that supports multiple deployment targets (CLI, server, minimal tool) while maximizing code reuse.

**Decision**:
Adopt Polylith Architecture with the **loose theme** (Python-specific variation).

**Rationale**:
- **Code Reusability**: Components are reusable building blocks from day one
- **Loose Coupling**: Each component has minimal dependencies
- **High Cohesion**: Related functionality is grouped together
- **Easy Testing**: Components can be tested independently
- **Scalability**: New projects can be added without affecting existing ones

**Structure**:
```
ai_task_notify_hook/
├── bases/                    # Entry points
│   └── ai_task_notify_hook/
│       └── cli/              # Command-line interface base
├── components/               # Reusable business logic
│   └── ai_task_notify_hook/
│       ├── config/           # Configuration management
│       ├── logging/          # Structured logging
│       ├── models/           # Shared data models
│       ├── notification/     # Core notification logic
│       └── validation/       # Exception hierarchy
├── projects/                 # Deployable artifacts
│   ├── notify-cli/           # Full-featured CLI
│   ├── notify-server/        # FastAPI server
│   └── notify-tool/          # Minimal hook tool
└── test/                     # Test files mirroring structure
```

**Consequences**:
- ✅ Clear separation of concerns
- ✅ Easy to add new deployment targets
- ✅ Components are independently testable
- ⚠️ Slightly more complex initial setup
- ⚠️ Requires understanding of Polylith concepts

---

### ADR-002: Single Top-Level Namespace

**Status**: ✅ Accepted
**Date**: 2025-01-11

**Context**:
Polylith requires a consistent namespace across all components for proper module resolution.

**Decision**:
Use `ai_task_notify_hook` as the single top-level namespace for all components, bases, and projects.

**Rationale**:
- **Simplicity**: One namespace is easier to understand and manage
- **Polylith Compliance**: Follows Polylith loose theme best practices
- **Import Clarity**: All imports start with the same namespace
- **No Conflicts**: Avoids naming conflicts between components

**Example**:
```python
from ai_task_notify_hook.models import NotificationLevel
from ai_task_notify_hook.logging import configure_logging
from ai_task_notify_hook.notification import show_notification
```

**Consequences**:
- ✅ Clear, consistent import paths
- ✅ Easy to trace dependencies
- ✅ No namespace pollution
- ⚠️ Longer import paths (acceptable trade-off)

---

### ADR-003: Component File Organization

**Status**: ✅ Accepted (with flexibility)
**Date**: 2025-01-11

**Context**:
Polylith best practice suggests using `core.py` for all component implementations, but we need flexibility for larger components.

**Decision**:
- **Preferred**: Use `core.py` for single-file components
- **Allowed**: Use descriptive names (`loader.py`, `exceptions.py`) for multi-concern components
- **Required**: Always provide `__init__.py` with clear public API exports

**Current Structure**:
```
components/ai_task_notify_hook/
├── config/
│   ├── loader.py          # Configuration loading logic
│   ├── models.py          # Pydantic configuration models
│   └── __init__.py        # Exports: load_config, validate_config_file
├── logging/
│   ├── core.py            # Logging configuration
│   └── __init__.py        # Exports: configure_logging, get_logger
├── models/
│   ├── core.py            # Data models and enums
│   └── __init__.py        # Exports: NotificationLevel, LogLevel, NotificationRequest
├── notification/
│   ├── core.py            # Notification display logic
│   └── __init__.py        # Exports: show_notification, StandardNotificationProvider
└── validation/
    ├── exceptions.py      # Exception hierarchy
    └── __init__.py        # Exports: all exception classes
```

**Rationale**:
- **Flexibility**: Allows components to grow naturally
- **Clarity**: Descriptive file names aid understanding
- **Maintainability**: Related code stays together
- **API Control**: `__init__.py` enforces clean public interfaces

**Consequences**:
- ✅ More readable for Python developers
- ✅ Components can scale without restructuring
- ⚠️ Slight deviation from strict Polylith convention
- ⚠️ Developers must maintain clear `__init__.py` exports

---

## Component Design Principles

### ADR-004: Zero-Dependency Core Components

**Status**: ✅ Accepted
**Date**: 2025-01-11

**Context**:
Some components should be foundational with no external dependencies.

**Decision**:
The `models` and `validation` components have **zero dependencies** on other components.

**Dependency Graph**:
```
models (no dependencies)
  ↑
  |
validation (no dependencies)
  ↑
  |
config, logging, notification (depend on models, validation)
  ↑
  |
bases (depend on necessary components)
```

**Rationale**:
- **Stability**: Core components rarely change
- **Reusability**: Can be used anywhere without pulling in dependencies
- **Testing**: Easier to test in isolation
- **Performance**: Faster imports

**Consequences**:
- ✅ Clear dependency direction (no cycles)
- ✅ Core components are highly reusable
- ⚠️ Developers must avoid adding dependencies to core components

---

### ADR-005: EAFP Error Handling Style

**Status**: ✅ Accepted
**Date**: 2025-01-11

**Context**:
Python supports two error handling philosophies: LBYL (Look Before You Leap) and EAFP (Easier to Ask for Forgiveness than Permission).

**Decision**:
Use **EAFP style** throughout the codebase.

**Example (Good - EAFP)**:
```python
def load_config(config_path: Path) -> ApplicationConfig:
    try:
        with config_path.open(encoding="utf-8") as f:
            data = json.load(f)
        return ApplicationConfig.model_validate(data)
    except (json.JSONDecodeError, ValueError) as exc:
        raise ConfigurationError(f"Failed to load config: {exc}") from exc
```

**Example (Avoid - LBYL)**:
```python
def load_config(config_path: Path) -> ApplicationConfig:
    if not config_path.exists():
        raise ConfigurationError("File not found")
    if not config_path.is_file():
        raise ConfigurationError("Not a file")
    # ... more checks before attempting operation
```

**Rationale**:
- **Pythonic**: EAFP is the idiomatic Python style
- **Race Conditions**: Avoids TOCTOU (Time-Of-Check-Time-Of-Use) bugs
- **Performance**: Faster in the common (success) case
- **Simplicity**: Less boilerplate code

**Consequences**:
- ✅ More Pythonic code
- ✅ Better error messages (actual errors from operations)
- ⚠️ Requires proper exception handling
- ⚠️ All developers must understand EAFP philosophy

---

### ADR-006: Immutability by Default

**Status**: ✅ Accepted
**Date**: 2025-01-11

**Context**:
Mutable data structures can lead to bugs, especially in concurrent environments.

**Decision**:
Use **immutable data structures** by default:
- Frozen dataclasses: `@dataclass(frozen=True)`
- Frozen Pydantic models: `model_config = ConfigDict(frozen=True)`
- Tuple over list for fixed collections

**Example**:
```python
@dataclass(frozen=True)
class NotificationRequest:
    title: str
    message: str
    level: NotificationLevel = NotificationLevel.INFO
    timeout: int = 10
```

**Rationale**:
- **Thread Safety**: Immutable objects are inherently thread-safe
- **Predictability**: State cannot change unexpectedly
- **Hashing**: Immutable objects can be used as dict keys
- **Debugging**: Easier to reason about data flow

**Consequences**:
- ✅ Fewer bugs related to unexpected mutations
- ✅ Can use dataclasses as dict keys
- ⚠️ Requires creating new objects for changes
- ⚠️ May use more memory (acceptable trade-off)

---

## Naming Conventions

### ADR-007: PEP 8 Compliance with Python 3.12+ Features

**Status**: ✅ Accepted
**Date**: 2025-01-11

**Context**:
Python 3.12+ introduces new features that should be leveraged for better code.

**Decision**:
Follow PEP 8 strictly, using Python 3.12+ features:

| Element | Convention | Example |
|---------|-----------|---------|
| **Modules** | `lowercase_with_underscores` | `config_loader.py` |
| **Functions** | `lowercase_with_underscores` | `load_config()`, `show_notification()` |
| **Variables** | `lowercase_with_underscores` | `config_path`, `timeout_value` |
| **Constants** | `UPPER_CASE_WITH_UNDERSCORES` | `DEFAULT_TIMEOUT`, `MAX_RETRIES` |
| **Classes** | `PascalCase` | `NotificationConfig`, `StandardNotificationProvider` |
| **Type Unions** | Use `|` operator | `str | Path | None` |
| **Type Aliases** | `PascalCase` | `ConfigPath = str | Path` |

**Modern Type Hints (Python 3.12+)**:
```python
# Old style (pre-3.10)
from typing import Union, Optional
def load_config(path: Optional[Union[str, Path]] = None) -> ApplicationConfig:
    ...

# Modern style (Python 3.12+)
def load_config(path: str | Path | None = None) -> ApplicationConfig:
    ...
```

**Consequences**:
- ✅ Clean, modern Python code
- ✅ Better IDE support
- ✅ Easier to read and maintain
- ⚠️ Requires Python 3.12+ (acceptable requirement)

---

### ADR-008: Component Naming Guidelines

**Status**: ✅ Accepted (with future consideration)
**Date**: 2025-01-11

**Context**:
Component names should be descriptive yet avoid conflicts with Python builtins.

**Decision**:
**Current State** (acceptable):
- `config`: Configuration management ✅
- `logging`: Structured logging ⚠️ (name conflicts with Python builtin)
- `models`: Shared data models ✅
- `notification`: Notification display ✅
- `validation`: Exception hierarchy ✅

**Future Consideration**:
If `logging` causes import conflicts, rename to:
- **Option 1**: `log_config` (logging configuration)
- **Option 2**: `structured_logging` (more descriptive)
- **Option 3**: `app_logging` (application logging)

**Current Mitigation**:
- Always use full import paths: `from ai_task_notify_hook.logging import configure_logging`
- Never use `from logging import ...` for the Python builtin in the same file

**Rationale**:
- **Pragmatism**: Current naming works in practice
- **Clarity**: `logging` accurately describes the component
- **Flexibility**: Easy to rename if conflicts arise
- **No Rush**: Only change if actual problems occur

**Consequences**:
- ✅ Clear, descriptive component names
- ⚠️ Potential for confusion with Python builtin
- ⚠️ Developers must be careful with imports

---

## Development Guidelines

### ADR-009: Testing Strategy

**Status**: ✅ Accepted
**Date**: 2025-01-11

**Context**:
Tests should mirror the component structure for clarity.

**Decision**:
- **Structure**: Test files mirror `components/` and `bases/` structure
- **Naming**: `test_<module>.py` or `<module>_test.py`
- **Coverage**: Minimum 80% code coverage (enforced by pytest-cov)
- **Markers**: Use pytest markers for test categorization

**Test Structure**:
```
test/
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

**Pytest Configuration** (in `workspace.toml`):
```toml
[tool.pytest.ini_options]
testpaths = ["test"]
addopts = [
    "--cov=ai_task_notify_hook",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-fail-under=80",
]
markers = [
    "performance: marks tests as performance tests",
    "benchmark: marks tests as benchmark tests",
]
```

**Consequences**:
- ✅ Clear test organization
- ✅ High code coverage enforced
- ✅ Easy to find tests for specific components
- ⚠️ Developers must write tests for new code

---

### ADR-010: Code Quality Tools

**Status**: ✅ Accepted
**Date**: 2025-01-11

**Context**:
Consistent code quality requires automated tooling.

**Decision**:
Use the following tools (all configured in `pyproject.toml`):
- **Ruff 0.13.2+**: Linting and formatting (replaces flake8, black, isort, pylint)
- **mypy**: Static type checking (strict mode)
- **pytest**: Testing framework with coverage
- **uv**: Fast Python package manager

**Configuration Philosophy**:
- **Single Source of Truth**: All configuration in `pyproject.toml`
- **Strict by Default**: Enable strict checks, selectively disable as needed
- **Preview Features**: Enable Ruff preview mode for latest improvements

**Daily Workflow**:
```bash
# Lint and auto-fix
uv run ruff check --fix .

# Format code
uv run ruff format .

# Type check
uv run mypy src/ai_task_notify_hook

# Run tests
uv run pytest

# All checks together
uv run ruff check --fix . && uv run ruff format . && uv run mypy src/ai_task_notify_hook
```

**Consequences**:
- ✅ Consistent code style across team
- ✅ Catch bugs early with type checking
- ✅ Fast feedback loop with Ruff
- ⚠️ Developers must run checks before committing

---

### ADR-011: Documentation Standards

**Status**: ✅ Accepted
**Date**: 2025-01-11

**Context**:
Good documentation is critical for maintainability and onboarding.

**Decision**:
- **Docstring Style**: Google-style docstrings
- **Documentation Tool**: Sphinx with MyST parser
- **API Documentation**: Auto-generated from docstrings
- **Component READMEs**: Optional for complex components

**Docstring Example**:
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
```

**Documentation Structure**:
```
docs/
├── source/
│   ├── api/                    # Auto-generated API docs
│   ├── development/            # Development guides
│   ├── index.rst               # Main documentation page
│   ├── installation.rst        # Installation guide
│   ├── usage.rst               # Usage examples
│   └── conf.py                 # Sphinx configuration
├── ARCHITECTURE_DECISIONS.md  # This file
├── CONTRIBUTING.md             # Contribution guidelines
└── DEVELOPMENT.md              # Development guide
```

**Consequences**:
- ✅ Consistent documentation style
- ✅ Easy to generate API docs
- ✅ Better onboarding experience
- ⚠️ Developers must write good docstrings

---

## Future Considerations

### Potential Future Changes

#### 1. Component Renaming
**If needed**, consider these renames to avoid builtin conflicts:
- `logging` → `log_config` or `structured_logging`

**Trigger**: Import conflicts or confusion with Python builtin

**Impact**: Medium (requires updating all imports)

**Decision Date**: TBD

---

#### 2. Multi-File Components
**If components grow large**, consider splitting into multiple files:
```
components/ai_task_notify_hook/notification/
├── core.py           # Main notification logic
├── providers.py      # Notification providers
├── formatters.py     # Message formatters
└── __init__.py       # Public API
```

**Trigger**: Any component exceeds 500 lines

**Impact**: Low (internal refactoring only)

**Decision Date**: TBD

---

#### 3. New Project Types
**Future deployment targets** to consider:
- `notify-webhook`: Webhook receiver for remote notifications
- `notify-desktop`: Electron-based desktop app
- `notify-lib`: Standalone library for external use

**Trigger**: User demand or specific use cases

**Impact**: Low (Polylith makes this easy)

**Decision Date**: TBD

---

## Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-01-11 | 1.0.0 | Initial ADR document | AI Assistant |

---

## Questions or Suggestions?

This document is a living record of architectural decisions. If you have questions or suggestions for improvement:

1. Open a GitHub Discussion
2. Create an issue with the `documentation` label
3. Submit a pull request with your proposed changes

**Remember**: The goal of these decisions is to maintain a **simple, maintainable, and scalable** codebase. When in doubt, favor simplicity.
