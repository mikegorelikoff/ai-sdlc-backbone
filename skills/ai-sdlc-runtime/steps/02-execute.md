# Execute — ai-sdlc-runtime: Resumable Delivery Runs

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Read `references/runtime-contract.md` before starting, resuming, retrying, or
  recording a run.
- Validate plans with `references/run-plan.schema.toon`, events with
  `references/run-event.schema.toon`, and state with
  `references/run-state.schema.toon`.
- Use `scripts/runtime.py` for every state mutation and recovery operation.

## Script Usage

```bash
python3 skills/ai-sdlc-runtime/scripts/runtime.py . --start --run-id delivery-004 --plan run-plan.toon --format toon
python3 skills/ai-sdlc-runtime/scripts/runtime.py . --next --run-id delivery-004 --format toon
python3 skills/ai-sdlc-runtime/scripts/runtime.py . --record --run-id delivery-004 --task T001 --outcome succeeded --result-fingerprint <sha256> --tokens 420 --commit <sha>
python3 skills/ai-sdlc-runtime/scripts/runtime.py . --resume --run-id delivery-004 --format toon
```

## Purpose

Make long-running delivery resumable, bounded, and auditable without coupling
the durable task state to one agent host or chat session.

## Inputs

- Immutable plan identity and ordered task IDs with dependencies.
- Per-task maximum attempts and commit-boundary requirement.
- Run-level maximum task starts, failures, and recorded tokens.
- Exact outcome evidence for each started task.

## Steps

1. Validate plan identity, unique tasks, dependency existence, and acyclicity.
2. Start one atomically created run workspace.
3. Call `--next`; repeated calls return the same running task without another event.
4. Execute the task through the owning host and workflow.
5. Record succeeded, failed, or blocked with exact evidence and resource use.
6. Let retryable failures return to pending; inspect terminal retry or budget stops.
7. Use `--retry` only for an eligible blocked or failed task after its cause is resolved.
8. Use `--resume` to replay and hash-check the journal and repair stale state.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
