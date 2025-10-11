# Models Component

## Purpose
Shared data models and enumerations used across all components.

## Design Principles
- **Zero dependencies**: No imports from other components
- **Immutable**: All models are frozen dataclasses or Pydantic models
- **Simple**: Minimal logic, focused on data representation
- **Type-safe**: Full type hints for mypy strict mode

## Exports
- `NotificationLevel`: Enum for notification severity
- `LogLevel`: Enum for logging levels
- `NotificationRequest`: Immutable notification request data

## Usage
```python
from ai_task_notify_hook.models import NotificationRequest, NotificationLevel

request = NotificationRequest(
    title="Task Complete",
    message="Build finished successfully",
    level=NotificationLevel.SUCCESS,
    timeout=10
)
```

## Dependencies
- Python 3.12+ standard library only
- No external dependencies