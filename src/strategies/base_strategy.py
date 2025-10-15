"""Base strategy class for all trading strategies."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from loguru import logger


class BaseStrategy(ABC):
    """
    Abstract base class for trading strategies.
    All strategies should inherit from this class.
    """

    def __init__(self, name: str, parameters: Dict[str, Any]):
        """
        Initialize the strategy.

        Args:
            name: Strategy name
            parameters: Strategy parameters
        """
        self.name = name
        self.parameters = parameters
        self.enabled = True
        logger.info(f"Strategy initialized: {name}")

    @abstractmethod
    async def analyze(
        self,
        symbol: str,
        market_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze market data and generate trading signal.

        Args:
            symbol: Trading symbol
            market_data: Market data including price, volume, indicators

        Returns:
            Trading signal or None if no signal
        """
        pass

    @abstractmethod
    def validate_parameters(self) -> bool:
        """
        Validate strategy parameters.

        Returns:
            True if parameters are valid
        """
        pass

    def enable(self) -> None:
        """Enable the strategy."""
        self.enabled = True
        logger.info(f"Strategy enabled: {self.name}")

    def disable(self) -> None:
        """Disable the strategy."""
        self.enabled = False
        logger.info(f"Strategy disabled: {self.name}")

    def update_parameters(self, parameters: Dict[str, Any]) -> None:
        """
        Update strategy parameters.

        Args:
            parameters: New parameters
        """
        self.parameters.update(parameters)
        logger.info(f"Strategy parameters updated: {self.name}")
