# Execute — ai-sdlc-workflow: Declarative Workflow Planning

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Read `references/workflow-contract.md` before authoring or reviewing workflows.
- Validate definitions with `references/workflow.schema.json` and generated
  plans with `references/workflow-plan.schema.json`.
- Use `scripts/workflow.py` for validation and planning.

## Script Usage

```bash
python3 skills/ai-sdlc-workflow/scripts/workflow.py . --workflow workflow.json --validate --format toon
python3 skills/ai-sdlc-workflow/scripts/workflow.py . --workflow workflow.json --plan --context context.json --concurrency 4 --isolation-supported --write
```

## Purpose

Separate portable workflow semantics from host execution while preserving gates,
capability boundaries, deterministic hooks, and safe parallelism.

## Inputs

- Exact workflow identity and version.
- Declared capability set and typed steps.
- Optional bounded condition context.
- Explicit host concurrency and isolation support.

## Steps

1. Validate schema shape, IDs, actions, declared capabilities, and hook targets.
2. Detect dependency cycles before evaluating conditions.
3. Evaluate only `eq`, `in`, and `exists` conditions against explicit context.
4. Preserve approval steps as exclusive gates; never auto-satisfy them.
5. Build topological dependency waves from eligible steps.
6. Keep a parallel wave only for isolated task/validation steps when the host supports it.
7. Otherwise split deterministically into sequential waves and report exact fallbacks.
8. Emit complete TOON and optional JSON/Markdown projections without executing actions.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
