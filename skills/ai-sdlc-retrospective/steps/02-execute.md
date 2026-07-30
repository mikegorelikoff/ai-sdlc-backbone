# Execute — ai-sdlc-retrospective: Reviewable Delivery Learning

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Read `references/retrospective-contract.md` before preparing input.
- Use `scripts/retrospective.py` to validate separation, decision safety, and
  emit or atomically write the canonical report pair.

## Script Usage

```bash
python3 skills/ai-sdlc-retrospective/scripts/retrospective.py specs/payments --input /tmp/retro.toon --emit --quick-flow
python3 skills/ai-sdlc-retrospective/scripts/retrospective.py specs/payments --input /tmp/retro.toon --write --full-flow --format toon
```

The finalizer never writes any path named by a proposal `target`.

## Purpose

Create a durable learning loop where teams can improve the harness from real
delivery evidence without allowing an AI session to self-modify governance.

## Inputs

- Anchor observations to repository-relative files and positive line numbers.
- Reference proposals back to one or more observation IDs.
- Give every proposal a target, owner, review status, and next action.
- Add `decision_ref` only when a proposal has actually been accepted.

## Steps

1. Review delivery evidence, outcomes, friction, escapes, and effective controls.
2. Record observations without embedding recommended changes.
3. Draft proposals that cite observation IDs and identify target plus owner.
4. Validate evidence lines and governance statuses with the finalizer.
5. Review proposals with accountable owners and record durable decisions.
6. Regenerate the report when proposal status changes.
7. Route accepted work to SDD or the owning policy/configuration workflow.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
