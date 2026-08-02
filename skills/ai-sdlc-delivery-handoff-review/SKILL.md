---
name: ai-sdlc-delivery-handoff-review
description: Use after story and spec synthesis to perform a strict delivery handoff review, identify remaining gaps or contradictions, and score readiness for engineering and cross-functional execution. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.
---

# ai-sdlc-delivery-handoff-review: Delivery Handoff Review

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-delivery-handoff-review`
- Primary audience: Delivery
- Supporting audience: PM, BA, QA, Dev Lead
- Audience tags: PM, BA, QA, Dev
- SDLC stage: Engineering handoff quality gate
- Purpose: Run the final quality gate on the delivery package before it is treated as ready for implementation planning or handoff.
- Output: Handoff readiness score, remaining blockers, contradictions, and execution risks

## Step Selector

This table is generated from `steps/manifest.toon`. The manifest and linked
step documents are canonical; regenerate this projection after graph changes.

| Step | Ready when | Depends on | Operation | Load |
| --- | --- | --- | --- | --- |
| `preflight` | `prepare` | none | `inspect-and-route` | [`steps/01-prepare.md`](steps/01-prepare.md) — `required` |
| `context` | `clarify`, `route` | `preflight` | `compile-context` | [`steps/02-context.md`](steps/02-context.md) — `required` |
| `execute` | `execute` | `context` | `execute-procedure` | [`steps/02-execute.md`](steps/02-execute.md) — `on-demand` |
| `validate` | `validate` | `execute` | `validate-evidence` | [`steps/03-validate-and-handoff.md`](steps/03-validate-and-handoff.md) — `before-completion` |
| `handoff` | `handoff`, `complete` | `validate` | `handoff-result` | [`steps/04-handoff.md`](steps/04-handoff.md) — `before-completion` |

## Progressive Disclosure Contract

- Resolve the phase entrypoint and dependency-ready set with
  `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`; never invent a step path.
- Read only the emitted StepCard and its selected context. Pass completed step
  IDs back to the selector before requesting the next ready node.
- Treat `direct_read` as an explicit context strategy. Block only when mandatory
  evidence or critical anchors are missing.
- Explore is read-only. After Apply, journal every selected owning-skill step,
  including analysis and validation nodes, before advancing the graph.
- In a source checkout use `skills/<skill>/...`; in a Codex project install
  use `.agents/skills/<skill>/...`, and in a Claude Code project install use
  `.claude/skills/<skill>/...`.
