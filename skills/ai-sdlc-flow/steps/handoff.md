# Handoff — Guided Explore and Apply

> Selector: handoff

## Entry

Use when requested and owning roles differ or one bounded checkpoint has finished.

## Procedure

### 0.3 Output Rules

- Return the decision card, blockers, action result, and evidence directly in
  the Codex response.
- Return progress, blockers, and completion directly in the active agent response.
- Emit `ai-sdlc-handoff/v1` with `result`, `blockers`, `next_required`, and
  `next_optional`; each action includes reason, command, and expected artifact.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary.

## Existing Phase Guidance

# Handoff

State the current owner, next owner, reason, completed evidence, unresolved decisions, and exact next action. A handoff cannot bypass a state prerequisite.

## Exit

Name the reason, evidence, next owner, and required next step without activating two roles.
