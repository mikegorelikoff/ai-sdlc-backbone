# Validate and Handoff — ai-sdlc-workflow: Declarative Workflow Planning

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

The plan records every step as eligible, skipped, or deferred; selected waves;
approval gates; hooks; fallback reason codes; source and plan fingerprints; and
explicit host capabilities.

Quality gate:

- Pass when the workflow is acyclic, capabilities are declared, conditions are
  bounded, hook targets resolve, and every planned parallel step is isolated.
- Fail closed on invalid workflow structure or ambiguous authority.

## Scope Boundary

- Do not execute workflow actions or hooks.
- Do not grant capabilities, approvals, isolation, or concurrency implicitly.
- Do not mutate policy, feature state, runtime state, or canonical artifacts.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
