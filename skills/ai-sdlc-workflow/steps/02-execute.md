# Execute — ai-sdlc-workflow: Declarative Workflow Planning

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Read `references/workflow-contract.md` before authoring or reviewing workflows.
- Validate definitions with `references/workflow.schema.toon` and generated
  plans with `references/workflow-plan.schema.toon`.
- Use `scripts/workflow.py` for validation and planning.

## Script Usage

```bash
python3 skills/ai-sdlc-workflow/scripts/workflow.py . --workflow workflow.toon --validate --format toon
python3 skills/ai-sdlc-workflow/scripts/workflow.py . --workflow workflow.toon --plan --context context.toon --concurrency 4 --approved-node release --write
```

## Purpose

Separate portable workflow semantics from execution while preserving canonical
skill graphs, approval boundaries, dependencies, and deterministic waves.

## Inputs

- Exact workflow identity and version.
- Canonical skill, entrypoint, role, and action for each node.
- Optional bounded condition context.
- Requested planning concurrency and explicit approved node IDs.

## Steps

1. Validate schema shape, IDs, skill entrypoints, roles, actions, and approval owners.
2. Detect dependency cycles before evaluating conditions.
3. Evaluate only `eq`, `in`, and `exists` conditions against explicit context.
4. Block approval-owned nodes until their exact node IDs are approved.
5. Compile each eligible node from its canonical skill graph and StepCard data.
6. Prefix task IDs and connect dependency-node terminal tasks.
7. Build bounded topological waves and one runtime-compatible v2 run plan.
8. Emit canonical TOON plus the human plan without executing skill steps.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
