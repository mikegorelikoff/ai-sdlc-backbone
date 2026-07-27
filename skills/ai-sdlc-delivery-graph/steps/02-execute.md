# Execute — ai-sdlc-delivery-graph: Repository Traceability

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Read `references/delivery-graph-contract.md` before interpreting nodes,
  edges, gaps, or query paths.
- Use `references/delivery-node.schema.json`,
  `references/delivery-edge.schema.json`, and
  `references/delivery-graph.schema.json` for machine contracts.
- Use `scripts/delivery_graph.py` for deterministic indexing and queries.
- Read `references/evidence-ledger-contract.md` before registering or judging
  evidence freshness. Validate inputs and outputs with
  `references/evidence-source.schema.json` and
  `references/evidence-ledger.schema.json`.
- Use `scripts/evidence_ledger.py` to recalculate current file identities,
  propagate stale state, and query fresh coverage.

## Script Usage

```bash
python3 skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py . --index --write --format toon --quick-flow
python3 skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py . --trace AC-004 --to T006 --format toon
python3 skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py . --gaps --format markdown
python3 skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py . --orphans --format toon
python3 skills/ai-sdlc-delivery-graph/scripts/evidence_ledger.py . --index --as-of 2026-07-19 --write --format toon
python3 skills/ai-sdlc-delivery-graph/scripts/evidence_ledger.py . --coverage --as-of 2026-07-19 --format toon
python3 skills/ai-sdlc-delivery-graph/scripts/evidence_ledger.py . --stale --as-of 2026-07-19 --format markdown
```

## Purpose

Make lifecycle traceability executable so reviewers can prove why work exists,
what verifies it, what shipped it, and where delivery evidence is missing.

## Inputs

- Stable trace identifiers in lifecycle Markdown.
- `Refs:` lines or co-located declaration references.
- Optional explicit `Component: <path> -> <trace-id>` and
  `Evidence: <path> -> <trace-id>` links.
- Conventional commit bodies containing `Spec:` and `Task:` and annotated Git
  tags for release nodes.

## Steps

1. Scan canonical lifecycle Markdown and hash every input file.
2. Scope declared and referenced trace IDs to their feature.
3. Add only evidence-backed semantic edges and Git task/release edges.
4. Normalize and fingerprint nodes, edges, sources, gaps, and coverage.
5. Inspect orphan and missing-coverage results.
6. Run trace queries using a scoped node ID when a short ID is ambiguous.
7. Write generated projections only when explicitly requested.
8. Register evidence with captured artifact and dependency hashes, expiry, and
   upstream evidence identities.
9. Rebuild the ledger for an explicit `as_of` date; resolve missing, changed,
   expired, unknown, ambiguous, or cyclic evidence before claiming coverage.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
