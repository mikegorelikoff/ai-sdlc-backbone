# Validate and Handoff — ai-sdlc-host-adapter: Portable Host Negotiation

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

The negotiation records StepCard identity, native mapping, unsupported
operation, derived and missing capabilities, side effect, gates, outputs,
idempotency scope, requested and effective limits, fallbacks, compatibility,
reasons, and deterministic fingerprints.

Quality gate:

- Pass only when the StepCard operation has an equivalent mapping and every
  derived capability is declared by the adapter.
- Fail closed when host behavior would change workflow semantics.

## Scope Boundary

- Do not execute host operations, commands, or approvals.
- Do not claim capabilities not declared by the adapter.
- Do not silently drop workflow steps or required gates.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
