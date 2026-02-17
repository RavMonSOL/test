from __future__ import annotations

import csv
from importlib import resources
from pathlib import Path

from .models import MarketState


def load_market_snapshots(steps: int, snapshot_path: str | None = None) -> list[MarketState]:
    if steps <= 0:
        return []

    if snapshot_path is None:
        with resources.files("openclaw_arena").joinpath("data/historical_snapshots.csv").open("r", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    else:
        with Path(snapshot_path).open("r", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))

    if not rows:
        raise ValueError("No market snapshots found")

    selected = rows[:steps]
    snapshots: list[MarketState] = []
    for idx, row in enumerate(selected, start=1):
        snapshots.append(
            MarketState(
                step=idx,
                price=float(row["price"]),
                momentum=float(row["momentum"]),
                volatility=float(row["volatility"]),
            )
        )
    return snapshots
