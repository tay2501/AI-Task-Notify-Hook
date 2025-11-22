<a href='https://ko-fi.com/Z8Z31J3LMW' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi6.png?v=6' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
<a href="https://www.buymeacoffee.com/tay2501" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 36px !important;width: 130px !important;" ></a>
# AI-Task-Notify-Hook 🍞

[![CI](https://github.com/tay2501/AI-Task-Notify-Hook/workflows/CI/badge.svg)](https://github.com/tay2501/AI-Task-Notify-Hook/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)

Professional Windows notification tool with structured logging, optimized for Claude Code hooks and automation workflows.

## ✨ Features

- 🚀 **Fast & Lightweight**: Minimal dependencies, maximum performance
- 🎯 **Claude Code Integration**: Perfect for automation hooks
- 🛡️ **Type Safe**: Full type hints and mypy support (Python 3.13+)
- 📊 **Structured Logging**: Advanced logging with structlog and 30-day rotation
- ⚙️ **External Configuration**: YAML-based logging configuration
- 🔧 **Highly Configurable**: Customizable timeout, app name, and logging
- 📦 **Modern Python**: Built with uv, follows latest best practices
- 🎨 **Rich Console Output**: Colored console logs with fallback support

## 🚀 Quick Start

### Installation

```bash
# Install with uv (recommended)
uv sync

# Or clone and install
git clone https://github.com/tay2501/AI-Task-Notify-Hook.git
cd AI-Task-Notify-Hook
uv sync
```

### Usage

#### Command Line

```bash
# Basic notification (with structured logging)
python src/ai_task_notify_hook/notify.py "Task Complete" "Claude Code finished successfully"

# Custom app name and timeout
python src/ai_task_notify_hook/notify.py "Build Status" "Tests passed!" --app-name "Builder" --timeout 5

# View logs (JSON format for analysis)
cat logs/notify.log
```

#### Log Output Examples

**Console Output (Colored):**
```
2025-09-23T11:12:10.907735Z [info     ] Starting notification application version=1.0.0
2025-09-23T11:12:10.914207Z [info     ] Application completed successfully
```

**Log File Output (JSON):**
```json
{"version":"1.0.0","event":"Starting notification application","level":"info","timestamp":"2025-09-23T11:12:10.907735Z"}
{"event":"Application completed successfully","level":"info","timestamp":"2025-09-23T11:12:10.914207Z"}
```

#### Claude Code Hook Integration

Add to your Claude Code hooks configuration:

```json
{
  "hooks": {
    "task-complete": ".venv/Scripts/python.exe notify.py \"Task Complete\" \"Claude Code finished successfully\" --timeout 3"
  }
}
```

#### Python API

```python
from ai_task_notify_hook.notify import show_notification

show_notification(
    title="My App",
    message="Process completed!",
    app_name="Custom App",
    timeout=5
)
```

#### Configuration File Customization

Create or modify `config.json` to customize default values:

```json
{
  "notification": {
    "app_name": "My Custom App",
    "timeout": 15
  },
  "application": {
    "version": "1.0.0",
    "debug": true
  }
}
```

Command line arguments always override configuration file settings.

## 📚 Documentation

Comprehensive documentation is available at: **[Documentation Site](https://AI-Task-Notify-Hook.readthedocs.io/)**

### Quick Links

- 📖 **[User Guide](docs/source/usage.rst)** - Complete usage examples and integration
- ⚙️ **[Configuration](docs/source/configuration.rst)** - Detailed configuration options
- 🔧 **[Troubleshooting](docs/source/troubleshooting.rst)** - Common issues and solutions
- 🛠️ **[API Reference](docs/source/api/modules.rst)** - Full API documentation
- 🤝 **[Contributing](docs/source/development/contributing.rst)** - Development guide

### Building Documentation Locally

```bash
# Install documentation dependencies
uv sync --extra docs

# Build HTML documentation
cd docs
make html

# View documentation
open build/html/index.html  # macOS
start build/html/index.html  # Windows
```

## 📖 API Reference

### Command Line Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `title` | str | ✅ | - | Notification title |
| `message` | str | ✅ | - | Notification message |
| `--app-name` | str | ❌ | "Claude Code" | Application name |
| `--timeout` | int | ❌ | 10 | Timeout in seconds |

### Python Function

```python
def show_notification(title: str, message: str, app_name: str = "Claude Code", timeout: int = 10) -> None
```

## ⚙️ Configuration

### Application Configuration

The application uses `config.json` for default notification settings:

```json
{
  "notification": {
    "app_name": "Claude Code",
    "timeout": 10
  },
  "application": {
    "version": "1.0.0",
    "debug": false
  }
}
```

#### Configuration Options

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `notification.app_name` | string | "Claude Code" | Application name displayed in notifications |
| `notification.timeout` | integer | 10 | Notification timeout in seconds (1-300) |
| `application.version` | string | "1.0.0" | Configuration version for compatibility |
| `application.debug` | boolean | false | Enable debug mode for additional logging |

#### Configuration Behavior

- **File Missing**: Uses hardcoded defaults with warning log
- **Invalid JSON**: Falls back to defaults with error log
- **Invalid Values**: Validates ranges and types, falls back on errors
- **Partial Config**: Missing fields use defaults, valid fields are applied

### Logging Configuration

The application uses `logging_config.yaml` for advanced logging configuration:

```yaml
version: 1
disable_existing_loggers: false

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: console_formatter

  rotating_file:
    class: logging.handlers.TimedRotatingFileHandler
    level: DEBUG
    filename: logs/notify.log
    when: midnight
    interval: 1
    backupCount: 30  # Keep logs for 30 days
    encoding: utf-8

app_logging:
  log_directory: logs
  max_retention_days: 30
  log_level: DEBUG
  enable_console_output: true
  enable_file_output: true
  log_format: json
```

### Log Rotation & Retention

- **Rotation**: Daily at midnight
- **Retention**: 30 days (configurable)
- **Format**: JSON for analysis, colored console for development
- **Location**: `logs/notify.log` and `logs/notify_error.log`

## 🔧 Troubleshooting

### Common Issues

#### 1. "plyer library not found"
```bash
# Solution: Install dependencies
uv add plyer
```

#### 2. "logging configuration failed"
```bash
# Check if logging_config.yaml exists
ls logging_config.yaml

# Verify YAML syntax
python -c "import yaml; yaml.safe_load(open('logging_config.yaml'))"
```

#### 3. "No log files created"
```bash
# Check if logs directory exists
mkdir logs

# Verify permissions
ls -la logs/
```

#### 4. Type checking errors
```bash
# Install all type stubs
uv add --dev types-pyyaml mypy

# Run type checking
uv run mypy src/ai_task_notify_hook/notify.py src/ai_task_notify_hook/config/log_config.py src/ai_task_notify_hook/config/config_loader.py
```

#### 5. Configuration file issues
```bash
# Create default configuration file
uv run python src/ai_task_notify_hook/config/config_loader.py

# Validate existing configuration
uv run python -c "from ai_task_notify_hook.config.config_loader import validate_config_file; print('Valid:', validate_config_file())"

# Test configuration loading
uv run python -c "from ai_task_notify_hook.config.config_loader import load_config; config = load_config(); print(f'App: {config.notification.app_name}, Timeout: {config.notification.timeout}')"
```

### Debug Mode

Enable debug logging by modifying `logging_config.yaml`:

```yaml
app_logging:
  log_level: DEBUG  # Change from INFO to DEBUG
```

## 🔧 Development

### Prerequisites

- Python 3.13+
- uv package manager
- Windows 10/11 (for notifications)
- YAML support for configuration

### Setup

```bash
# Clone repository
git clone https://github.com/tay2501/AI-Task-Notify-Hook.git
cd AI-Task-Notify-Hook

# Install dependencies
uv sync --dev

# Run tests
uv run python -c "import ai_task_notify_hook.notify; print('✓ Import successful')"
```

### Code Quality

```bash
# Linting with Ruff (fast Python linter)
uv run ruff check .

# Auto-fix issues with Ruff
uv run ruff check --fix .

# Format code with Ruff (replaces Black)
uv run ruff format .

# Check formatting without applying changes
uv run ruff format --check .

# Type checking with mypy
uv run mypy src/ai_task_notify_hook

# Run all checks
uv run ruff check --fix . && uv run ruff format . && uv run mypy src/ai_task_notify_hook

# Test notification
uv run python src/ai_task_notify_hook/notify.py "Test" "Development test" --timeout 3
```

## 🧪 Testing

The project includes comprehensive testing and validation:

- ✅ Python 3.13+ compatibility testing
- ✅ Type safety validation with MyPy
- ✅ Structured logging verification
- ✅ Configuration file validation
- ✅ Notification functionality testing
- ✅ Log rotation and retention testing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 🔒 Security

For security vulnerabilities, please see our [Security Policy](.github/SECURITY.md).

## 📋 Requirements

### Runtime Dependencies
- Python 3.13+
- Windows 10/11 (for notifications)
- plyer >= 2.1.0
- structlog >= 25.4.0
- orjson >= 3.11.3
- pyyaml >= 6.0.2
- colorama >= 0.4.6

### Development Dependencies
- ruff >= 0.13.2 (replaces flake8, black, isort, pylint)
- mypy >= 1.18.2
- pytest >= 8.0.0
- pytest-cov >= 5.0.0
- pytest-mock >= 3.12.0
- pytest-benchmark >= 4.0.0
- sphinx >= 7.3.0

## 🏗️ Design Principles

- **🎯 Single Responsibility**: Focuses on notification display with comprehensive logging
- **🔧 Simple Interface**: Minimal command-line arguments with powerful configuration
- **🐍 EAFP Style**: "Easier to Ask for Forgiveness than Permission"
- **🚀 Performance First**: Fast startup, minimal memory usage, efficient logging
- **📊 Observability**: Structured logging for monitoring and debugging
- **⚙️ Configuration-Driven**: External YAML configuration for flexibility
- **🛡️ Type Safety**: Full type hints for Python 3.13+ compatibility

---

<div align="center">
<b>Made with ❤️ for the Claude Code community</b>
</div>