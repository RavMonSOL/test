# OpenClaw Arena v0

A starter implementation of the paper-trading arena described in `PLATFORM_BLUEPRINT.md`.

## What is implemented

- Synthetic market with simple trend + volatility dynamics.
- Multiple autonomous agents that observe market snapshots and submit buy/sell/hold intents.
- Deterministic risk engine enforcing:
  - max position size,
  - max notional per trade,
  - no shorting,
  - minimum cash reserve.
- Epoch simulation loop with decision/action logs.
- Scoreboard with PnL and max drawdown.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python -m openclaw_arena.main --steps 50 --seed 7
```

## Run tests

```bash
pytest
```

## Next build targets

- Replace synthetic market with replayed historical snapshots.
- Add token launch proposal flow and policy checks.
- Stream logs to a persistent store for tournament analytics.
