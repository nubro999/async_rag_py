"""Event processor for handling WebSocket events."""

from typing import Dict, Any, Callable, List
import asyncio
from loguru import logger


class EventProcessor:
    """
    Handles WebSocket events with real-time data streaming
    and event-driven architecture.
    """

    def __init__(self):
        """Initialize the event processor."""
        self.handlers: Dict[str, List[Callable]] = {}
        self.running = False
        logger.info("Event Processor initialized")

    def register_handler(
        self,
        event_type: str,
        handler: Callable
    ) -> None:
        """
        Register an event handler.

        Args:
            event_type: Type of event (e.g., 'orderbook', 'trade', 'account')
            handler: Async function to handle the event
        """
        if event_type not in self.handlers:
            self.handlers[event_type] = []

        self.handlers[event_type].append(handler)
        logger.debug(f"Registered handler for {event_type}")

    def unregister_handler(
        self,
        event_type: str,
        handler: Callable
    ) -> None:
        """
        Unregister an event handler.

        Args:
            event_type: Type of event
            handler: Handler function to remove
        """
        if event_type in self.handlers:
            self.handlers[event_type].remove(handler)
            logger.debug(f"Unregistered handler for {event_type}")

    async def process_orderbook_update(
        self,
        update: Dict[str, Any]
    ) -> None:
        """
        Process order book update event.

        Args:
            update: Order book update data
        """
        logger.debug("Processing orderbook update")
        await self.emit_event("orderbook", update)

    async def process_trade_update(
        self,
        trade: Dict[str, Any]
    ) -> None:
        """
        Process trade update event.

        Args:
            trade: Trade data
        """
        logger.debug("Processing trade update")
        await self.emit_event("trade", trade)

    async def process_account_update(
        self,
        account_data: Dict[str, Any]
    ) -> None:
        """
        Process account update event.

        Args:
            account_data: Account update data
        """
        logger.debug("Processing account update")
        await self.emit_event("account", account_data)

    async def emit_event(
        self,
        event_type: str,
        data: Dict[str, Any]
    ) -> None:
        """
        Emit an event to all registered handlers.

        Args:
            event_type: Type of event
            data: Event data
        """
        if event_type not in self.handlers:
            return

        # Call all handlers concurrently
        tasks = [
            handler(data)
            for handler in self.handlers[event_type]
        ]

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def start(self) -> None:
        """Start the event processor."""
        self.running = True
        logger.info("Event Processor started")

    async def stop(self) -> None:
        """Stop the event processor."""
        self.running = False
        logger.info("Event Processor stopped")
