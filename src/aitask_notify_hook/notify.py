#!/usr/bin/env python3
"""
Windows notification tool for Claude Code hooks.
Simple notification script using Plyer library with structured logging.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Configure logging before importing other modules
try:
    from .config.log_config import configure_logging, get_logger
    configure_logging()
    logger = get_logger("notify")
except ImportError as exc:
    # Critical failure - must use stderr fallback
    import logging
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
        stream=sys.stderr
    )
    fallback_logger = logging.getLogger("notify.fallback")
    fallback_logger.error("Critical: logging configuration failed - missing dependencies. Error: %s. Suggestion: Check log_config.py dependencies", str(exc))
    sys.exit(1)

# Load configuration
try:
    from .config.config_loader import load_config, Config
    app_config = load_config()
except ImportError as exc:
    logger.error("Configuration loader not available, using hardcoded defaults",
                error=str(exc))
    # Fallback to hardcoded defaults
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class FallbackNotificationConfig:
        app_name: str = "Claude Code"
        timeout: int = 10

    @dataclass(frozen=True)
    class FallbackConfig:
        notification: FallbackNotificationConfig = FallbackNotificationConfig()

    app_config = FallbackConfig()
except Exception as exc:
    logger.warning("Failed to load configuration, using defaults",
                  error=str(exc))
    app_config = load_config()  # This will use fallback defaults

try:
    from plyer import notification  # type: ignore[import-untyped]
except ImportError as exc:
    logger.critical("plyer library not found - cannot display notifications",
                   error=str(exc), suggestion="Install with: uv add plyer",
                   exit_code=1)
    sys.exit(1)


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
    """
    # Use configuration defaults if not provided
    if app_name is None:
        app_name = app_config.notification.app_name
    if timeout is None:
        timeout = app_config.notification.timeout

    logger.info("Attempting to show notification",
                title=title, message=message, app_name=app_name, timeout=timeout,
                config_used=True)

    try:
        # Use the correct Plyer notification API as per latest documentation
        notification.notify(
            title=title,
            message=message,
            app_name=app_name,
            timeout=timeout
        )
        logger.info("Notification displayed successfully",
                   title=title, app_name=app_name, timeout=timeout)
    except ImportError as exc:
        logger.critical("plyer library not properly imported during notification",
                       error=str(exc), title=title, exit_code=1)
        sys.exit(1)
    except AttributeError as exc:
        logger.critical("plyer notification method not available",
                       error=str(exc), title=title, suggestion="Check plyer installation",
                       exit_code=1)
        sys.exit(1)
    except Exception as exc:
        logger.critical("Failed to show notification - unexpected error",
                       error=str(exc), title=title, app_name=app_name,
                       error_type=type(exc).__name__, exit_code=1)
        sys.exit(1)


def main() -> None:
    """Main entry point for command line usage."""
    logger.info("Starting notification application", version="1.0.0")

    parser = argparse.ArgumentParser(
        description="Display Windows notification for Claude Code hooks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python notify.py "Task Complete" "Claude Code finished successfully"
  python notify.py "Build Status" "Tests passed!" --app-name "Builder"
  python notify.py "Warning" "Check logs" --timeout 5
        """
    )

    parser.add_argument("title", help="Notification title")
    parser.add_argument("message", help="Notification message")
    parser.add_argument(
        "--app-name",
        default=app_config.notification.app_name,
        help=f"Application name (default: {app_config.notification.app_name})"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=app_config.notification.timeout,
        help=f"Notification timeout in seconds (default: {app_config.notification.timeout})"
    )

    try:
        args = parser.parse_args()
        logger.info("Parsed command line arguments",
                   title=args.title, message=args.message,
                   app_name=args.app_name, timeout=args.timeout)

        show_notification(args.title, args.message, args.app_name, args.timeout)

        logger.info("Application completed successfully")
    except KeyboardInterrupt:
        logger.warning("Application cancelled by user", exit_code=1,
                      signal="SIGINT")
        sys.exit(1)
    except Exception as exc:
        logger.critical("Application failed with unexpected error",
                       error=str(exc), error_type=type(exc).__name__,
                       exit_code=1)
        sys.exit(1)


if __name__ == "__main__":
    main()