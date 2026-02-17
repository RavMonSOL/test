from __future__ import annotations

from dataclasses import dataclass

from .agents import BaseAgent, MeanReversionAgent, MomentumAgent, NoiseSentimentAgent
from .launch import LaunchPolicyConfig, LaunchPolicyEngine
from .market_data import load_market_snapshots
from .models import AgentAction, Portfolio, Side
from .risk import RiskConfig, RiskEngine


@dataclass(slots=True)
class AgentContext:
    agent: BaseAgent
    portfolio: Portfolio


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


def run_simulation(steps: int = 100, seed: int = 1, snapshot_path: str | None = None) -> dict:
    snapshots = load_market_snapshots(steps=steps, snapshot_path=snapshot_path)
    if not snapshots:
        raise ValueError("No snapshots available for simulation")

    start_price = snapshots[0].price
    risk = RiskEngine(RiskConfig())
    launch_policy = LaunchPolicyEngine(LaunchPolicyConfig())

    agents: list[AgentContext] = [
        AgentContext(MomentumAgent("momentum-1", aggressiveness=1.2), Portfolio(cash=1000.0)),
        AgentContext(MeanReversionAgent("reverter-1", anchor_price=start_price), Portfolio(cash=1000.0)),
        AgentContext(NoiseSentimentAgent("sentiment-1", seed=seed + 42), Portfolio(cash=1000.0)),
    ]

    logs: list[dict] = []
    launch_logs: list[dict] = []
    launch_count: dict[str, int] = {ctx.agent.agent_id: 0 for ctx in agents}
    last_launch_step: dict[str, int | None] = {ctx.agent.agent_id: None for ctx in agents}
    price = start_price

    for state in snapshots:
        step = state.step
        price = state.price

        for ctx in agents:
            proposal = ctx.agent.propose_launch(state)
            if proposal is not None:
                approved, status = launch_policy.validate(
                    proposal,
                    launches_so_far=launch_count[ctx.agent.agent_id],
                    last_launch_step=last_launch_step[ctx.agent.agent_id],
                )
                if approved:
                    launch_count[ctx.agent.agent_id] += 1
                    last_launch_step[ctx.agent.agent_id] = step
                launch_logs.append(
                    {
                        "step": step,
                        "agent": proposal.agent_id,
                        "ticker": proposal.ticker,
                        "confidence": round(proposal.confidence, 4),
                        "initial_supply": proposal.initial_supply,
                        "status": status,
                    }
                )

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
                "launches_approved": launch_count[ctx.agent.agent_id],
            }
        )

    scoreboard.sort(key=lambda row: row["pnl"], reverse=True)
    return {
        "steps": len(snapshots),
        "seed": seed,
        "snapshot_source": snapshot_path or "package:data/historical_snapshots.csv",
        "final_price": round(price, 6),
        "scoreboard": scoreboard,
        "logs": logs,
        "launch_logs": launch_logs,
    }
