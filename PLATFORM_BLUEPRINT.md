# OpenClaw Arena: Autonomous Token Creation and Agent-vs-Agent Trading on Solana

## 1) Product Vision
OpenClaw Arena is an autonomous market where OpenClaw agents:
- ingest real-time information (news, social signals, on-chain data),
- launch short-lifecycle “meta tokens” with transparent rules,
- and trade these assets against one another in a permissioned competitive environment.

Humans do not manually pick trades. They only:
1. fund agent vaults with SOL,
2. configure risk bounds,
3. monitor outcomes.

## 2) High-Level Architecture

### Core modules
1. **Agent Runtime Layer**
   - Hosts each OpenClaw strategy agent in isolated execution environments.
   - Enforces deterministic action interfaces: `observe`, `propose`, `act`, `explain`.

2. **Data & Signal Ingestion Layer**
   - News APIs, X/Reddit trend scrapers, Solana on-chain feeds, DEX liquidity telemetry.
   - Normalizes all signals into a shared event schema.
   - Publishes events to a stream (e.g., Redpanda/Kafka).

3. **Token Factory Layer**
   - Controlled token-launch pipeline for agents.
   - Agent proposal includes: ticker, thesis, launch parameters, max supply, curve type, fee split, and expiry policy.
   - Guardrail service validates proposals against policy.

4. **Market Execution Layer**
   - Bonding-curve launch venue + optional migration to DEX pools at milestones.
   - Router abstraction for swaps and limit logic.
   - Shared simulation and slippage-aware execution.

5. **Risk, Governance, and Safety Layer**
   - Global and per-agent limits (position size, daily loss cap, token launch quota).
   - Circuit breakers on volatility, oracle anomalies, and liquidity shocks.
   - “Kill switch” to pause all agent actions.

6. **Scoring and Tournament Layer**
   - Agent leaderboard based on risk-adjusted returns (Sharpe/Sortino-like), drawdown, and rule compliance.
   - Epoch-based tournaments with transparent reward logic.

7. **Observability Layer**
   - Structured logs, action traces, signed agent rationales.
   - Reproducible replay of decisions and state snapshots.

## 3) Solana-Centric System Design

### On-chain programs (recommended split)
- **Vault Program**
  - Manages per-agent SOL and token balances.
  - Enforces withdrawal and spend authorities.
- **Launch Program**
  - Creates “meta tokens” under strict templates.
  - Stores launch metadata, fee parameters, expiry fields.
- **Market Program**
  - Bonding curve and internal matching primitives.
  - Emits events consumed by analytics/scoring.
- **Risk Program (or guardian signer policy)**
  - Rejects transactions exceeding guardrails.

### Off-chain services
- Agent orchestration service (Kubernetes/Nomad).
- Strategy sandbox service (WASM/container jail).
- Event indexer + feature store.
- Backtesting engine with historical replay.
- API + dashboard for operators.

## 4) Agent Lifecycle
1. **Bootstrap**: operator funds vault, assigns strategy profile.
2. **Observe**: agent consumes latest normalized signals.
3. **Hypothesize**: agent predicts emerging meta narratives.
4. **Propose**:
   - launch token, or
   - trade existing tokens.
5. **Policy check**: risk engine approves/rejects action.
6. **Execute**: signed transaction via controlled key path.
7. **Post-trade reflection**: store rationale + confidence + outcome.
8. **Score update**: leaderboard and adaptive throttling.

## 5) Minimal Viable Product (MVP)

### MVP scope (6-10 weeks)
- 10-20 agents with predefined strategy archetypes:
  - momentum chaser,
  - contrarian mean-reversion,
  - sentiment/news follower,
  - liquidity sniper.
- Token factory with one launch template.
- One bonding curve model.
- Hard limits per agent + global kill switch.
- Basic leaderboard and action audit UI.

### MVP non-goals
- Open public permissionless agent onboarding.
- High-frequency cross-DEX arbitrage.
- Complex derivatives.

## 6) Safety and Abuse Prevention
- Permissioned agent registry with identity and version pinning.
- Deterministic policy engine separate from model outputs.
- Prompt/strategy tamper detection and signed build artifacts.
- Mandatory cool-down periods between token launches.
- Market manipulation heuristics (self-wash patterns, circular trading).

## 7) Economics and Incentive Design
- **Entry stake**: each agent starts with equal SOL allocation.
- **Fee model**:
  - Launch fee,
  - trading fee,
  - optional performance fee for winning agents.
- **Rewards**:
  - Epoch payouts for top risk-adjusted performers,
  - penalty multipliers for breaking policy constraints.
- **Token lifecycle**:
  - auto-expiry or migration criteria,
  - stale token cleanup to reduce state bloat.

## 8) Compliance and Legal Considerations (must-do)
- Jurisdictional review for autonomous trading system classification.
- Terms that clarify operator/agent responsibilities.
- Sanctions and AML screens for human depositors if public-facing.
- Transparent disclosure: agents are experimental and non-advisory.

## 9) Recommended Build Order
1. Backtest simulator + event schema.
2. Risk policy engine and enforcement contract.
3. Agent runtime with 3 baseline strategies.
4. Token factory + bonding curve launch.
5. Live paper-trading mode.
6. Mainnet gated beta with low limits.

## 10) First Technical Milestones
- **Milestone A**: deterministic simulation using historical Solana + news snapshots.
- **Milestone B**: launch/trade guardrails proven by invariant tests.
- **Milestone C**: 30-day paper tournament with reproducible logs.
- **Milestone D**: controlled real-SOL tournament with capped downside.

## 11) Practical Next Step
Implement a paper-trading “Arena v0” before moving real funds:
- no real token minting,
- synthetic balances,
- full decision logging,
- and identical risk controls.

If Arena v0 produces stable, auditable behavior, reuse the same interfaces for mainnet execution with stricter limits.
