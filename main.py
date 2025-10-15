"""Main entry point for the Hyperliquid Trading Bot."""

import asyncio
import sys
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv
import yaml

from src.core.orchestrator import BotOrchestrator


def load_config() -> dict:
    """
    Load configuration from YAML file.

    Returns:
        Configuration dictionary
    """
    config_path = Path("config/config.yaml")

    if not config_path.exists():
        logger.error(f"Configuration file not found: {config_path}")
        sys.exit(1)

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    logger.info("Configuration loaded successfully")
    return config


def setup_logging(config: dict) -> None:
    """
    Set up logging configuration.

    Args:
        config: Configuration dictionary
    """
    log_config = config.get("logging", {})
    log_level = log_config.get("level", "INFO")
    log_format = log_config.get(
        "format",
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>"
    )

    # Remove default logger
    logger.remove()

    # Add console logger
    logger.add(
        sys.stderr,
        format=log_format,
        level=log_level,
        colorize=True
    )

    # Add file logger
    log_dir = Path(log_config.get("log_dir", "./data/logs"))
    log_dir.mkdir(parents=True, exist_ok=True)

    logger.add(
        log_dir / "bot_{time:YYYY-MM-DD}.log",
        format=log_format,
        level="DEBUG",
        rotation=log_config.get("rotation", "500 MB"),
        retention=log_config.get("retention", "10 days"),
        compression="zip"
    )

    logger.info("Logging configured")


async def main() -> None:
    """Main async entry point."""
    # Load environment variables
    load_dotenv()

    # Load configuration
    config = load_config()

    # Setup logging
    setup_logging(config)

    logger.info("=" * 60)
    logger.info("Hyperliquid Trading Bot")
    logger.info("=" * 60)

    # Create and start bot orchestrator
    bot = BotOrchestrator(config)

    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
    finally:
        await bot.stop()
        logger.info("Bot shutdown complete")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot terminated by user")
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)
