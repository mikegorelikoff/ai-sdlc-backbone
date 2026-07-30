# Validate and Handoff — ai-sdlc-delivery-graph: Repository Traceability

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

The graph contains sorted nodes, edges, gaps, orphans, coverage counters, source
hashes, and fingerprints. Rebuilding identical inputs produces byte-identical
TOON, TOON, and Markdown. `requirement_declarations` inventories FR, NFR, AC,
REQ, story, workflow, and rule nodes. Actionable missing-task/test gaps and
coverage counters apply only to explicitly declared leaf `AC-###` nodes because
SDD tasks and tests trace acceptance criteria. Inferred references and parent requirements remain visible for explicit
paths and orphan review rather than inflating leaf coverage.

The canonical TOON evidence ledger contains recalculated file identities, resolved subjects,
freshness states, reason codes, upstream state, stale paths, and fresh-only
requirement coverage.

Quality gate:

- Pass when all node and edge evidence resolves, identities are unambiguous,
  fingerprints recompute, and required coverage gaps are understood.
- Fail when an explicit query is absent or ambiguous, an edge endpoint is
  missing, or generated output drifts from current authoritative inputs.

## Examples

`TC-004 / AC-004` declares a test and creates a `verifies` edge to the
acceptance criterion. A following `Refs: AC-004` under `T006` creates a task
`traces-to` edge. A commit with `Task: T006` creates an `implements` edge.

## Edge Cases

- The same `AC-001` in two features is two nodes and requires a scoped query.
- A reference without a local declaration still becomes a placeholder node and
  is reported as an orphan or coverage gap.
- Git-less fixture directories still produce valid lifecycle graphs.
- Generated graph files never become their own inputs.
- Evidence dependency cycles, duplicate IDs, ambiguous subjects, and unknown
  upstream evidence fail closed.

## Scope Boundary

- Do not infer semantic similarity, ownership, or policy decisions.
- Do not mark evidence fresh without matching current hashes, expiry, and all
  upstream evidence states.
- Do not edit lifecycle artifacts to make a graph appear complete.
- Do not treat graph generation as approval, validation evidence, or release.
- Do not overwrite producer manifests or evidence artifacts during indexing.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
