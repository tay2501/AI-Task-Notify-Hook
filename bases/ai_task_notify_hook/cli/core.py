"""CLI base component.

This base provides the command-line interface entry point.
Thin layer that orchestrates components - follows separation of concerns.

Updated to use fully async notification with asyncio.run() at the CLI boundary,
eliminating event loop overhead from the notification layer.
"""

import argparse
import asyncio
import sys

from pydantic import ValidationError

# Import from Polylith components
from ai_task_notify_hook.config import load_config
from ai_task_notify_hook.logging import configure_logging, get_logger
from ai_task_notify_hook.notification import show_notification
from ai_task_notify_hook.validation import (
    ConfigurationError,
    NotificationBackendError,
    NotificationError,
)


async def async_main() -> None:
    """Async main entry point for command line usage.

    Fully async implementation that uses asyncio.run() at the CLI boundary
    for optimal performance."""
    # Initialize logging first
    configure_logging()
    logger = get_logger("cli")

    # Load configuration
    app_config = load_config()

    logger.info("Starting notification application", version=app_config.version)

    parser = argparse.ArgumentParser(
        description="Display Windows notification for Claude Code hooks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python notify.py "Task Complete" "Claude Code finished successfully"
  python notify.py "Build Status" "Tests passed!" --app-name "Builder"
  python notify.py "Warning" "Check logs" --timeout 5
        """,
    )

    parser.add_argument("title", help="Notification title")
    parser.add_argument("message", help="Notification message")
    parser.add_argument(
        "--timeout",
        type=int,
        default=app_config.notification.timeout,
        help=(
            f"Notification timeout in seconds "
            f"(default: {app_config.notification.timeout})"
        ),
    )

    try:
        args = parser.parse_args()
        logger.info(
            "Parsed command line arguments",
            title=args.title,
            message=args.message,
            timeout=args.timeout,
        )

        # Use notification component (fully async)
        await show_notification(title=args.title, message=args.message, timeout=args.timeout)

        logger.info("Application completed successfully")

    except KeyboardInterrupt:
        logger.warning("Application cancelled by user", exit_code=1, signal="SIGINT")
        sys.exit(1)

    except NotificationBackendError as exc:
        # Platform/dependency issues - permanent failures
        logger.critical(
            "Notification backend unavailable",
            error=str(exc),
            suggestion="Check that plyer is installed and platform is supported",
            exit_code=2,
        )
        sys.exit(2)

    except ConfigurationError as exc:
        # Configuration loading issues
        logger.critical(
            "Configuration error",
            error=str(exc),
            suggestion="Check config/config.json syntax and values",
            exit_code=3,
        )
        sys.exit(3)

    except ValidationError as exc:
        # Pydantic validation failures - input validation errors
        logger.critical(
            "Input validation failed",
            error=str(exc),
            suggestion="Check title/message content and timeout range (1-300)",
            exit_code=4,
        )
        sys.exit(4)

    except NotificationError as exc:
        # General notification errors - transient failures
        logger.critical(
            "Notification failed",
            error=str(exc),
            error_type=type(exc).__name__,
            exit_code=1,
        )
        sys.exit(1)


def main() -> None:
    """Synchronous entry point that runs async_main with asyncio.

    This function provides a synchronous interface for setuptools entry_points
    while using asyncio.run() to execute the async_main() function.
    """
    asyncio.run(async_main())
