"""Order model definitions."""

from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class OrderSide(str, Enum):
    """Order side enumeration."""

    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    """Order type enumeration."""

    MARKET = "market"
    LIMIT = "limit"
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"


class OrderStatus(str, Enum):
    """Order status enumeration."""

    PENDING = "pending"
    OPEN = "open"
    PARTIAL = "partial"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class Order(BaseModel):
    """Order model."""

    order_id: Optional[str] = None
    symbol: str
    side: OrderSide
    order_type: OrderType
    size: float = Field(gt=0)
    price: Optional[float] = Field(default=None, gt=0)
    stop_price: Optional[float] = Field(default=None, gt=0)
    leverage: int = Field(default=1, ge=1)
    status: OrderStatus = OrderStatus.PENDING
    filled_size: float = Field(default=0.0, ge=0)
    average_price: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    fee: float = 0.0

    class Config:
        """Pydantic config."""

        use_enum_values = True

    def is_filled(self) -> bool:
        """Check if order is fully filled."""
        return self.status == OrderStatus.FILLED

    def is_active(self) -> bool:
        """Check if order is active."""
        return self.status in [OrderStatus.PENDING, OrderStatus.OPEN, OrderStatus.PARTIAL]

    def filled_percentage(self) -> float:
        """Get filled percentage."""
        if self.size == 0:
            return 0.0
        return (self.filled_size / self.size) * 100
