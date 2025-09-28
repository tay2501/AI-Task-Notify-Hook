# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup with GitHub workflows
- Comprehensive CI/CD pipeline
- Security scanning and vulnerability checks

## [1.0.0] - 2024-09-23

### Added
- Windows notification tool for Claude Code hooks
- Simple command-line interface using argparse
- Plyer library integration for cross-platform notifications
- Support for customizable notification timeout
- Application name configuration
- Comprehensive error handling
- Type hints for better code maintainability

### Features
- Display Windows notifications with custom title and message
- Configurable application name (defaults to "Claude Code")
- Timeout control (default: 10 seconds)
- Robust error handling and user feedback

### Dependencies
- Python 3.8+ support
- Plyer >= 2.1.0 for notification functionality

### Documentation
- README with usage examples
- CLI help text and examples
- Type hints for all functions

[Unreleased]: https://github.com/tay2501/AI-Task-Notify-Hook/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/tay2501/AI-Task-Notify-Hook/releases/tag/v1.0.0