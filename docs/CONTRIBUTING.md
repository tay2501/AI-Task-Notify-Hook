# Contributing to AI-Task-Notify-Hook 🍞

Thank you for your interest in contributing to AI-Task-Notify-Hook! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- Git
- Windows 10/11 (for testing notifications)

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/AI-Task-Notify-Hook.git
   cd AI-Task-Notify-Hook
   ```

2. **Install Dependencies**
   ```bash
   uv sync --dev
   ```

3. **Verify Setup**
   ```bash
   uv run python -c "import notify; print('✓ Setup successful')"
   ```

## 🔧 Development Workflow

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Code Quality

Before submitting, ensure your code passes all checks:

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type checking
uv run mypy notify.py --ignore-missing-imports

# Security scan
uv run bandit -r .
```

### Testing

```bash
# Basic functionality test
uv run python -c "
import notify
notify.show_notification('Test', 'Development setup working!')
"

# Import test
uv run python -c "import notify; print('✓ Import successful')"
```

## 📝 Code Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/)
- Use [Ruff](https://docs.astral.sh/ruff/) for formatting and linting
- Include type hints for all functions
- Follow EAFP (Easier to Ask for Forgiveness than Permission) style

### Code Examples

#### Function Definition
```python
def show_notification(
    title: str,
    message: str,
    app_name: str = "Claude Code",
    timeout: int = 10
) -> None:
    """Display Windows notification using Plyer.

    Args:
        title: Notification title
        message: Notification message body
        app_name: Application name to display
        timeout: Notification timeout in seconds
    """
```

#### Error Handling
```python
try:
    notification.notify(...)
except Exception as e:
    print(f"Failed to show notification: {e}", file=sys.stderr)
    sys.exit(1)
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - OS version (Windows 10/11)
   - Python version
   - AI-Task-Notify-Hook version

2. **Steps to Reproduce**
   - Exact commands run
   - Expected vs actual behavior

3. **Error Output**
   - Full error messages
   - Stack traces if available

Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yml).

## ✨ Feature Requests

For new features:

1. Check existing issues first
2. Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yml)
3. Provide clear use cases
4. Consider backward compatibility

## 📋 Pull Request Process

### Before Submitting

1. **Update Documentation**
   - Update README.md for new features
   - Add docstrings for new functions
   - Update CHANGELOG.md

2. **Test Your Changes**
   - Run all code quality checks
   - Test on Windows 10/11
   - Verify CLI functionality

3. **Small, Focused Changes**
   - One feature/fix per PR
   - Clear, descriptive commit messages
   - Squash commits if necessary

### PR Template

Use the provided [PR template](.github/pull_request_template.md) and ensure:

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] Self-review completed

## 🏗️ Project Structure

```
AI-Task-Notify-Hook/
├── .github/                # GitHub templates and workflows
│   ├── workflows/         # CI/CD workflows
│   ├── ISSUE_TEMPLATE/    # Issue templates
│   └── SECURITY.md        # Security policy
├── notify.py              # Main notification script
├── pyproject.toml         # Project configuration
├── uv.lock               # Dependency lock file
├── README.md             # Project documentation
├── CHANGELOG.md          # Version history
├── LICENSE               # MIT license
└── CONTRIBUTING.md       # This file
```

## 🔄 Release Process

1. **Version Bump**
   - Update `pyproject.toml`
   - Update `CHANGELOG.md`

2. **Create Release**
   - Tag with `v{version}` format
   - GitHub Actions handles the rest

3. **Post-Release**
   - Verify CI/CD pipeline
   - Update documentation if needed

## 📚 Documentation

### Code Documentation

- Use Google-style docstrings
- Include type hints
- Document exceptions

### User Documentation

- Keep README.md current
- Include examples for new features
- Update CLI help text

## 🤝 Community

### Communication

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and improve

### Recognition

Contributors will be:
- Listed in release notes
- Mentioned in the contributors section
- Credited in security advisories (if applicable)

## ❓ Questions?

- Check existing [Issues](https://github.com/yourusername/AI-Task-Notify-Hook/issues)
- Create a new [Discussion](https://github.com/yourusername/AI-Task-Notify-Hook/discussions)
- Review the [README](README.md)

---

Thank you for contributing to AI-Task-Notify-Hook! 🎉