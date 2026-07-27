# Validate and Handoff — ai-sdlc-evidence-council: Authority-Safe Review Orchestration

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

`ai-sdlc-evidence-council/v1` contains topic, mode, authority, panel, evidence,
agreements, conflicts with positions, proposals, and unresolved questions.

Quality gate:

- Pass when mode is honest, every synthesis row cites registered evidence and
  reviewers, conflicts preserve positions, and actionable rows name owner/next action.
- Full flow fails below three reviewers, two roles, or one evidence anchor.

## Examples

Valid independent panel rows use three different `execution_id` values produced
by actual isolated runs. Three role labels generated in one response are valid
only as `simulated`, never `independent`.

## Edge Cases

- No consensus is a valid result; preserve owned unresolved questions.
- A reviewer may support one agreement and one side of a conflict.
- A proposal may be deferred or rejected but cannot be marked accepted by council.
- If independent execution fails midway, report partial/blocked rather than simulating missing votes.

## Scope Boundary

- Do not let reviewers edit authoritative artifacts, state, policy, or decisions.
- Do not claim reviewer independence without isolated executions.
- Do not convert majority opinion into acceptance authority.
- Do not hide conflicts, dissent, missing evidence, or unanswered questions.
- Use `$ai-sdlc-change-impact` after owners accept a proposal that changes delivery truth.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
