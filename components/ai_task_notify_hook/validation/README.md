# Validation Component

## Purpose
Provides custom exception classes for error handling across all components.
All data validation is delegated to Pydantic models in the config component.

## Design Principles
- **Exception hierarchy**: All exceptions inherit from `NotificationError` base class
- **Descriptive errors**: Each exception includes context and optional cause tracking
- **EAFP style**: Designed for "Easier to Ask for Forgiveness than Permission" approach
- **Zero validation logic**: Pure exception definitions, validation is handled by Pydantic

## Exports
- `NotificationError`: Base exception class for all application errors
- `ConfigurationError`: Configuration loading and validation failures
- `ValidationError`: Input validation failures
- `NotificationBackendError`: Platform notification system failures

## Usage
```python
from ai_task_notify_hook.validation import ConfigurationError, NotificationBackendError

# Raising exceptions with context
try:
    config = load_config("invalid.json")
except json.JSONDecodeError as e:
    raise ConfigurationError(
        f"Failed to parse config file: invalid.json",
        cause=e
    ) from e

# Catching application-specific errors
try:
    show_notification(title, message)
except NotificationBackendError as e:
    logger.error("Notification failed", error=str(e))
```

## Exception Hierarchy
```
NotificationError (base)
├── ConfigurationError
├── ValidationError
└── NotificationBackendError
```

## Design Note
This component intentionally does NOT contain validation logic.
All validation is performed by Pydantic models in the `config` component
and dataclass validators in the `models` component.

## Dependencies
- Python 3.12+ standard library only
- No external dependencies
