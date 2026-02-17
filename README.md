# OpenClaw Arena v0

A starter implementation of the paper-trading arena described in `PLATFORM_BLUEPRINT.md`.

## What is implemented

- Replayed market feed from historical snapshot CSV data.
- Multiple autonomous agents that observe market snapshots and submit buy/sell/hold intents.
- Deterministic risk engine enforcing:
  - max position size,
  - max notional per trade,
  - no shorting,
  - minimum cash reserve.
- Token launch proposal flow where agents can propose new meta tokens.
- Launch policy guardrails enforcing:
  - launch quota per agent,
  - minimum confidence,
  - ticker format,
  - max initial supply,
  - cooldown between launches.
- Epoch simulation loop with decision/action logs and launch approval/rejection logs.
- Scoreboard with PnL, max drawdown, and approved launch count.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python -m openclaw_arena.main --steps 50 --seed 7
```

Run using a custom snapshot file:

```bash
python -m openclaw_arena.main --steps 120 --snapshot-path ./path/to/snapshots.csv
```

Expected CSV columns:

- `step`
- `price`
- `momentum`
- `volatility`

## Run tests

```bash
pytest
```

## Next build targets

- Add cross-agent token inventory and venue-level pricing for launched tokens.
- Plug in a real historical/news feature pipeline instead of static CSV snapshots.
- Stream logs to a persistent store for tournament analytics.
