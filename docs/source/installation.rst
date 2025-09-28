============
Installation
============

Requirements
============

* Python 3.12 or higher
* Windows OS (for notification functionality)
* Modern terminal for best experience

.. note::
   While the notification features are Windows-specific, the core functionality
   can run on other platforms for development and testing purposes.

Installation Methods
===================

Using uv (Recommended)
----------------------

The fastest and most reliable installation method using `uv <https://docs.astral.sh/uv/>`_:

.. code-block:: console

   $ uv add AI-Task-Notify-Hook

For global installation:

.. code-block:: console

   $ uv tool install AI-Task-Notify-Hook

Using pip
---------

Standard installation via pip:

.. code-block:: console

   $ pip install AI-Task-Notify-Hook

Development Installation
========================

For development work, clone the repository and install in editable mode:

.. code-block:: console

   $ git clone https://github.com/user/AI-Task-Notify-Hook.git
   $ cd AI-Task-Notify-Hook
   $ uv sync
   $ uv run python -m ai_task_notify_hook.notify --help

Dependencies
============

Core Dependencies
-----------------

* **plyer**: Cross-platform notification library
* **structlog**: Structured logging library
* **PyYAML**: YAML configuration file support
* **orjson**: Fast JSON serialization for logging
* **colorama**: Colored terminal output

Development Dependencies
------------------------

* **mypy**: Static type checking
* **types-pyyaml**: Type stubs for PyYAML
* **types-requests**: Type stubs for requests

Verification
============

Verify your installation by running:

.. code-block:: console

   $ AI-Task-Notify-Hook "Test" "Installation successful!"

You should see a desktop notification if everything is working correctly.

Troubleshooting Installation
============================

Common Issues
-------------

**ModuleNotFoundError: No module named 'plyer'**
   The notification library is missing. Reinstall the package:

   .. code-block:: console

      $ uv add --force-reinstall AI-Task-Notify-Hook

**Permission denied on Windows**
   Run your terminal as administrator or install to user directory:

   .. code-block:: console

      $ pip install --user AI-Task-Notify-Hook

**Python version too old**
   This package requires Python 3.12+. Update your Python installation:

   .. code-block:: console

      $ python --version
      # Should show 3.12 or higher

Next Steps
==========

Once installed, continue to :doc:`usage` to learn how to use the tool effectively.