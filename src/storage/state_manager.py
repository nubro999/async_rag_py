"""State manager for positions and orders tracking."""

from typing import Dict, Any, List, Optional
from loguru import logger


class StateManager:
    """
    Manages active positions tracking, order state,
    and configuration persistence.
    """

    def __init__(self, config: dict):
        """
        Initialize the state manager.

        Args:
            config: Configuration dict with storage settings
        """
        self.config = config
        self.positions: Dict[str, Dict[str, Any]] = {}
        self.orders: Dict[str, Dict[str, Any]] = {}
        self.bot_state: Dict[str, Any] = {}
        logger.info("State Manager initialized")

    async def save_position(
        self,
        position_id: str,
        position: Dict[str, Any]
    ) -> None:
        """
        Save or update a position.

        Args:
            position_id: Position identifier
            position: Position data
        """
        logger.debug(f"Saving position: {position_id}")
        self.positions[position_id] = position

        # TODO: Persist to storage (Redis/Database)

    async def get_position(
        self,
        position_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get a position by ID.

        Args:
            position_id: Position identifier

        Returns:
            Position data or None
        """
        return self.positions.get(position_id)

    async def get_open_positions(
        self,
        symbol: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all open positions, optionally filtered by symbol.

        Args:
            symbol: Optional symbol filter

        Returns:
            List of open positions
        """
        logger.debug(f"Getting open positions{f' for {symbol}' if symbol else ''}")

        positions = list(self.positions.values())

        if symbol:
            positions = [p for p in positions if p.get("symbol") == symbol]

        return [p for p in positions if p.get("status") == "open"]

    async def close_position(
        self,
        position_id: str
    ) -> bool:
        """
        Mark a position as closed.

        Args:
            position_id: Position identifier

        Returns:
            True if successful
        """
        if position_id in self.positions:
            self.positions[position_id]["status"] = "closed"
            logger.info(f"Position closed: {position_id}")
            return True

        return False

    async def update_order_status(
        self,
        order_id: str,
        status: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Update an order's status.

        Args:
            order_id: Order identifier
            status: New status
            details: Optional additional details
        """
        logger.debug(f"Updating order {order_id} status to {status}")

        if order_id not in self.orders:
            self.orders[order_id] = {}

        self.orders[order_id]["status"] = status

        if details:
            self.orders[order_id].update(details)

        # TODO: Persist to storage

    async def get_order(
        self,
        order_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get an order by ID.

        Args:
            order_id: Order identifier

        Returns:
            Order data or None
        """
        return self.orders.get(order_id)

    async def get_active_orders(self) -> List[Dict[str, Any]]:
        """
        Get all active orders.

        Returns:
            List of active orders
        """
        return [
            order for order in self.orders.values()
            if order.get("status") in ["pending", "open", "partial"]
        ]

    async def save_bot_state(
        self,
        key: str,
        value: Any
    ) -> None:
        """
        Save bot state data.

        Args:
            key: State key
            value: State value
        """
        self.bot_state[key] = value

        # TODO: Persist to storage

    async def get_bot_state(
        self,
        key: str,
        default: Any = None
    ) -> Any:
        """
        Get bot state data.

        Args:
            key: State key
            default: Default value if key not found

        Returns:
            State value or default
        """
        return self.bot_state.get(key, default)
