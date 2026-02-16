from __future__ import annotations

import random
from dataclasses import dataclass

from .agents import BaseAgent, MeanReversionAgent, MomentumAgent, NoiseSentimentAgent
from .models import AgentAction, MarketState, Portfolio, Side
from .risk import RiskConfig, RiskEngine


@dataclass(slots=True)
class AgentContext:
    agent: BaseAgent
    portfolio: Portfolio


def _next_market_state(step: int, prev_price: float, rng: random.Random) -> MarketState:
    drift = rng.uniform(-0.01, 0.01)
    shock = rng.gauss(0, 0.015)
    momentum = 0.6 * drift + 0.4 * shock
    price = max(0.1, prev_price * (1 + momentum))
    volatility = abs(shock)
    return MarketState(step=step, price=price, momentum=momentum, volatility=volatility)


def _apply_fill(action: AgentAction, portfolio: Portfolio, price: float, qty: float) -> None:
    if qty <= 0:
        return
    notional = qty * price
    if action.side is Side.BUY:
        portfolio.cash -= notional
        portfolio.position += qty
    elif action.side is Side.SELL:
        portfolio.cash += notional
        portfolio.position -= qty


def _equity(portfolio: Portfolio, price: float) -> float:
    return portfolio.cash + portfolio.position * price


def _max_drawdown(equity_curve: list[float]) -> float:
    if not equity_curve:
        return 0.0
    peak = equity_curve[0]
    max_dd = 0.0
    for value in equity_curve:
        peak = max(peak, value)
        dd = (peak - value) / peak if peak else 0.0
        max_dd = max(max_dd, dd)
    return max_dd


def run_simulation(steps: int = 100, seed: int = 1) -> dict:
    rng = random.Random(seed)
    start_price = 1.0
    risk = RiskEngine(RiskConfig())

    agents: list[AgentContext] = [
        AgentContext(MomentumAgent("momentum-1", aggressiveness=1.2), Portfolio(cash=1000.0)),
        AgentContext(MeanReversionAgent("reverter-1", anchor_price=start_price), Portfolio(cash=1000.0)),
        AgentContext(NoiseSentimentAgent("sentiment-1", seed=seed + 42), Portfolio(cash=1000.0)),
    ]

    logs: list[dict] = []
    price = start_price

    for step in range(1, steps + 1):
        state = _next_market_state(step, price, rng)
        price = state.price

        for ctx in agents:
            action = ctx.agent.act(state)
            fill = risk.validate(action, ctx.portfolio, state.price)
            if fill.accepted:
                _apply_fill(action, ctx.portfolio, state.price, fill.filled_qty)
            equity = _equity(ctx.portfolio, state.price)
            ctx.portfolio.equity_curve.append(equity)
            logs.append(
                {
                    "step": step,
                    "agent": action.agent_id,
                    "price": round(state.price, 6),
                    "momentum": round(state.momentum, 6),
                    "side": action.side.value,
                    "requested_qty": round(action.quantity, 4),
                    "filled_qty": round(fill.filled_qty, 4),
                    "status": fill.reason,
                    "cash": round(ctx.portfolio.cash, 4),
                    "position": round(ctx.portfolio.position, 4),
                    "equity": round(equity, 4),
                }
            )

    scoreboard = []
    for ctx in agents:
        final_equity = _equity(ctx.portfolio, price)
        pnl = final_equity - 1000.0
        scoreboard.append(
            {
                "agent": ctx.agent.agent_id,
                "final_equity": round(final_equity, 4),
                "pnl": round(pnl, 4),
                "max_drawdown": round(_max_drawdown(ctx.portfolio.equity_curve), 4),
            }
        )

    scoreboard.sort(key=lambda row: row["pnl"], reverse=True)
    return {
        "steps": steps,
        "seed": seed,
        "final_price": round(price, 6),
        "scoreboard": scoreboard,
        "logs": logs,
    }
