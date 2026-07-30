# Validate and Handoff — ai-sdlc-retrospective: Reviewable Delivery Learning

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

The TOON schema `ai-sdlc-retrospective/v1` contains observations with exact
evidence and proposals with `based_on`, `target`, `change`, `owner`, `status`,
`decision_ref`, and `next_action`.

Quality gate:

- Pass when observations and proposals are separate, evidence is exact, every
  proposal traces to an observation, and accepted proposals cite a decision.
- Fail when a proposal is presented as an observation, approval is implied, or
  target policy content would be mutated by finalization.

## Examples

Valid accepted proposal:

```toon
based_on[1]: OBS-002
change: Add the deterministic retry fixture to standard validation.
decision_ref: DEC-014
id: PROP-001
next_action: Implement through a traced SDD task.
owner: Dev
status: accepted
target: skills/ai-sdlc-shared-runtime/scripts/validation-policy.toon
```

Invalid counter-example: `We learned that the policy should now skip tests.` It
mixes observation and policy mutation and has no evidence or decision.

## Edge Cases

- A retrospective with observations and no proposals is valid.
- Rejected proposals retain their evidence links and rationale in `next_action`.
- An accepted proposal without `decision_ref` always fails, including quick flow.
- A target may not exist yet; the report records it without creating it.

## Scope Boundary

- Do not edit policy, configuration, skill, or source targets.
- Do not accept proposals on behalf of owners.
- Do not turn anecdotes into observations without durable evidence.
- Do not advance feature lifecycle or hide failed proposals.
- Use `$ai-sdlc-flow` Explore to route accepted implementation work.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
