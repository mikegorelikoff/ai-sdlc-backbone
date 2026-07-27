# Execute — ai-sdlc-quality-lenses: Traceable Cross-Artifact Review

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Read `references/quality-lenses.json` to select applicable lenses.
- Read `references/finding-contract.md` before creating or changing findings.
- Use `scripts/quality_lens_report.py` to list lenses, validate findings, and
  emit or atomically write the canonical report pair.

## Script Usage

```bash
python3 skills/ai-sdlc-quality-lenses/scripts/quality_lens_report.py --list-lenses --format markdown
python3 skills/ai-sdlc-quality-lenses/scripts/quality_lens_report.py --artifact specs/example/requirements.md --artifact-kind requirements --feature example --findings /tmp/findings.json --lens edge-case-hunt --emit --quick-flow
python3 skills/ai-sdlc-quality-lenses/scripts/quality_lens_report.py --artifact specs/example/design.md --artifact-kind design --feature example --findings /tmp/findings.json --write --full-flow
```

`--emit` prints one format without writes. `--write` creates both canonical
formats. Invalid or incomplete findings exit non-zero and produce no files.

## Purpose

Turn reusable critical-thinking modes into consistent, portable review
evidence instead of one-off prose that loses ownership and traceability.

## Inputs

- Read the source artifact and its direct trace sources.
- Select lenses by applicability and review risk.
- Create a JSON array conforming to `references/finding-contract.md`.
- Anchor evidence to an exact repository-relative path and positive line.

## Steps

1. Inspect the registry and select applicable lenses.
2. Read the source artifact plus targeted requirement, decision, test, or task
   evidence needed by those lenses.
3. Apply each lens independently; distinguish observed evidence from impact.
4. Create findings with stable IDs and all required contract fields.
5. Run the finalizer with `--emit` and correct every validation error.
6. Run `--write` only after owners and trace targets are credible.
7. Route open findings to the owning skill; preserve accepted, mitigated,
   rejected, and deferred resolution states in later reviews.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
