# Validate and Handoff — ai-sdlc-quality-lenses: Traceable Cross-Artifact Review

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

The TOON schema `ai-sdlc-quality-report/v1` contains registry version, artifact,
artifact kind, feature, flow mode, selected lenses, summary counts, and findings
with `id`, `lens`, `evidence_path`, `evidence_line`, `evidence_detail`,
`severity`, `trace_targets`, `owner`, `resolution_status`, and `next_action`.

Quality gate:

- Pass when every finding uses a registered selected lens and contains all
  required evidence, traceability, ownership, state, and action fields.
- Fail when evidence is vague, a trace target is empty, a status is unknown,
  a severity is invalid, or a selected lens is not registered/applicable.

## Examples

Valid finding:

```json
{"id":"QL-001","lens":"edge-case-hunt","evidence":{"path":"specs/payments/requirements.md","line":88,"detail":"Timeout behavior is unspecified"},"severity":"high","trace_targets":["AC-004","TC-012"],"owner":"BA","resolution_status":"open","next_action":"Define timeout and retry acceptance behavior."}
```

Invalid counter-example: `The design feels risky.` It has no exact evidence,
trace target, owner, status, or executable next action.

## Edge Cases

- An empty findings array is valid and explicitly reports zero findings.
- Full flow selects only lenses applicable to the declared artifact kind.
- A finding may trace to multiple requirement, test, task, risk, or decision
  identifiers; preserve them as slash-separated values in TOON.
- Rejected and deferred findings still retain evidence and next action so the
  decision remains auditable.

## Scope Boundary

- Do not edit the reviewed artifact as part of report finalization.
- Do not accept, reject, or defer findings without the accountable owner.
- Do not use generic model opinion as evidence.
- Do not advance lifecycle state or weaken protected rigor gates.
- Use `$ai-sdlc-flow` Explore when the owning remediation workflow is unclear.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
