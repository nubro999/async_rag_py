"""Position model definitions."""

from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class PositionSide(str, Enum):
    """Position side enumeration."""

    LONG = "long"
    SHORT = "short"


class Position(BaseModel):
    """Position model."""

    position_id: str
    symbol: str
    side: PositionSide
    size: float = Field(gt=0)
    entry_price: float = Field(gt=0)
    current_price: float = Field(gt=0)
    leverage: int = Field(ge=1)
    stop_loss: Optional[float] = Field(default=None, gt=0)
    take_profit: Optional[float] = Field(default=None, gt=0)
    unrealized_pnl: float = 0.0
    realized_pnl: float = 0.0
    margin: float = Field(gt=0)
    liquidation_price: Optional[float] = None
    opened_at: datetime = Field(default_factory=datetime.now)
    closed_at: Optional[datetime] = None
    status: str = "open"

    class Config:
        """Pydantic config."""

        use_enum_values = True

    def update_pnl(self, current_price: float) -> None:
        """
        Update unrealized PnL based on current price.

        Args:
            current_price: Current market price
        """
        self.current_price = current_price

        if self.side == PositionSide.LONG:
            self.unrealized_pnl = (current_price - self.entry_price) * self.size
        else:
            self.unrealized_pnl = (self.entry_price - current_price) * self.size

    def get_pnl_percentage(self) -> float:
        """
        Get PnL as percentage of entry value.

        Returns:
            PnL percentage
        """
        entry_value = self.entry_price * self.size
        if entry_value == 0:
            return 0.0

        return (self.unrealized_pnl / entry_value) * 100

    def should_stop_loss(self) -> bool:
        """Check if position should be stopped out."""
        if not self.stop_loss:
            return False

        if self.side == PositionSide.LONG:
            return self.current_price <= self.stop_loss
        else:
            return self.current_price >= self.stop_loss

    def should_take_profit(self) -> bool:
        """Check if position should take profit."""
        if not self.take_profit:
            return False

        if self.side == PositionSide.LONG:
            return self.current_price >= self.take_profit
        else:
            return self.current_price <= self.take_profit
