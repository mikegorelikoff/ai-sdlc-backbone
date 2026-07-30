<!-- public-docs-canonical: ../docs/index.md -->

> **Internal, non-canonical design note.** The maintained public documentation starts at [AI SDLC Harness docs](../docs/index.md). This file is retained for repository history and maintainer context only.

# Workflow Handoff Contract

Every AI SDLC workflow returns a normalized post-workflow handoff directly in
the assistant response. The contract separates what happened from what must or
may happen next.

Schema `ai-sdlc-handoff/v2` contains:

- `result`: `complete`, `partial`, or `blocked`;
- `summary`: concise outcome;
- `blockers`: explicit unresolved conditions;
- `next_required`: exactly one skill, reason, command, and expected artifact;
- `next_optional`: zero or more actions with the same fields.

Use `skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_handoff.py` to validate and render Markdown or TOON.
The emitter is read-only: the owning workflow completes artifacts and state
before producing its handoff. When the next required action is unclear, use
`ai-sdlc-flow` Explore and then emit the selected action.

Executable v4 handoffs also preserve the completed StepCard identity: owning
skill, semantic step ID, graph and step fingerprints, context decision,
operation, capabilities, side-effect class, gates, outputs, idempotency scope,
status, and evidence references. Flow, workflow, runtime, and host adapters must
not translate these fields into weaker local meanings.

After Apply, runtime records each owning-skill step in strict planned, started,
terminal, evidence, result order. A handoff may summarize that history, but the
canonical evidence remains the immutable plan and hash-chained
`journal/<sequence>.toon` events.
