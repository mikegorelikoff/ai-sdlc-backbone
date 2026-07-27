# Execute — Guided Explore and Apply

> Selector: execute

## Entry

Enter only after Explore has no blockers and the accepted fingerprint still matches current evidence.

## Procedure

## Script Usage

```bash
python3 skills/ai-sdlc-flow/scripts/flow.py explore \
  --intent "<request>" --feature NNN-feature \
  [--role software-engineer] [--action implementation] --format markdown
```

After the contributor explicitly accepts the displayed JSON card, pass that
same saved card to the separate mutation command:

```bash
python3 skills/ai-sdlc-flow/scripts/flow.py apply \
  --card <accepted-card.json> --execute
```

Use `.agents/skills/` instead of `skills/` in a project-scoped installation.
Without `--execute`, Apply performs verification and reports the single action
it would start. `--execute` is an explicit mutation boundary.

## Existing Phase Guidance

# Execute

Read the active role contract, current traced task or artifact, and selector-approved references. Perform one bounded checkpoint and preserve human-readable code.

## Exit

Start at most one allow-listed lifecycle transition, then return control to the owning skill.
