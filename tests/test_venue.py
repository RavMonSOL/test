from openclaw_arena.models import Portfolio, Side, TokenOrder
from openclaw_arena.venue import TokenVenue


def test_venue_launch_and_price_moves_on_buy() -> None:
    venue = TokenVenue()
    ok, _ = venue.launch_token("META", creator="a1", initial_supply=1000, seed_price=1.0)
    assert ok

    portfolio = Portfolio(cash=200)
    before = venue.markets["META"].price
    fill = venue.process_order(TokenOrder(agent_id="a1", ticker="META", side=Side.BUY, quantity=100), portfolio)
    after = venue.markets["META"].price

    assert fill.accepted
    assert fill.filled_base_qty > 0
    assert after > before
    assert portfolio.token_inventory["META"] > 0


def test_cross_agent_inventory_independent() -> None:
    venue = TokenVenue()
    ok, _ = venue.launch_token("MOMO", creator="a1", initial_supply=500, seed_price=1.0)
    assert ok

    p1 = Portfolio(cash=100)
    p2 = Portfolio(cash=100)

    venue.process_order(TokenOrder(agent_id="a1", ticker="MOMO", side=Side.BUY, quantity=50), p1)
    venue.process_order(TokenOrder(agent_id="a2", ticker="MOMO", side=Side.BUY, quantity=30), p2)

    assert p1.token_inventory.get("MOMO", 0) != p2.token_inventory.get("MOMO", 0)
