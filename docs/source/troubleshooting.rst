===============
Troubleshooting
===============

This guide helps resolve common issues when using Ai-task Notify Hook.

Common Issues
=============

Notifications Not Appearing
---------------------------

**Symptoms**: Commands run without error but no notifications appear.

**Possible Causes**:

1. **Windows Focus Assist enabled**

   .. code-block:: console

      # Check Windows Focus Assist settings
      # Windows Settings > System > Focus assist

2. **Plyer backend issues**

   Test the notification system:

   .. code-block:: python

      from plyer import notification
      notification.notify(title="Test", message="Testing")

3. **Notification timeout too short**

   Try a longer timeout:

   .. code-block:: console

      $ AI-Task-Notify-Hook "Test" "Message" --timeout 30

**Solutions**:

- Disable Windows Focus Assist temporarily
- Update Plyer: ``uv add --upgrade plyer``
- Check Windows notification settings
- Test with different timeout values

Import Errors
-------------

**ModuleNotFoundError: No module named 'ai_task_notify_hook'**

.. code-block:: console

   # Verify installation
   $ python -c "import ai_task_notify_hook; print('OK')"

   # Reinstall if needed
   $ uv add --force-reinstall AI-Task-Notify-Hook

**ModuleNotFoundError: No module named 'plyer'**

.. code-block:: console

   # Check dependencies
   $ uv add plyer structlog pyyaml orjson colorama

Configuration Issues
-------------------

**Configuration file not found**

The application works with default settings, but you can create configuration files:

.. code-block:: python

   from ai_task_notify_hook.config.config_loader import create_default_config
   create_default_config("config/config.json")

**Invalid JSON configuration**

Validate your JSON:

.. code-block:: console

   $ python -m json.tool config/config.json

**YAML logging configuration errors**

Check YAML syntax:

.. code-block:: python

   import yaml
   with open('config/logging_config.yaml') as f:
       try:
           yaml.safe_load(f)
           print("YAML is valid")
       except yaml.YAMLError as e:
           print(f"YAML error: {e}")

Logging Issues
--------------

**No log files created**

Check permissions and create log directory:

.. code-block:: console

   $ mkdir -p logs
   $ chmod 755 logs

**Logs not appearing in console**

Enable debug mode in configuration:

.. code-block:: json

   {
     "application": {
       "debug": true
     }
   }

**Structured logging not working**

Verify structlog installation:

.. code-block:: console

   $ python -c "import structlog; print(structlog.__version__)"

Command Line Issues
==================

**Command not found: AI-Task-Notify-Hook**

The script entry point isn't available. Try:

.. code-block:: console

   # Direct module execution
   $ python -m ai_task_notify_hook.notify "Test" "Message"

   # Check if script is in PATH
   $ which AI-Task-Notify-Hook

**Permission denied errors**

On Windows, run as administrator or install for user:

.. code-block:: console

   $ pip install --user AI-Task-Notify-Hook

Performance Issues
==================

**Slow startup**

The application may be slow on first run due to:

1. Module imports
2. Configuration file loading
3. Logging setup

This is normal and subsequent runs are faster.

**High memory usage**

Check for:

1. Large log files in the logs directory
2. Multiple Python processes running
3. Logging configuration with high verbosity

Debug Mode
==========

Enable comprehensive debugging:

.. code-block:: json

   {
     "application": {
       "debug": true,
       "version": "1.0.0"
     },
     "notification": {
       "app_name": "Debug App",
       "timeout": 10
     }
   }

Then run with verbose output:

.. code-block:: console

   $ python -m ai_task_notify_hook.notify "Debug Test" "Debug message" --app-name "Debug"

Platform-Specific Issues
========================

Windows-Specific
----------------

**Windows Defender blocking**

If Windows Defender flags the application:

1. Add Python executable to exclusions
2. Add the project directory to exclusions
3. Use Windows Security settings to allow the app

**PowerShell execution policy**

If using PowerShell scripts:

.. code-block:: powershell

   # Check current policy
   Get-ExecutionPolicy

   # Set policy for current user
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

**UAC (User Account Control)**

Some notification features may require elevated privileges.
Try running your terminal as administrator.

Error Codes and Messages
========================

Exit Codes
----------

* **0**: Success
* **1**: General error (missing dependencies, configuration issues, etc.)

Common Error Messages
--------------------

**"plyer library not found"**
   Install dependencies: ``uv add plyer``

**"Configuration loader not available"**
   Configuration module issue. Check Python path and installation.

**"Failed to show notification"**
   Notification system unavailable. Check Windows notification settings.

**"Critical: logging configuration failed"**
   Logging setup issue. Check YAML configuration file.

Getting Help
============

Collecting Debug Information
---------------------------

When reporting issues, include:

1. **Version information**:

   .. code-block:: console

      $ python --version
      $ python -c "import ai_task_notify_hook; print(ai_task_notify_hook.__version__)"

2. **System information**:

   .. code-block:: console

      $ python -c "import sys, platform; print(f'{platform.system()} {platform.release()}')"

3. **Configuration files** (remove sensitive information)

4. **Log files** from the logs directory

5. **Full error messages** with stack traces

Test Script
-----------

Use this test script to diagnose issues:

.. code-block:: python

   #!/usr/bin/env python3
   """Diagnostic script for Ai-task Notify Hook."""

   import sys
   import platform
   from pathlib import Path

   def test_imports():
       """Test all imports."""
       try:
           import ai_task_notify_hook
           print("✓ Main package import: OK")
       except ImportError as e:
           print(f"✗ Main package import failed: {e}")
           return False

       try:
           from ai_task_notify_hook.notify import show_notification
           print("✓ Notification function import: OK")
       except ImportError as e:
           print(f"✗ Notification function import failed: {e}")
           return False

       try:
           import plyer
           print("✓ Plyer import: OK")
       except ImportError as e:
           print(f"✗ Plyer import failed: {e}")
           return False

       return True

   def test_notification():
       """Test notification functionality."""
       try:
           from ai_task_notify_hook.notify import show_notification
           show_notification("Test", "Diagnostic test notification")
           print("✓ Test notification sent")
           return True
       except Exception as e:
           print(f"✗ Test notification failed: {e}")
           return False

   def main():
       """Run all diagnostic tests."""
       print(f"Python: {sys.version}")
       print(f"Platform: {platform.system()} {platform.release()}")
       print(f"Working directory: {Path.cwd()}")
       print("-" * 50)

       if not test_imports():
           sys.exit(1)

       if not test_notification():
           sys.exit(1)

       print("-" * 50)
       print("✓ All tests passed!")

   if __name__ == "__main__":
       main()

Run this script to identify issues:

.. code-block:: console

   $ python test_diagnosis.py

Support Resources
----------------

* Check the :doc:`api/modules` for API details
* Review :doc:`configuration` for setup options
* See :doc:`usage` for usage examples

Next Steps
==========

If you've resolved your issue, consider contributing to the documentation
by reporting what worked. See :doc:`development/contributing` for details.