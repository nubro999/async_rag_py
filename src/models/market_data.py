"""Market data model definitions."""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Candle(BaseModel):
    """Candlestick data model."""

    symbol: str
    timeframe: str
    timestamp: datetime
    open: float = Field(gt=0)
    high: float = Field(gt=0)
    low: float = Field(gt=0)
    close: float = Field(gt=0)
    volume: float = Field(ge=0)

    def is_bullish(self) -> bool:
        """Check if candle is bullish."""
        return self.close > self.open

    def is_bearish(self) -> bool:
        """Check if candle is bearish."""
        return self.close < self.open

    def body_size(self) -> float:
        """Get candle body size."""
        return abs(self.close - self.open)

    def wick_size(self) -> tuple[float, float]:
        """Get upper and lower wick sizes."""
        upper_wick = self.high - max(self.open, self.close)
        lower_wick = min(self.open, self.close) - self.low
        return upper_wick, lower_wick


class OrderBookLevel(BaseModel):
    """Order book price level."""

    price: float = Field(gt=0)
    size: float = Field(gt=0)


class OrderBook(BaseModel):
    """Order book model."""

    symbol: str
    timestamp: datetime
    bids: List[OrderBookLevel] = Field(default_factory=list)
    asks: List[OrderBookLevel] = Field(default_factory=list)

    def get_best_bid(self) -> Optional[OrderBookLevel]:
        """Get best bid price and size."""
        return self.bids[0] if self.bids else None

    def get_best_ask(self) -> Optional[OrderBookLevel]:
        """Get best ask price and size."""
        return self.asks[0] if self.asks else None

    def get_spread(self) -> float:
        """Get bid-ask spread."""
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()

        if not best_bid or not best_ask:
            return 0.0

        return best_ask.price - best_bid.price

    def get_mid_price(self) -> Optional[float]:
        """Get mid-market price."""
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()

        if not best_bid or not best_ask:
            return None

        return (best_bid.price + best_ask.price) / 2


class Trade(BaseModel):
    """Trade model."""

    symbol: str
    trade_id: str
    timestamp: datetime
    price: float = Field(gt=0)
    size: float = Field(gt=0)
    side: str  # 'buy' or 'sell'

    def is_buy(self) -> bool:
        """Check if trade is a buy."""
        return self.side == "buy"

    def is_sell(self) -> bool:
        """Check if trade is a sell."""
        return self.side == "sell"
