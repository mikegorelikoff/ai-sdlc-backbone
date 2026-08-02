---
name: ai-sdlc-workflow
description: AI SDLC declarative workflow planning. Use when an AI assistant needs to validate a versioned workflow of canonical skill entrypoints, evaluate bounded conditions, enforce explicit approval owners, detect dependency cycles, compile deterministic waves, or produce one runtime-compatible run plan without executing it. Supports `--quick-flow` and `--full-flow`.
---

# ai-sdlc-workflow: Declarative Workflow Planning

> Internal AI SDLC skill, not client-facing by default.
> Planning never executes skill steps, approvals, or shell commands.

## 0. Skill Card

- Skill name: `ai-sdlc-workflow`
- Primary audience: Delivery, Dev
- Supporting audience: QA, Security, Architecture
- Audience tags: Delivery, Dev, QA, Security
- SDLC stage: Controlled execution planning
- Purpose: Compile portable workflow intent into deterministic, gated skill
  waves and one immutable runtime plan.
- Output: `workflow-plan.toon`, `run-plan.toon`, and `plan.md` below
  `_ai_sdlc/workflows/<workflow-id>/`

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
