# Execute — ai-sdlc-change-set: Isolated Change Workspace

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Read `references/change-set-contract.md` before creating or reviewing a
  workspace.
- Use `references/change-set.schema.toon` for the versioned machine contract.
- Use `scripts/change_set.py` for deterministic emit, create, and validation.
- Read `references/spec-delta-contract.md` before authoring or reviewing delta
  Markdown and use `references/spec-delta.schema.toon` for its projection.
- Use `scripts/spec_delta.py` to validate and project semantic deltas.
- Read `references/apply-preview-contract.md` before reviewing planned target
  changes and use `references/change-preview.schema.toon` for the projection.
- Use `scripts/change_preview.py` to compile diffs, conflicts, stale evidence,
  reopen actions, and required gates without target writes.
- Read `references/controlled-apply-contract.md` before applying or archiving.
- Validate approval with `references/change-approval.schema.toon` and recovery
  evidence with `references/change-recovery.schema.toon`.
- Use `scripts/change_apply.py` only after a ready preview and explicit approval.

## Script Usage

```bash
python3 skills/ai-sdlc-change-set/scripts/change_set.py . --change-id add-session-timeout --title "Add session timeout" --summary "Expire inactive sessions." --owner Security --target specs/auth/requirements.md --emit --quick-flow
python3 skills/ai-sdlc-change-set/scripts/change_set.py . --change-id add-session-timeout --title "Add session timeout" --summary "Expire inactive sessions." --owner Security --target specs/auth/requirements.md --create --full-flow
python3 skills/ai-sdlc-change-set/scripts/change_set.py . --change-id add-session-timeout --validate --format toon
python3 skills/ai-sdlc-change-set/scripts/spec_delta.py . --change-id add-session-timeout --validate --write --format toon
python3 skills/ai-sdlc-change-set/scripts/change_preview.py . --change-id add-session-timeout --preview --write --format toon
python3 skills/ai-sdlc-change-set/scripts/change_apply.py . --change-id add-session-timeout --apply --approval changes/add-session-timeout/evidence/owner-approval.toon --format toon
python3 skills/ai-sdlc-change-set/scripts/change_apply.py . --change-id add-session-timeout --archive --format toon
```

`--emit` renders the planned record without writes. `--create` builds the
workspace atomically and fails if it already exists. `--validate` verifies the
existing workspace and fingerprint.

## Purpose

Separate proposed change intent from current system truth so humans and AI can
review scope, ownership, targets, tasks, deltas, and evidence before any
canonical mutation is possible.

## Inputs

- Use a stable change ID that describes one bounded outcome.
- Use repository-relative POSIX paths for canonical targets.
- Use an accountable role or person as owner.
- Keep summary factual and state uncertainty in the proposal after creation.

## Steps

1. Inspect canonical sources read-only and identify their authority owners.
2. Run `--emit` to review the planned workspace and fingerprint.
3. Resolve unsafe IDs, paths, duplicate targets, or missing ownership.
4. Run `--create`; confirm canonical target bytes did not change.
5. Edit proposal sections through normal reviewed repository changes.
6. Run `--validate` before authoring semantic deltas.
7. Author delta Markdown with stable requirement IDs and operation-specific
   evidence, then run `spec_delta.py --validate`.
8. Compile preview and resolve every conflict, stale reference, reopen action,
   and required gate.
9. Obtain approval through an independently enforced repository or
   organizational control, then record its reference against the current
   preview fingerprint and every required gate. The local record validator does
   not authenticate the approver.
10. Apply through `change_apply.py`, inspect the completed recovery manifest,
    then archive the evidence-preserving workspace.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
