# Architecture Documentation

## AI Task Notify Hook - Polylith Architecture

**Version**: 1.0.0
**Last Updated**: 2025-01-11
**Architecture Pattern**: Polylith (Loose Theme)

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [Component Catalog](#component-catalog)
4. [Dependency Graph](#dependency-graph)
5. [Data Flow](#data-flow)
6. [Design Decisions](#design-decisions)
7. [Future Extensions](#future-extensions)

---

## Executive Summary

### What is This Project?
A lightweight, modular notification system designed for Claude Code hooks and automation workflows. Built using Polylith architecture for maximum reusability and maintainability.

### Key Features
- ✅ **Simple**: Minimal API surface, easy to integrate
- ✅ **Fast**: Lightweight startup, minimal dependencies
- ✅ **Modular**: Polylith architecture enables component reuse
- ✅ **Type-Safe**: Full mypy strict mode compliance
- ✅ **Extensible**: Easy to add new notification backends or entry points

### Technology Stack
| Layer | Technology |
|-------|-----------|
| **Language** | Python 3.12+ |
| **Architecture** | Polylith (Loose Theme) |
| **Package Manager** | uv |
| **Validation** | Pydantic 2.11+ |
| **Logging** | structlog 25.4+ |
| **Notifications** | plyer 2.1+ |
| **Type Checking** | mypy (strict mode) |
| **Linting** | Ruff 0.8+ |
| **Testing** | pytest 8.0+ |

---

## Architecture Overview

### Polylith Concepts

#### What is Polylith?
Polylith is a software architecture that applies functional thinking at the system scale. It treats code as LEGO-like building blocks that can be composed into different applications.

#### Key Terminology
- **Brick**: Generic term for a building block (component or base)
- **Component**: Reusable business logic (the "LEGO bricks")
- **Base**: Entry point for a specific context (CLI, server, etc.)
- **Project**: Deployable artifact combining components and bases
- **Workspace**: The monorepo containing all bricks

### Workspace Structure
```
ai_task_notify_hook/           # Root workspace
├── bases/                     # Entry points
│   └── ai_task_notify_hook/
│       └── cli/               # Command-line interface base
├── components/                # Reusable components
│   └── ai_task_notify_hook/
│       ├── config/            # Configuration management
│       ├── logging/           # Structured logging
│       ├── models/            # Data models and enums
│       ├── notification/      # Core notification logic
│       └── validation/        # Exception hierarchy
├── projects/                  # Deployable applications
│   ├── notify-cli/            # Rich CLI application
│   ├── notify-server/         # REST API server
│   └── notify-tool/           # Minimal CLI for hooks
├── development/               # Shared dev utilities
├── test/                      # Test suite (mirrors structure)
└── docs/                      # Documentation
```

### Architecture Principles

#### 1. **Separation of Concerns**
Each component has a single, well-defined responsibility:
- `models`: Data structures only
- `validation`: Exception definitions only
- `config`: Configuration loading only
- `notification`: Notification display only
- `logging`: Logging setup only

#### 2. **Dependency Inversion**
- High-level components don't depend on low-level details
- Dependencies flow inward toward stable core (models)
- Easy to swap implementations (e.g., different notification backends)

#### 3. **Loose Coupling**
- Components interact through well-defined interfaces
- Minimal knowledge of other components' internals
- Changes in one component rarely affect others

#### 4. **High Cohesion**
- Related functionality stays together in the same component
- Each component is a complete, self-contained unit
- Easy to understand and test in isolation

---

## Component Catalog

### Foundation Layer (Zero Dependencies)

#### **models** Component
```
Purpose: Shared data models and enumerations
Type: Pure data component
Dependencies: None
Exports:
  - NotificationLevel (Enum)
  - LogLevel (Enum)
  - NotificationRequest (frozen dataclass)
```

**Design Notes**:
- Immutable by design (frozen dataclasses)
- No business logic, pure data structures
- Foundation for all other components
- Can never import from other components

**File Structure**:
```
components/ai_task_notify_hook/models/
├── __init__.py         # Public interface
├── core.py             # Model definitions
├── py.typed            # Type hint marker
└── README.md           # Component documentation
```

#### **validation** Component
```
Purpose: Exception hierarchy for error handling
Type: Pure exception component
Dependencies: None
Exports:
  - NotificationError (base exception)
  - ConfigurationError
  - ValidationError
  - NotificationBackendError
```

**Design Notes**:
- All exceptions inherit from `NotificationError`
- Support exception chaining with `cause` parameter
- No validation logic (delegated to Pydantic)
- Can never import from other components

**File Structure**:
```
components/ai_task_notify_hook/validation/
├── __init__.py         # Public interface
├── exceptions.py       # Exception definitions
└── README.md           # Component documentation
```

### Business Logic Layer

#### **config** Component
```
Purpose: Configuration loading and validation
Type: Infrastructure component
Dependencies: models, validation, pydantic
Exports:
  - load_config() -> ApplicationConfig
  - validate_config_file() -> bool
  - NotificationConfig (Pydantic model)
  - ApplicationConfig (Pydantic model)
```

**Design Notes**:
- EAFP style error handling
- Returns default config if file not found
- Pydantic for validation and type safety
- JSON configuration format

**File Structure**:
```
components/ai_task_notify_hook/config/
├── __init__.py         # Public interface
├── loader.py           # Configuration loading logic
└── models.py           # Pydantic models
```

**Configuration Schema**:
```json
{
  "app_name": "Claude Code",
  "version": "1.0.0",
  "notification": {
    "timeout": 10
  }
}
```

#### **logging** Component
```
Purpose: Structured logging setup with structlog
Type: Infrastructure component
Dependencies: structlog
Exports:
  - configure_logging() -> None
  - get_logger(name: str) -> BoundLogger
```

**Design Notes**:
- Structured logging for machine parsing
- Context-aware logging (adds metadata)
- JSON output for production
- Human-friendly console output for development

**File Structure**:
```
components/ai_task_notify_hook/logging/
├── __init__.py         # Public interface
└── core.py             # Logging configuration
```

#### **notification** Component
```
Purpose: Core notification display functionality
Type: Business logic component
Dependencies: models, validation, plyer
Exports:
  - show_notification() -> None
  - StandardNotificationProvider (class)
```

**Design Notes**:
- Platform abstraction via plyer library
- Graceful degradation if backend unavailable
- Notification level support (INFO, SUCCESS, WARNING, ERROR)
- Timeout configuration per notification

**File Structure**:
```
components/ai_task_notify_hook/notification/
├── __init__.py         # Public interface
└── core.py             # Notification logic
```

### Entry Points (Bases)

#### **cli** Base
```
Purpose: Command-line interface entry point
Type: Application base
Dependencies: config, logging, notification, models, argparse
Entry Point: main() -> None
```

**Design Notes**:
- Minimal base focused on argument parsing and orchestration
- No business logic (delegates to components)
- Error handling and exit codes
- Help text and examples

**File Structure**:
```
bases/ai_task_notify_hook/cli/
├── __init__.py         # Public interface
└── core.py             # CLI implementation
```

**Command Signature**:
```bash
notify TITLE MESSAGE [--timeout SECONDS]
```

### Projects (Deployable Artifacts)

#### **notify-tool** Project
```
Target: Minimal CLI for Claude Code hooks
Goal: Fast startup, minimal dependencies
Components Used:
  - models
  - validation
  - config
  - logging
  - notification
Base Used:
  - cli
```

**Use Case**: Claude Code integration, automation scripts

#### **notify-cli** Project
```
Target: Full-featured command-line application
Goal: Rich UI, enhanced user experience
Components Used:
  - All from notify-tool
Additional Dependencies:
  - click (better CLI framework)
  - rich (terminal formatting)
Base Used:
  - cli_enhanced (hypothetical)
```

**Use Case**: Interactive use, development

#### **notify-server** Project
```
Target: REST API server for remote notifications
Goal: Network-accessible notification service
Components Used:
  - All core components
Additional Dependencies:
  - fastapi (web framework)
  - uvicorn (ASGI server)
Base Used:
  - server (hypothetical)
```

**Use Case**: Distributed systems, microservices

---

## Dependency Graph

### Component Dependencies

```
         ┌──────────┐
         │  models  │  (Foundation: No dependencies)
         └────┬─────┘
              │
         ┌────▼────────┐
         │ validation  │  (Foundation: No dependencies)
         └────┬────────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌───▼────┐      ┌───────▼─────┐
│ config │      │ notification │
└───┬────┘      └───────┬──────┘
    │                   │
    │           ┌───────▼──────┐
    │           │   logging    │
    │           └───────┬──────┘
    │                   │
    └───────┬───────────┘
            │
      ┌─────▼─────┐
      │    cli    │  (Base)
      └───────────┘
```

### Dependency Rules
1. **Foundation components** (`models`, `validation`) → No dependencies
2. **Infrastructure components** (`config`, `logging`) → Depend on foundation
3. **Business logic** (`notification`) → Depends on foundation + infrastructure
4. **Bases** (`cli`) → Depend on necessary components
5. **Projects** → Compose components + bases

### Anti-Patterns to Avoid
❌ Circular dependencies between components
❌ Components depending on bases
❌ Foundation components importing from business logic
❌ Bases containing business logic

---

## Data Flow

### CLI Execution Flow
```
1. User executes command
   ↓
2. cli base: Parse arguments
   ↓
3. logging component: Initialize logging
   ↓
4. config component: Load configuration
   ↓
5. notification component: Display notification
   ↓
6. Exit with appropriate code
```

### Configuration Loading Flow
```
1. config.load_config(path?)
   ↓
2. Check if file exists
   ├─ No → Return ApplicationConfig() (defaults)
   └─ Yes → Continue
   ↓
3. Open file with UTF-8 encoding
   ├─ OSError → ConfigurationError
   └─ Success → Continue
   ↓
4. Parse JSON
   ├─ JSONDecodeError → ConfigurationError
   └─ Success → Continue
   ↓
5. Validate with Pydantic
   ├─ ValidationError → ConfigurationError
   └─ Success → Return ApplicationConfig
```

### Notification Display Flow
```
1. show_notification(title, message, level, timeout)
   ↓
2. Create NotificationRequest
   ├─ Validation fails → ValueError
   └─ Success → Continue
   ↓
3. StandardNotificationProvider.send()
   ↓
4. Try to use plyer notification
   ├─ Backend unavailable → NotificationBackendError
   ├─ Send fails → NotificationError
   └─ Success → Return
```

---

## Design Decisions

### Why Polylith?
**Decision**: Use Polylith architecture

**Rationale**:
- Enables true code reuse across multiple projects
- Easy to test components in isolation
- Incremental development without breaking existing code
- Future-proof: can add projects without touching components

**Alternatives Considered**:
- Monolithic structure: Limited reusability
- Traditional packages: Too much overhead for internal code

### Why EAFP Style?
**Decision**: Use "Easier to Ask for Forgiveness than Permission" error handling

**Rationale**:
- More Pythonic (PEP 20: "It's easier to ask forgiveness than permission")
- Better performance (no redundant checks)
- Clearer error messages
- Handles edge cases naturally

**Example**:
```python
# EAFP (chosen)
try:
    return json.load(f)
except JSONDecodeError as e:
    raise ConfigurationError(...) from e

# vs LBYL (avoided)
if not is_valid_json(f):
    raise ConfigurationError(...)
return json.load(f)  # Still might fail!
```

### Why Frozen Dataclasses?
**Decision**: Use frozen dataclasses and Pydantic with `frozen=True`

**Rationale**:
- Immutability prevents accidental mutations
- Makes data flow explicit (no hidden state changes)
- Thread-safe by default
- Easier to reason about

**Trade-offs**:
- Slightly more verbose (must create new instances for changes)
- Minor performance cost (negligible for this use case)

### Why Pydantic for Config?
**Decision**: Use Pydantic for configuration validation

**Rationale**:
- Industry standard for Python data validation
- Excellent error messages
- Type coercion and validation in one step
- IDE autocomplete support

**Alternatives Considered**:
- Manual validation: Too error-prone
- attrs: Less validation features
- dataclasses only: No validation

### Why structlog?
**Decision**: Use structlog for logging

**Rationale**:
- Structured logging enables machine parsing
- Context propagation (adds metadata automatically)
- JSON output for log aggregation tools
- Better than stdlib logging for modern apps

**Alternatives Considered**:
- stdlib logging: Less structure, harder to parse
- loguru: More magic, less explicit

### Why plyer?
**Decision**: Use plyer for notifications

**Rationale**:
- Cross-platform abstraction
- Simple API
- Well-maintained
- No platform-specific code needed

**Limitations**:
- Windows-only in practice (primary target)
- Limited notification customization
- Graceful degradation handled in our code

---

## Future Extensions

### Planned Features

#### 1. **Web Dashboard** (notify-dashboard project)
```
New Components:
  - api (REST endpoints)
  - storage (notification history)

New Base:
  - web (FastAPI/Flask application)

Timeline: Q2 2025
```

#### 2. **Notification History**
```
New Component:
  - history (SQLite-backed storage)

Changes:
  - notification component: Log to history
  - New CLI commands: list, search

Timeline: Q3 2025
```

#### 3. **Plugin System**
```
New Component:
  - plugins (dynamic loader)

Features:
  - Custom notification backends
  - Post-send hooks
  - Filtering/routing logic

Timeline: Q4 2025
```

#### 4. **Rich Notifications**
```
Enhanced:
  - notification component: Support images, buttons

New Dependencies:
  - Notification backend upgrades
  - Platform-specific implementations

Timeline: 2026
```

### Extension Guidelines

#### Adding a New Component
1. Identify single responsibility
2. Define public interface (`__init__.py`)
3. Document in component README
4. Write tests first (TDD)
5. Ensure zero circular dependencies

#### Adding a New Project
1. Identify target use case
2. Select necessary components
3. Create `pyproject.toml` with brick mappings
4. Add project-specific dependencies
5. Document deployment process

#### Modifying Existing Components
1. Check dependent components/projects
2. Maintain backward compatibility
3. Update component README
4. Update relevant tests
5. Consider deprecation warnings if breaking

---

## Conclusion

The AI Task Notify Hook project demonstrates how Polylith architecture enables:
- **Modularity**: Easy to add/remove functionality
- **Reusability**: Components shared across projects
- **Testability**: Each component tested independently
- **Scalability**: Add projects without touching components

This architecture positions the project for long-term maintainability and future growth.

---

## References

- [Polylith Official Documentation](https://polylith.gitbook.io/polylith)
- [Python Polylith Tools](https://davidvujic.github.io/python-polylith-docs/)
- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [PEP 20 - The Zen of Python](https://peps.python.org/pep-0020/)
- [EAFP vs LBYL](https://docs.python.org/3/glossary.html#term-EAFP)

---

**Document Status**: ✅ Complete
**Review Date**: 2025-01-11
**Next Review**: 2025-07-11 (or when major changes occur)
