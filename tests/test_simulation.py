from openclaw_arena.simulation import run_simulation


def test_simulation_produces_scoreboard() -> None:
    result = run_simulation(steps=10, seed=2)

    assert result["steps"] == 10
    assert len(result["scoreboard"]) == 3
    assert all("agent" in row and "pnl" in row for row in result["scoreboard"])
    assert len(result["logs"]) == 30  # 3 agents x 10 steps
