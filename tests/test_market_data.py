from pathlib import Path

from openclaw_arena.market_data import load_market_snapshots


def test_load_market_snapshots_from_package_data() -> None:
    snapshots = load_market_snapshots(steps=5)

    assert len(snapshots) == 5
    assert snapshots[0].step == 1
    assert snapshots[0].price > 0


def test_load_market_snapshots_from_custom_file(tmp_path: Path) -> None:
    custom = tmp_path / "snapshots.csv"
    custom.write_text(
        "step,price,momentum,volatility\n"
        "10,1.01,0.01,0.02\n"
        "11,1.00,-0.01,0.03\n",
        encoding="utf-8",
    )

    snapshots = load_market_snapshots(steps=10, snapshot_path=str(custom))

    assert len(snapshots) == 2
    assert snapshots[0].step == 1
    assert snapshots[1].momentum == -0.01
