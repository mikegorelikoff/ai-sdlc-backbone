# Validate and Handoff — ai-sdlc-change-set: Isolated Change Workspace

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

The `ai-sdlc-change-set/v1` record is written as complete TOON plus JSON and contains `change_id`, `title`,
`summary`, `status`, `owner`, `flow_mode`, dates, canonical targets, workspace
artifact paths, authority rules, and `contract_fingerprint`.

The `ai-sdlc-spec-delta/v1` TOON/JSON pair contains normalized operations, target
and source evidence, exact source hashes, and a deterministic fingerprint.

The `ai-sdlc-change-preview/v1` TOON/JSON pair contains virtual target hashes and
diffs, conservative conflicts, stale references, reopen actions, gates, and a
fingerprint that becomes invalid when any input drifts.

The JSON schemas `ai-sdlc-change-approval/v1` and
`ai-sdlc-change-recovery/v1` bind a structurally valid approval record to the
current preview and preserve transaction, backup, apply, and rollback evidence.
They do not authenticate the named owner or prove authorization. Branch
protection, CODEOWNERS review, a signed attestation, or another independently
enforced control must establish that authority before apply.

Quality gate:

- Pass when the workspace has every required artifact, the JSON record matches
  the schema, paths are safe and unique, headings and metadata are complete,
  and the fingerprint recomputes exactly.
- Fail when creation would overwrite a workspace, a target crosses a safety
  boundary, metadata and machine state disagree, or any required artifact is
  missing.

## Examples

Valid target: `specs/identity/requirements.md`.

Invalid counter-example: `../../policy.md`. Reject it because a change target
must remain repository-relative and cannot traverse outside the repository.

## Edge Cases

- A target may not exist yet when the proposal adds a new canonical artifact;
  record it explicitly and let delta validation decide whether `ADDED` is valid.
- Multiple targets are sorted for deterministic identity.
- Re-running `--create` never merges or replaces an existing workspace.
- A hand-edited record with a stale fingerprint fails validation.
- Empty delta and evidence indexes are valid at intake and become stricter in
  later lifecycle stages.
- Preview returns status `blocked` and exit code 2 for semantic conflicts while
  still emitting complete review evidence.
- Interrupted or failed multi-target apply uses the persisted recovery manifest
  to restore every already-replaced target before another attempt is accepted.

## Scope Boundary

- Do not treat valid requirement delta semantics as approval or compatibility.
- Never mutate a target outside the controlled apply command or without both an
  accepted, current, all-gates record and independently enforced human
  authorization.
- Do not compute downstream impact; use `$ai-sdlc-change-impact` and preview.
- Do not mutate canonical artifacts, policy, feature state, or specs indexes.
- This skill does not grant approval and does not merge, commit, or release a
  change. It validates record consistency, not external identity or authority;
  it may apply and archive only after the host organization enforces approval.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
