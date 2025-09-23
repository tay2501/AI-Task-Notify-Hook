# Security Policy

## Supported Versions

We actively support the following versions of Aitask-Notify-Hook with security updates:

| Version | Python Requirement | Supported          |
| ------- | ------------------ | ------------------ |
| 1.x.x   | Python 3.12+      | :white_check_mark: |
| < 1.0   | Python 3.8+       | :x:                |

**Note**: Only Python 3.12+ is supported for security updates. Older Python versions are not maintained.

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in Aitask-Notify-Hook, please report it responsibly:

### How to Report

1. **DO NOT** open a public GitHub issue for security vulnerabilities
2. Send an email to [your-security-email@example.com] with:
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

When using Aitask-Notify-Hook:

1. **Keep Updated**: Always use the latest version
2. **Validate Input**: Be cautious with notification content from untrusted sources
3. **System Permissions**: Run with minimal required permissions
4. **Network Security**: Aitask-Notify-Hook doesn't make network requests, but be aware of your environment

### Scope

This security policy covers:
- The core Aitask-Notify-Hook notification functionality
- Command-line interface security
- Dependency vulnerabilities in our supply chain

### Out of Scope

- Issues in dependencies that don't affect Aitask-Notify-Hook
- General Windows notification system vulnerabilities
- Social engineering attacks

## Security Features

- **No Network Access**: Aitask-Notify-Hook doesn't make external network requests
- **Minimal Dependencies**: We maintain a small, audited dependency footprint
- **Input Validation**: All user inputs are properly validated and sanitized
- **Secure Configuration**: JSON configuration files with schema validation
- **Structured Logging**: Secure structured logging prevents information disclosure
- **Type Safety**: Full type hints and mypy validation (Python 3.12+)
- **Error Handling**: Secure error handling with structured logging
- **No Credential Storage**: Application doesn't store or process sensitive credentials

Thank you for helping keep Aitask-Notify-Hook secure!