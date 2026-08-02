---
name: ai-sdlc-retrospective
description: AI SDLC evidence-backed retrospective workflow. Use when delivery work is complete or paused and an AI assistant needs to capture observations, connect them to validation or artifact evidence, formulate reviewable process or policy improvement proposals, assign ownership, and preserve the rule that policy changes require an accepted decision. Supports `--quick-flow` for focused learning and `--full-flow` for strict evidence and decision gates.
---

# ai-sdlc-retrospective: Reviewable Delivery Learning

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Retrospectives propose improvements; they never silently change policy.

## 0. Skill Card

- Skill name: `ai-sdlc-retrospective`
- Primary audience: Delivery, Dev, QA, BA
- Supporting audience: PM, platform maintainers
- Audience tags: Delivery, Dev, QA, BA, PM
- SDLC stage: Post-delivery learning
- Purpose: Separate evidence-backed observations from governed improvements.
- Output: `retrospective.md` and `_ai_sdlc/retrospective.toon`

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
