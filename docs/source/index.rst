=====================================
Ai-task Notify Hook Documentation
=====================================

.. image:: https://img.shields.io/pypi/v/AI-Task-Notify-Hook.svg
   :target: https://pypi.org/project/AI-Task-Notify-Hook/
   :alt: PyPI Version

.. image:: https://img.shields.io/badge/python-3.12+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python 3.12+

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :target: https://github.com/astral-sh/ruff
   :alt: Ruff

A simple and robust Windows notification tool designed specifically for Claude Code hooks,
providing structured logging and reliable desktop notifications.

.. note::
   This tool is designed for Windows environments and uses the Plyer library
   for cross-platform notification support.

Features
========

* 🔔 **Desktop Notifications**: Clean, reliable Windows notifications via Plyer
* 📊 **Structured Logging**: Built with structlog for excellent debugging experience
* ⚙️ **Configurable**: JSON configuration with YAML logging setup
* 🧩 **Hook-Friendly**: Designed specifically for Claude Code hook integration
* 🛡️ **Error Handling**: Comprehensive error handling with fallbacks
* 📝 **Type Safe**: Full type hints and mypy compatibility

Quick Start
===========

Installation
------------

Install using uv (recommended):

.. code-block:: console

   $ uv add AI-Task-Notify-Hook

Or using pip:

.. code-block:: console

   $ pip install AI-Task-Notify-Hook

Basic Usage
-----------

Command line usage:

.. code-block:: console

   $ AI-Task-Notify-Hook "Task Complete" "Claude Code finished successfully"

Python API usage:

.. code-block:: python

   from ai_task_notify_hook.notify import show_notification

   show_notification(
       title="Build Status",
       message="Tests passed!",
       app_name="Builder",
       timeout=5
   )

Configuration
=============

The application supports configuration via JSON and YAML files:

* :file:`config/config.json` - Application settings
* :file:`config/logging_config.yaml` - Logging configuration

See :doc:`configuration` for detailed configuration options.

Table of Contents
=================

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   usage
   configuration
   troubleshooting

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/modules

.. toctree::
   :maxdepth: 1
   :caption: Development

   development/contributing
   development/changelog

.. toctree::
   :maxdepth: 1
   :caption: About

   license

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`