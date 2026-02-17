from openclaw_arena.simulation import run_simulation


def test_simulation_produces_scoreboard() -> None:
    result = run_simulation(steps=10, seed=2)

    assert result["steps"] == 10
    assert len(result["scoreboard"]) == 3
    assert all("agent" in row and "pnl" in row for row in result["scoreboard"])
    assert all("launches_approved" in row for row in result["scoreboard"])
    assert len(result["logs"]) == 30  # 3 agents x 10 steps


def test_simulation_contains_launch_logs_key() -> None:
    result = run_simulation(steps=20, seed=7)

    assert "launch_logs" in result
    assert isinstance(result["launch_logs"], list)
