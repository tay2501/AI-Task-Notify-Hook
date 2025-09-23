============
Contributing
============

We welcome contributions to Aitask Notify Hook! This guide will help you get
started with development and contributing to the project.

Development Setup
=================

Prerequisites
-------------

* Python 3.12 or higher
* uv package manager
* Git
* Windows OS (for full testing)

Getting Started
---------------

1. **Fork and Clone**

   .. code-block:: console

      $ git clone https://github.com/yourusername/aitask-notify-hook.git
      $ cd aitask-notify-hook

2. **Set up Development Environment**

   .. code-block:: console

      $ uv sync
      $ uv run python -c "import aitask_notify_hook; print('OK')"

3. **Install Development Dependencies**

   .. code-block:: console

      $ uv add --dev mypy types-pyyaml types-requests

Project Structure
================

.. code-block::

   aitask-notify-hook/
   ├── src/
   │   └── aitask_notify_hook/         # Main package
   │       ├── __init__.py
   │       ├── notify.py               # Core notification functionality
   │       └── config/                 # Configuration modules
   │           ├── __init__.py
   │           ├── config_loader.py    # Configuration loading
   │           └── log_config.py       # Logging setup
   ├── config/                         # Application configuration files
   │   ├── config.json
   │   └── logging_config.yaml
   ├── docs/                          # Documentation
   │   ├── source/                    # Sphinx source files
   │   └── build/                     # Generated documentation
   ├── tests/                         # Test suite (to be added)
   ├── pyproject.toml                 # Project configuration
   └── README.md

Code Style and Standards
========================

Code Formatting
---------------

This project follows Python best practices:

* **PEP 8** compliance
* **Type hints** for all public functions
* **Docstrings** in Google/NumPy format
* **Import organization** following isort standards

Example function with proper documentation:

.. code-block:: python

   def show_notification(
       title: str,
       message: str,
       app_name: str | None = None,
       timeout: int | None = None
   ) -> None:
       """Display Windows notification using Plyer.

       Args:
           title: Notification title
           message: Notification message body
           app_name: Application name to display (uses config default if None)
           timeout: Notification timeout in seconds (uses config default if None)

       Raises:
           ImportError: If plyer library is not available
           ValueError: If parameters are invalid

       Example:
           >>> show_notification("Hello", "World!", timeout=5)
       """

Type Checking
-------------

All code must pass mypy type checking:

.. code-block:: console

   $ uv run mypy src/aitask_notify_hook/

Error Handling
--------------

Follow the established error handling patterns:

* Use structured logging with context
* Provide fallback behaviors
* Include helpful error messages
* Log errors at appropriate levels

Testing
=======

Test Structure
--------------

Tests should be added to the ``tests/`` directory:

.. code-block::

   tests/
   ├── __init__.py
   ├── test_notify.py
   ├── test_config_loader.py
   └── test_log_config.py

Writing Tests
-------------

Use pytest for testing:

.. code-block:: python

   import pytest
   from aitask_notify_hook.notify import show_notification

   def test_notification_with_defaults():
       """Test notification with default parameters."""
       # Test implementation
       pass

   def test_notification_with_custom_params():
       """Test notification with custom parameters."""
       # Test implementation
       pass

Running Tests
-------------

.. code-block:: console

   # Run all tests
   $ uv run pytest

   # Run with coverage
   $ uv run pytest --cov=aitask_notify_hook

   # Run specific test file
   $ uv run pytest tests/test_notify.py

Documentation
=============

Building Documentation
----------------------

Build the documentation locally:

.. code-block:: console

   $ cd docs
   $ uv run sphinx-build -b html source build/html

View the documentation:

.. code-block:: console

   $ open build/html/index.html  # macOS
   $ start build/html/index.html  # Windows

Documentation Standards
----------------------

* Use clear, concise language
* Provide code examples
* Include type information
* Document all public APIs
* Keep examples up to date

Adding New Documentation
-----------------------

1. Create new ``.rst`` files in ``docs/source/``
2. Add them to the appropriate ``toctree``
3. Build and test the documentation
4. Ensure all links work correctly

Pull Request Process
====================

Preparation
-----------

Before submitting a pull request:

1. **Create a feature branch**:

   .. code-block:: console

      $ git checkout -b feature/your-feature-name

2. **Make your changes** following the coding standards

3. **Add tests** for new functionality

4. **Update documentation** as needed

5. **Verify everything works**:

   .. code-block:: console

      $ uv run mypy src/
      $ uv run pytest
      $ cd docs && uv run sphinx-build -b html source build/html

Submission
----------

1. **Commit your changes** with descriptive messages:

   .. code-block:: console

      $ git commit -m "Add: new notification timeout feature

      - Implement configurable timeout validation
      - Add tests for timeout edge cases
      - Update documentation with examples"

2. **Push your branch**:

   .. code-block:: console

      $ git push origin feature/your-feature-name

3. **Create a pull request** with:
   - Clear description of changes
   - Reference to any related issues
   - Screenshots if applicable (for UI changes)

Code Review Guidelines
---------------------

When reviewing code:

* Check for code style compliance
* Verify test coverage
* Ensure documentation is updated
* Test the functionality
* Provide constructive feedback

Release Process
===============

Version Management
------------------

This project uses semantic versioning (SemVer):

* **MAJOR**: Breaking changes
* **MINOR**: New features (backward compatible)
* **PATCH**: Bug fixes (backward compatible)

Update version in:
* ``pyproject.toml``
* ``src/aitask_notify_hook/__init__.py``
* ``docs/source/conf.py``

Creating Releases
----------------

1. **Update version numbers**
2. **Update CHANGELOG.md**
3. **Create and test the build**:

   .. code-block:: console

      $ uv build

4. **Tag the release**:

   .. code-block:: console

      $ git tag -a v1.0.0 -m "Release version 1.0.0"
      $ git push origin v1.0.0

Getting Help
============

If you need help with development:

* Check this contributing guide
* Review the :doc:`../api/modules`
* Look at existing code for patterns
* Ask questions in issues or discussions

Issue Reporting
===============

When reporting bugs:

1. **Use the issue template**
2. **Provide reproduction steps**
3. **Include system information**
4. **Add relevant logs or error messages**
5. **Specify expected vs actual behavior**

Feature Requests
================

When requesting features:

1. **Describe the use case**
2. **Explain the problem being solved**
3. **Provide examples if possible**
4. **Consider backward compatibility**

Thank You
=========

Thank you for contributing to Aitask Notify Hook! Your contributions help
make this tool better for everyone.