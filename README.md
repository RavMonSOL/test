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

## Run tests

```bash
pytest
```

## Next build targets

- Replace synthetic market with replayed historical snapshots.
- Add cross-agent token inventory and venue-level pricing for launched tokens.
- Stream logs to a persistent store for tournament analytics.
