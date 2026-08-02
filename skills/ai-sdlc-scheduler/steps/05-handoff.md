# Handoff — AI SDLC Scheduler

## Entry

Validation completed or a terminal blocker was identified.

## Procedure

Return run ID, state path, revision, ready tasks, leases, terminal outcomes,
blockers, and the exact next claim, recovery, validation, or escalation action.

Emit an `ai-sdlc-handoff/v2` contract. Populate `result`, `blockers`,
`next_required`, and `next_optional`; every next action includes its reason,
command, expected artifact, and owner. Reference durable scheduler, runtime,
context, and effect evidence so the next owner can verify rather than trusting
chat history. Never call an unfinished or expired run complete.

## Examples

- Schedule two independent ready StepCards, dispatch them to different workers,
  recover one expired lease, and compare-commit both isolated runtime results.

## Edge Cases

- On revision contention, reload and retry selection. On dispatch interruption,
  retain the lease until explicit recovery. On terminal replay, reuse matching
  evidence and reject any changed result or effect identity.

## Exit

The next owner can continue without relying on chat history.
