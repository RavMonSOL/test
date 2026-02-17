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
- **Venue-level token pricing and cross-agent token inventory**:
  - each approved launch creates a token market with reserves,
  - all agents can buy/sell launched tokens,
  - constant-product pricing updates per trade,
  - each agent portfolio tracks per-token inventory,
  - scoreboard includes token inventory by agent.
- Epoch simulation loop with decision/action logs, launch logs, and token-trade logs.

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

- Add per-token risk limits (max exposure per agent/token).
- Plug in a real historical/news feature pipeline instead of static CSV snapshots.
- Stream logs to a persistent store for tournament analytics.
