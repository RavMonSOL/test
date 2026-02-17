from __future__ import annotations

import argparse
import json

from .simulation import run_simulation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run OpenClaw Arena v0 simulation")
    parser.add_argument("--steps", type=int, default=100, help="Number of simulation steps")
    parser.add_argument("--seed", type=int, default=1, help="Random seed")
    parser.add_argument("--json", action="store_true", help="Print full JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_simulation(steps=args.steps, seed=args.seed)

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print(f"OpenClaw Arena v0 | steps={result['steps']} seed={result['seed']} final_price={result['final_price']}")
    print("\nScoreboard")
    for row in result["scoreboard"]:
        print(
            f"- {row['agent']}: pnl={row['pnl']:.4f} final_equity={row['final_equity']:.4f} "
            f"max_drawdown={row['max_drawdown']:.4f} launches={row['launches_approved']}"
        )


if __name__ == "__main__":
    main()
