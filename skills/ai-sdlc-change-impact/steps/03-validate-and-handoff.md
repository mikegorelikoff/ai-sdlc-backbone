# Validate and Handoff — ai-sdlc-change-impact: Evidence-Backed Lifecycle Recovery

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

The TOON schema `ai-sdlc-change-impact/v1` contains changes, affected artifacts,
stage status, blockers, and actions with `stage`, `skill`, `action`, `reason`,
`evidence_path`, `evidence_line`, `changed_ref`, and `expected_artifact`.

Quality gate:

- Pass when every change has valid source evidence and every impact/action is
  backed by an exact downstream trace occurrence.
- Full flow fails when state is absent, source evidence is invalid, or an
  affected artifact cannot be mapped to a lifecycle owner.

## Examples

Valid change:

```json
{"id":"CHG-001","changed_ref":"AC-004","source":{"path":"requirements.md","line":121,"detail":"Retry behavior changed from optional to required."}}
```

Invalid counter-example: `The requirements changed recently.` It cannot prove
which durable source changed or which downstream artifacts are stale.

## Edge Cases

- A valid change with no downstream occurrence reports no stale artifact and
  recommends targeted trace review rather than broad reopening.
- Multiple occurrences in one artifact are collapsed into one affected row per
  changed reference using the earliest exact line as evidence.
- Unknown artifact owners block full flow but remain visible in quick flow.
- Already active stages are revalidated, never reopened concurrently.

## Scope Boundary

- Do not mutate lifecycle state, indexes, source artifacts, or policy.
- Do not reopen a stage solely because it follows another stage chronologically.
- Do not treat filename similarity or model intuition as impact evidence.
- Do not approve recovery actions on behalf of artifact owners.
- Use `$ai-sdlc-flow` Explore when the owning workflow is unclear.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
