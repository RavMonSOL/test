from __future__ import annotations

from dataclasses import dataclass

from .models import AgentAction, FillResult, Portfolio, Side


@dataclass(slots=True)
class RiskConfig:
    max_position: float = 100.0
    max_trade_notional: float = 500.0
    min_cash_reserve: float = 50.0


class RiskEngine:
    def __init__(self, config: RiskConfig) -> None:
        self.config = config

    def validate(self, action: AgentAction, portfolio: Portfolio, price: float) -> FillResult:
        if action.side is Side.HOLD or action.quantity <= 0:
            return FillResult(True, "hold", 0.0, 0.0)

        requested_notional = action.quantity * price
        if requested_notional > self.config.max_trade_notional:
            max_qty = self.config.max_trade_notional / price
        else:
            max_qty = action.quantity

        if action.side is Side.BUY:
            max_cash_qty = max(0.0, (portfolio.cash - self.config.min_cash_reserve) / price)
            allowed_qty = min(max_qty, max_cash_qty, self.config.max_position - portfolio.position)
            if allowed_qty <= 0:
                return FillResult(False, "buy rejected by cash/position limits")
            return FillResult(True, "buy allowed", allowed_qty, allowed_qty * price)

        # SELL path: no shorting
        allowed_qty = min(max_qty, portfolio.position)
        if allowed_qty <= 0:
            return FillResult(False, "sell rejected (no inventory)")
        return FillResult(True, "sell allowed", allowed_qty, allowed_qty * price)
