from __future__ import annotations

from dataclasses import dataclass

from .models import LaunchProposal


@dataclass(slots=True)
class LaunchPolicyConfig:
    max_launches_per_agent: int = 2
    min_confidence: float = 0.6
    max_initial_supply: int = 1_000_000
    cooldown_steps: int = 10


class LaunchPolicyEngine:
    def __init__(self, config: LaunchPolicyConfig) -> None:
        self.config = config

    def validate(
        self,
        proposal: LaunchProposal,
        launches_so_far: int,
        last_launch_step: int | None,
    ) -> tuple[bool, str]:
        if launches_so_far >= self.config.max_launches_per_agent:
            return False, "launch rejected: launch quota exceeded"

        if proposal.confidence < self.config.min_confidence:
            return False, "launch rejected: confidence below minimum"

        if proposal.initial_supply <= 0 or proposal.initial_supply > self.config.max_initial_supply:
            return False, "launch rejected: invalid initial supply"

        if not proposal.ticker.isalpha() or len(proposal.ticker) < 3 or len(proposal.ticker) > 8:
            return False, "launch rejected: invalid ticker format"

        if last_launch_step is not None and (proposal.step - last_launch_step) < self.config.cooldown_steps:
            return False, "launch rejected: cooldown active"

        return True, "launch approved"
