# Validate and Handoff — ai-sdlc-workflow: Declarative Workflow Planning

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

The plan records every node as eligible, skipped, deferred, or blocked;
selected waves; explicit approvals; derived capabilities and side effects;
source fingerprints; and the embedded runtime plan.

Quality gate:

- Pass when the workflow is acyclic, every referenced skill graph validates,
  conditions are bounded, approval gates are satisfied, and the compiled run
  plan passes runtime validation.
- Fail closed on invalid workflow structure or ambiguous authority.

## Scope Boundary

- Do not execute workflow nodes.
- Do not grant capabilities, approvals, or concurrency implicitly.
- Do not mutate policy, feature state, runtime state, or canonical artifacts.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
