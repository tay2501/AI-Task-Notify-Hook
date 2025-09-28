=====
Usage
=====

This page covers various ways to use Ai-task Notify Hook, from basic command-line
usage to advanced Python API integration.

Command Line Interface
======================

Basic Notification
------------------

Display a simple notification:

.. code-block:: console

   $ AI-Task-Notify-Hook "Task Complete" "Your task has finished successfully"

Custom App Name and Timeout
---------------------------

Customize the notification appearance and duration:

.. code-block:: console

   $ AI-Task-Notify-Hook "Build Status" "Tests passed!" --app-name "CI/CD" --timeout 10

Available Options
-----------------

.. program:: AI-Task-Notify-Hook

.. option:: title

   The notification title (required)

.. option:: message

   The notification message body (required)

.. option:: --app-name <name>

   Application name to display (default: "Claude Code")

.. option:: --timeout <seconds>

   Notification timeout in seconds (default: 10)

.. option:: --help

   Show help message and exit

Python API
===========

Basic Usage
-----------

Import and use the notification function:

.. code-block:: python

   from ai_task_notify_hook.notify import show_notification

   # Simple notification
   show_notification("Hello", "World!")

   # With custom settings
   show_notification(
       title="Build Status",
       message="All tests passed successfully",
       app_name="CI System",
       timeout=5
   )

Configuration Loading
---------------------

Work with configuration files:

.. code-block:: python

   from ai_task_notify_hook.config.config_loader import load_config

   # Load configuration
   config = load_config()

   # Access settings
   print(f"App name: {config.notification.app_name}")
   print(f"Timeout: {config.notification.timeout}")

Advanced Logging Setup
----------------------

Set up structured logging:

.. code-block:: python

   from ai_task_notify_hook.config.log_config import configure_logging, get_logger

   # Configure logging
   configure_logging()

   # Get a logger
   logger = get_logger("my_app")

   # Use structured logging
   logger.info("Application started",
              version="1.0.0",
              user="admin")

Claude Code Integration
=======================

Hook Configuration
------------------

Add to your Claude Code hook configuration:

.. code-block:: json

   {
     "hooks": {
       "on_completion": {
         "command": "AI-Task-Notify-Hook",
         "args": ["Task Complete", "Claude Code finished the task"]
       },
       "on_error": {
         "command": "AI-Task-Notify-Hook",
         "args": ["Error", "Claude Code encountered an error", "--timeout", "15"]
       }
     }
   }

Script Integration
------------------

Use in shell scripts:

.. code-block:: bash

   #!/bin/bash

   # Run your command
   your_command

   # Check exit status and notify
   if [ $? -eq 0 ]; then
       AI-Task-Notify-Hook "Success" "Command completed successfully"
   else
       AI-Task-Notify-Hook "Error" "Command failed" --timeout 30
   fi

PowerShell Integration
---------------------

Use in PowerShell scripts:

.. code-block:: powershell

   # Run your command
   try {
       Your-Command
       AI-Task-Notify-Hook "Success" "PowerShell command completed"
   }
   catch {
       AI-Task-Notify-Hook "Error" "PowerShell command failed: $($_.Exception.Message)"
   }

Error Handling
==============

The tool includes comprehensive error handling:

Graceful Fallbacks
------------------

* If Plyer is unavailable, the tool exits with a clear error message
* If configuration files are missing, defaults are used
* If logging setup fails, stderr fallback is activated

Exit Codes
----------

* **0**: Success
* **1**: General error (missing dependencies, invalid arguments, etc.)

Debug Mode
----------

Enable debug logging by modifying the configuration file:

.. code-block:: json

   {
     "application": {
       "debug": true
     }
   }

Best Practices
==============

1. **Test First**: Always test notifications in your environment
2. **Configure Timeouts**: Adjust timeout values based on notification importance
3. **Use Meaningful Messages**: Provide clear, actionable notification content
4. **Handle Errors**: Wrap notification calls in try-catch blocks for production use
5. **Monitor Logs**: Check log files for debugging information

Examples
========

CI/CD Pipeline
--------------

.. code-block:: yaml

   # GitHub Actions example
   - name: Notify on Success
     if: success()
     run: AI-Task-Notify-Hook "Build Success" "All tests passed!"

   - name: Notify on Failure
     if: failure()
     run: AI-Task-Notify-Hook "Build Failed" "Check the logs for details" --timeout 30

Development Workflow
--------------------

.. code-block:: python

   import subprocess

   def run_tests_with_notification():
       """Run tests and notify of results."""
       try:
           result = subprocess.run(['pytest'], capture_output=True, text=True)
           if result.returncode == 0:
               show_notification("Tests Passed", "All tests completed successfully")
           else:
               show_notification("Tests Failed", f"Failed tests: {result.stderr[:100]}")
       except Exception as e:
           show_notification("Error", f"Test execution failed: {e}")

Next Steps
==========

Learn about configuration options in :doc:`configuration` or check the
:doc:`api/modules` for detailed API documentation.