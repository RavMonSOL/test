from openclaw_arena.simulation import run_simulation


def test_simulation_produces_scoreboard() -> None:
    result = run_simulation(steps=10, seed=2)

    assert result["steps"] == 10
    assert result["snapshot_source"] == "package:data/historical_snapshots.csv"
    assert len(result["scoreboard"]) == 3
    assert all("agent" in row and "pnl" in row for row in result["scoreboard"])
    assert all("launches_approved" in row for row in result["scoreboard"])
    assert all("token_inventory" in row for row in result["scoreboard"])
    assert len(result["logs"]) == 30  # 3 agents x 10 steps


def test_simulation_contains_launch_and_token_trade_logs() -> None:
    result = run_simulation(steps=20, seed=7)

    assert "launch_logs" in result
    assert "token_trade_logs" in result
    assert isinstance(result["launch_logs"], list)
    assert isinstance(result["token_trade_logs"], list)


def test_simulation_caps_to_available_snapshots() -> None:
    result = run_simulation(steps=1000, seed=7)

    assert result["steps"] == 300
    assert len(result["logs"]) == 900


def test_simulation_has_token_market_state() -> None:
    result = run_simulation(steps=60, seed=7)

    assert "token_markets" in result
    assert isinstance(result["token_markets"], dict)
