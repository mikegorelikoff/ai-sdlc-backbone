# Execute — ai-sdlc-change-impact: Evidence-Backed Lifecycle Recovery

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Read `references/change-set-contract.md` before preparing change evidence.
- Use `scripts/change_impact.py` for deterministic trace scanning, stage
  mapping, validation, and canonical report generation.

## Script Usage

```bash
python3 skills/ai-sdlc-change-impact/scripts/change_impact.py specs/payments --changes /tmp/changes.json --emit --quick-flow
python3 skills/ai-sdlc-change-impact/scripts/change_impact.py specs/payments --changes /tmp/changes.json --write --full-flow --format toon
python3 skills/ai-sdlc-change-impact/scripts/change_impact.py specs/payments --changes /tmp/changes.json --state-check --format toon
```

The change set is read-only input. `--write` atomically creates both report
formats after all evidence gates pass.

## Purpose

Make late change recovery explicit and bounded so teams update the smallest
credible lifecycle surface instead of either ignoring drift or restarting all
delivery work.

## Inputs

- Use repository-relative source evidence with a positive line number.
- Use stable trace IDs already present in source and downstream artifacts.
- Read state status and artifact ownership from canonical repository records.
- Exclude generated change-impact reports from their own analysis.

## Steps

1. Record each changed reference and exact changed-source evidence.
2. Validate that the source path is inside the feature and the evidence line
   contains the changed reference.
3. Scan feature Markdown for exact downstream trace occurrences.
4. Map affected artifacts to lifecycle skills and stages using metadata.
5. Classify the safe action from current state: reopen complete work,
   revalidate active work, or add a pre-start validation gate.
6. Order actions by canonical lifecycle stage order and retain all evidence.
7. Emit or write the analysis, then hand approved actions to owning skills.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
