from openclaw_arena.models import AgentAction, Portfolio, Side
from openclaw_arena.risk import RiskConfig, RiskEngine


def test_buy_respects_cash_and_reserve() -> None:
    engine = RiskEngine(RiskConfig(max_position=100, max_trade_notional=500, min_cash_reserve=50))
    portfolio = Portfolio(cash=100, position=0)
    action = AgentAction(agent_id="a", side=Side.BUY, quantity=100, confidence=1.0, rationale="test")

    result = engine.validate(action, portfolio, price=10)

    assert result.accepted
    assert result.filled_qty == 5  # (100 - 50) / 10


def test_sell_rejected_without_inventory() -> None:
    engine = RiskEngine(RiskConfig())
    portfolio = Portfolio(cash=1000, position=0)
    action = AgentAction(agent_id="a", side=Side.SELL, quantity=1, confidence=1.0, rationale="test")

    result = engine.validate(action, portfolio, price=1)

    assert not result.accepted
