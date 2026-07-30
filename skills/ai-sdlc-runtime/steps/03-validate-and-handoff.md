# Validate and Handoff — ai-sdlc-runtime: Resumable Delivery Runs

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

The hash-chained `journal/*.toon` event files store contiguous sequence numbers
and transition payloads. `state.toon` exposes plan identity, task protocol
phases and attempts, running and ready tasks, budgets, stop reason, sequence,
and fingerprint. Replay must reproduce that projection from immutable
`plan.toon` plus the journal.

Quality gate:

- Pass when journal chain and replay are valid, dependencies are satisfied,
  budgets remain, outcome evidence is complete, and commit-boundary tasks carry
  commit identity.
- Fail when a transition duplicates work, skips dependencies, exceeds a hard
  boundary, omits evidence, or conflicts with journal history.

## Examples

A repeated `--next` after T001 was claimed returns T001 with `idempotent: true`
and does not increase attempts or journal sequence. A repeated identical success
record also returns the existing outcome without another event.

## Edge Cases

- Corrupt or missing summarized state is repaired from a valid journal.
- A journal sequence gap, hash mismatch, or invalid transition fails recovery.
- Retry exhaustion and each budget type have distinct stop reasons.
- A commit-boundary task cannot succeed with a missing or malformed commit SHA.

## Scope Boundary

- Do not execute task commands, create commits, satisfy gates, or approve work.
- Do not edit journal lines, plan identity, attempts, budgets, or fingerprints manually.
- Do not run two mutating runtime commands concurrently for one run.
- Declarative workflow steps and host execution belong to later workflow and adapter layers.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
