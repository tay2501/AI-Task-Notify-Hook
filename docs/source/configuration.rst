=============
Configuration
=============

Ai-task Notify Hook uses a flexible configuration system with JSON and YAML files
to control notification behavior, logging, and application settings.

Configuration Files
===================

The application looks for configuration files in the following locations:

* :file:`config/config.json` - Main application configuration
* :file:`config/logging_config.yaml` - Logging system configuration

If configuration files are not found, the application uses built-in defaults.

Main Configuration (config.json)
================================

The main configuration file controls notification and application behavior.

Default Configuration
---------------------

.. code-block:: json

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

Configuration Sections
----------------------

notification
~~~~~~~~~~~~

.. confval:: notification.app_name
   :type: ``str``
   :default: ``"Claude Code"``

   The application name displayed in notifications.

.. confval:: notification.timeout
   :type: ``int``
   :default: ``10``

   Notification display timeout in seconds. Must be between 1 and 300.

application
~~~~~~~~~~~

.. confval:: application.version
   :type: ``str``
   :default: ``"1.0.0"``

   Application version for logging and metadata.

.. confval:: application.debug
   :type: ``bool``
   :default: ``false``

   Enable debug mode for verbose logging.

Logging Configuration (logging_config.yaml)
===========================================

The logging configuration uses Python's dictConfig format with structlog integration.

Default Logging Setup
---------------------

.. code-block:: yaml

   version: 1
   disable_existing_loggers: false

   formatters:
     structured:
       format: "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"

   handlers:
     console:
       class: logging.StreamHandler
       level: INFO
       formatter: structured
       stream: ext://sys.stdout

     file:
       class: logging.handlers.RotatingFileHandler
       level: DEBUG
       formatter: structured
       filename: logs/notify.log
       maxBytes: 10485760  # 10MB
       backupCount: 5
       encoding: utf8

   loggers:
     notify:
       level: INFO
       handlers: [console, file]
       propagate: false

     config_loader:
       level: INFO
       handlers: [console, file]
       propagate: false

   root:
     level: INFO
     handlers: [console]

   # Application-specific settings
   app_logging:
     log_directory: logs

   # Structlog configuration
   structlog:
     cache_logger_on_first_use: true
     processors:
       - structlog.contextvars.merge_contextvars
       - structlog.stdlib.add_log_level
       - structlog.processors.TimeStamper:
           fmt: iso
           utc: true
       - structlog.stdlib.ProcessorFormatter.wrap_for_formatter

Configuration Validation
========================

The application includes built-in validation for all configuration values:

Type Validation
---------------

* String values are checked for non-empty content
* Integer values are validated within acceptable ranges
* Boolean values are strictly typed

Range Validation
----------------

* ``timeout``: Must be between 1 and 300 seconds
* File paths are validated for existence and permissions

Error Handling
--------------

When configuration validation fails:

1. Invalid JSON/YAML syntax triggers a detailed error message
2. Missing files fall back to built-in defaults
3. Invalid values use fallback defaults with warnings

Environment Variables
====================

While not currently implemented, the configuration system is designed to support
environment variable overrides in future versions:

.. code-block:: bash

   # Future support planned
   export NOTIFY_APP_NAME="My App"
   export NOTIFY_TIMEOUT=15
   export NOTIFY_DEBUG=true

Creating Custom Configurations
==============================

Application Configuration
-------------------------

Create a custom :file:`config/config.json`:

.. code-block:: json

   {
     "notification": {
       "app_name": "My Custom App",
       "timeout": 15
     },
     "application": {
       "version": "2.0.0",
       "debug": true
     }
   }

Logging Configuration
--------------------

Customize logging in :file:`config/logging_config.yaml`:

.. code-block:: yaml

   version: 1
   disable_existing_loggers: false

   handlers:
     console:
       class: logging.StreamHandler
       level: DEBUG  # More verbose console output
       formatter: structured
       stream: ext://sys.stdout

     custom_file:
       class: logging.handlers.TimedRotatingFileHandler
       level: INFO
       formatter: structured
       filename: logs/custom.log
       when: midnight
       backupCount: 30
       encoding: utf8

   loggers:
     my_app:
       level: DEBUG
       handlers: [console, custom_file]
       propagate: false

Configuration API
=================

Programmatic Configuration Access
--------------------------------

Load and access configuration programmatically:

.. code-block:: python

   from ai_task_notify_hook.config.config_loader import load_config, Config

   # Load configuration
   config = load_config("path/to/config.json")

   # Access values
   print(config.notification.app_name)
   print(config.application.debug)

   # Create configuration from dictionary
   config_data = {
       "notification": {"app_name": "Test App", "timeout": 5},
       "application": {"version": "1.0.0", "debug": True}
   }
   config = Config.from_dict(config_data)

Configuration Validation
------------------------

Validate configuration files before use:

.. code-block:: python

   from ai_task_notify_hook.config.config_loader import validate_config_file

   # Validate configuration
   is_valid = validate_config_file("config/config.json")
   if not is_valid:
       print("Configuration file is invalid")

Create Default Configuration
----------------------------

Generate a default configuration file:

.. code-block:: python

   from ai_task_notify_hook.config.config_loader import create_default_config

   # Create default config file
   create_default_config("config/config.json")

Troubleshooting Configuration
=============================

Common Issues
-------------

**JSON Syntax Errors**
   Use a JSON validator to check syntax:

   .. code-block:: console

      $ python -m json.tool config/config.json

**YAML Syntax Errors**
   Validate YAML syntax:

   .. code-block:: python

      import yaml
      with open('config/logging_config.yaml') as f:
          yaml.safe_load(f)

**Permission Errors**
   Ensure the config directory and files are writable:

   .. code-block:: console

      $ ls -la config/

**File Not Found**
   Check that configuration files exist in the expected location relative to
   the current working directory.

Debug Configuration Loading
---------------------------

Enable debug mode to see configuration loading details:

.. code-block:: json

   {
     "application": {
       "debug": true
     }
   }

Then check the logs for configuration loading information.

Next Steps
==========

For troubleshooting runtime issues, see :doc:`troubleshooting`. For API details,
check :doc:`api/modules`.