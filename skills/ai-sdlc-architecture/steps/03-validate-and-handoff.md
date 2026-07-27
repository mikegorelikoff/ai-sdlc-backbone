# Validate and Handoff — ai-sdlc-architecture: Traceable System Design

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

`ai-sdlc-architecture/v1` contains context, constraints, components, interfaces,
decisions, risks, and validation checks with trace targets and owners.

Quality gate:

- Pass when boundaries are explicit and every material claim has traceability.
- Full flow fails without decisions, risks, validation, alternatives, consequences,
  risk ownership, or mitigation.

## Examples

A valid decision records `DEC-021`, its requirement traces, selected option,
rationale, alternatives, and operational consequences. “Use microservices
because they scale” is invalid without evidence, boundary, alternatives, or tradeoff.

## Edge Cases

- A local reversible patch may use quick flow and record no new decision.
- External systems remain components with explicit unverified interface assumptions.
- Existing ADRs are referenced, not duplicated.
- Diagram generation is optional; structured contracts remain authoritative.

## Scope Boundary

- Do not approve architecture on behalf of owners.
- Do not provision infrastructure or change production systems.
- Do not replace SDD requirements, tests, tasks, or decisions.
- Do not hide unresolved architecture risks.
- Use `$ai-sdlc-change-impact` when an accepted design changes downstream work.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
