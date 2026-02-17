from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


@dataclass(slots=True)
class MarketState:
    step: int
    price: float
    momentum: float
    volatility: float


@dataclass(slots=True)
class AgentAction:
    agent_id: str
    side: Side
    quantity: float
    confidence: float
    rationale: str


@dataclass(slots=True)
class Portfolio:
    cash: float
    position: float = 0.0
    token_inventory: dict[str, float] = field(default_factory=dict)
    equity_curve: list[float] = field(default_factory=list)


@dataclass(slots=True)
class FillResult:
    accepted: bool
    reason: str
    filled_qty: float = 0.0
    notional: float = 0.0


@dataclass(slots=True)
class LaunchProposal:
    agent_id: str
    step: int
    ticker: str
    thesis: str
    initial_supply: int
    confidence: float


@dataclass(slots=True)
class TokenOrder:
    agent_id: str
    ticker: str
    side: Side
    quantity: float


@dataclass(slots=True)
class TokenFillResult:
    accepted: bool
    reason: str
    filled_base_qty: float = 0.0
    quote_delta: float = 0.0
    execution_price: float = 0.0
