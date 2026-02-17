from __future__ import annotations

import random
from dataclasses import dataclass

from .models import AgentAction, LaunchProposal, MarketState, Side


class BaseAgent:
    agent_id: str

    def act(self, state: MarketState) -> AgentAction:
        raise NotImplementedError

    def propose_launch(self, state: MarketState) -> LaunchProposal | None:
        return None


@dataclass(slots=True)
class MomentumAgent(BaseAgent):
    agent_id: str
    aggressiveness: float = 1.0

    def act(self, state: MarketState) -> AgentAction:
        if state.momentum > 0.001:
            qty = max(0.0, self.aggressiveness * state.momentum * 100)
            return AgentAction(self.agent_id, Side.BUY, qty, 0.7, "Positive momentum detected")
        if state.momentum < -0.001:
            qty = max(0.0, self.aggressiveness * abs(state.momentum) * 100)
            return AgentAction(self.agent_id, Side.SELL, qty, 0.7, "Negative momentum detected")
        return AgentAction(self.agent_id, Side.HOLD, 0.0, 0.3, "No clear momentum")

    def propose_launch(self, state: MarketState) -> LaunchProposal | None:
        if state.momentum > 0.009:
            return LaunchProposal(
                agent_id=self.agent_id,
                step=state.step,
                ticker="MOMO",
                thesis="Strong positive price impulse indicates short-lived momentum meta",
                initial_supply=250_000,
                confidence=0.74,
            )
        return None


@dataclass(slots=True)
class MeanReversionAgent(BaseAgent):
    agent_id: str
    anchor_price: float

    def act(self, state: MarketState) -> AgentAction:
        deviation = (state.price - self.anchor_price) / self.anchor_price
        if deviation > 0.03:
            return AgentAction(self.agent_id, Side.SELL, deviation * 50, 0.65, "Price above anchor; mean reversion short-bias")
        if deviation < -0.03:
            return AgentAction(self.agent_id, Side.BUY, abs(deviation) * 50, 0.65, "Price below anchor; mean reversion long-bias")
        return AgentAction(self.agent_id, Side.HOLD, 0.0, 0.35, "Price near anchor")


@dataclass(slots=True)
class NoiseSentimentAgent(BaseAgent):
    agent_id: str
    seed: int

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    def act(self, state: MarketState) -> AgentAction:
        sentiment = self._rng.uniform(-1, 1) + (state.momentum * 10)
        if sentiment > 0.5:
            return AgentAction(self.agent_id, Side.BUY, sentiment * 4, 0.55, "Synthetic sentiment bullish")
        if sentiment < -0.5:
            return AgentAction(self.agent_id, Side.SELL, abs(sentiment) * 4, 0.55, "Synthetic sentiment bearish")
        return AgentAction(self.agent_id, Side.HOLD, 0.0, 0.25, "Sentiment neutral")

    def propose_launch(self, state: MarketState) -> LaunchProposal | None:
        buzz = self._rng.uniform(0, 1) + abs(state.momentum)
        if buzz > 0.92:
            ticker = "META" if state.momentum >= 0 else "FADE"
            thesis = "Synthetic social buzz spike detected"
            return LaunchProposal(
                agent_id=self.agent_id,
                step=state.step,
                ticker=ticker,
                thesis=thesis,
                initial_supply=300_000,
                confidence=min(0.9, 0.6 + buzz / 3),
            )
        return None
