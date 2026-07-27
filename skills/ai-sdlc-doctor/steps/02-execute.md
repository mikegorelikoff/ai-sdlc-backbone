# Execute — ai-sdlc-doctor: Diagnostics And Safe Upgrade Plans

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Read `references/doctor-contract.md` before interpreting health or upgrade safety.
- Use `references/diagnostics.json` as the deterministic check registry.
- Validate inventories with `references/upgrade-inventory.schema.json`.
- Use `scripts/doctor.py` for all reports and plans.

## Script Usage

```bash
python3 skills/ai-sdlc-doctor/scripts/doctor.py . --doctor --write
python3 skills/ai-sdlc-doctor/scripts/doctor.py . --upgrade --current current.json --target target.json --upgrade-id v2-preview --write
```

## Purpose

Make operational gaps and upgrade risk reviewable before any installation mutation.

## Steps

1. Run registered prerequisite, layout, module, skill, and docs checks.
2. Report evidence and exact remediation without executing it.
3. Validate current and target inventories and API compatibility.
4. Diff files into add, modify, remove, unchanged, and schema-migration actions.
5. Plan backups for every modified or removed file.
6. Plan reverse-order rollback for every proposed change.
7. Emit TOON-first records; require a later authorized workflow to apply them.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
