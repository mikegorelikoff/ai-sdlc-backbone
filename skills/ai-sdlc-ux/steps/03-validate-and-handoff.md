# Validate and Handoff — ai-sdlc-ux: Traceable Experience Specification

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

`ai-sdlc-ux/v1` contains context, actors, journeys, interaction states,
accessibility checks, content notes, and exact trace targets.

Quality gate:

- Pass when journey actors exist, steps and acceptance are observable, states
  include behavior plus recovery, and accessibility status has evidence.
- Full flow fails without journey, state, or accessibility coverage.

## Examples

A valid journey identifies actor `ACT-001`, ordered steps, `AC-012` traces, and
observable completion. “Make onboarding delightful” is invalid because it has
no actor, behavior, evidence, or testable outcome.

## Edge Cases

- One actor may have several journeys with different permissions or channels.
- A state may intentionally have no recovery; document the reason explicitly.
- Accessibility checks may be planned, passed, failed, or blocked.
- Visual references remain optional evidence and never replace behavior contracts.

## Scope Boundary

- Do not claim user validation without research evidence.
- Do not generate production UI code unless separately requested through SDD.
- Do not replace business rules, requirements, or test cases.
- Do not mark accessibility conformance from intent alone.
- Use `$ai-sdlc-change-impact` when accepted UX behavior invalidates downstream work.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
