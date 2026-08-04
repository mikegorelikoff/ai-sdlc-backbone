---
name: ai-sdlc-doctor
description: AI SDLC installation diagnostics and safe upgrade planning. Use when an AI assistant needs to inspect harness prerequisites, repository layout, module and skill registration, detect actionable installation problems, compare versioned file inventories, preview additions/modifications/removals/schema migrations, or produce backup and rollback plans without applying an upgrade. Supports `--quick-flow` and `--full-flow`.
---

# ai-sdlc-doctor: Diagnostics And Safe Upgrade Plans

> Internal AI SDLC skill, not client-facing by default.
> Doctor and upgrade planning are read-only with respect to installation files.

## 0. Skill Card

- Skill name: `ai-sdlc-doctor`
- Primary audience: Dev, Delivery
- Supporting audience: Release, Architecture
- Audience tags: Dev, Delivery, Release, Architecture
- SDLC stage: Installation and upgrade operations
- Purpose: Explain installation health and upgrade impact before mutation.
- Output: `_ai_sdlc/doctor/report.toon` or `_ai_sdlc/upgrades/<id>/plan.toon`, with optional human Markdown

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
- In source use `skills/<skill>/...`; use `.agents/skills/<skill>/...` for
  Codex, `.claude/skills/<skill>/...` for Claude Code, or the project skills
  root recorded in `.ai-sdlc/harness-install.toon` for `agent-project`.
