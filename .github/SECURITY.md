# Security Policy

## Supported Versions

We actively support the following versions of AI-Task-Notify-Hook with security updates:

| Version | Python Requirement | Supported          |
| ------- | ------------------ | ------------------ |
| 1.x.x   | Python 3.12+      | :white_check_mark: |
| < 1.0   | Python 3.8+       | :x:                |

**Note**: Only Python 3.12+ is supported for security updates. Older Python versions are not maintained.

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in AI-Task-Notify-Hook, please report it responsibly:

### How to Report

1. **DO NOT** open a public GitHub issue for security vulnerabilities
2. Use GitHub's private vulnerability reporting feature:
   - Go to the repository's Security tab
   - Click "Report a vulnerability"
   - Fill out the private vulnerability report

   Or send an email to [security contact needed] with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Your contact information

### What to Expect

- **Response Time**: We will acknowledge your report within 48 hours
- **Investigation**: We will investigate and validate the issue within 5 business days
- **Resolution**: We will work on a fix and coordinate disclosure timing with you
- **Credit**: We will acknowledge your contribution in the security advisory (if desired)

### Security Best Practices

When using AI-Task-Notify-Hook:

1. **Keep Updated**: Always use the latest version
2. **Validate Input**: Be cautious with notification content from untrusted sources
3. **System Permissions**: Run with minimal required permissions
4. **Network Security**: AI-Task-Notify-Hook doesn't make network requests, but be aware of your environment

### Scope

This security policy covers:
- The core AI-Task-Notify-Hook notification functionality
- Command-line interface security
- Dependency vulnerabilities in our supply chain

### Out of Scope

- Issues in dependencies that don't affect AI-Task-Notify-Hook
- General operating system notification system vulnerabilities
- Social engineering attacks
- Issues in Python interpreter or uv package manager itself

## Security Features

- **No Network Access**: AI-Task-Notify-Hook doesn't make external network requests
- **Minimal Dependencies**: We maintain a small, audited dependency footprint:
  - `colorama` for cross-platform terminal colors
  - `orjson` for fast, secure JSON parsing
  - `plyer` for cross-platform notifications
  - `pyyaml` for configuration files
  - `structlog` for structured logging
- **Input Validation**: All user inputs are properly validated and sanitized
- **Secure Configuration**: YAML/JSON configuration files with schema validation
- **Structured Logging**: Secure structured logging prevents information disclosure
- **Type Safety**: Full type hints and mypy validation (Python 3.12+)
- **Error Handling**: Secure error handling with structured logging
- **No Credential Storage**: Application doesn't store or process sensitive credentials
- **Cross-Platform**: Secure notification support for Windows, macOS, and Linux

Thank you for helping keep AI-Task-Notify-Hook secure!