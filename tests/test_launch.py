from openclaw_arena.launch import LaunchPolicyConfig, LaunchPolicyEngine
from openclaw_arena.models import LaunchProposal


def test_launch_policy_rejects_quota_exceeded() -> None:
    engine = LaunchPolicyEngine(LaunchPolicyConfig(max_launches_per_agent=1))
    proposal = LaunchProposal(
        agent_id="a1",
        step=20,
        ticker="META",
        thesis="test",
        initial_supply=100_000,
        confidence=0.9,
    )

    approved, reason = engine.validate(proposal, launches_so_far=1, last_launch_step=5)

    assert not approved
    assert "quota" in reason


def test_launch_policy_rejects_cooldown() -> None:
    engine = LaunchPolicyEngine(LaunchPolicyConfig(cooldown_steps=10))
    proposal = LaunchProposal(
        agent_id="a1",
        step=12,
        ticker="META",
        thesis="test",
        initial_supply=100_000,
        confidence=0.9,
    )

    approved, reason = engine.validate(proposal, launches_so_far=0, last_launch_step=8)

    assert not approved
    assert "cooldown" in reason
