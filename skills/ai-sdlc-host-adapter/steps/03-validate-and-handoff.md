# Validate and Handoff — ai-sdlc-host-adapter: Portable Host Negotiation

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

The negotiation records native and fallback mappings, unsupported operations,
missing capabilities, requested and effective limits, compatibility, reasons,
and deterministic fingerprints.

Quality gate:

- Pass only when every required operation and capability has an equivalent
  mapping or registered semantic-preserving fallback.
- Fail closed when host behavior would change workflow semantics.

## Scope Boundary

- Do not execute host operations, commands, hooks, or approvals.
- Do not claim capabilities not declared by the adapter.
- Do not silently drop workflow steps or required gates.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
