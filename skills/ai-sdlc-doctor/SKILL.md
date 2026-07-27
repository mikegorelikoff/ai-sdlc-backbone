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
- Output: `_ai_sdlc/doctor/report.{toon,json,md}` or `_ai_sdlc/upgrades/<id>/plan.{toon,json,md}`

## Step Selector

Read `steps/manifest.json` and load only the step selected for the current phase, active role, and action. Treat every selected step as normative.

| Selector | Read when | Step | Load rule |
| --- | --- | --- | --- |
| `prepare` | `prepare`, `clarify`, `route` | [`steps/01-prepare.md`](steps/01-prepare.md) | `required` |
| `execute` | `execute` | [`steps/02-execute.md`](steps/02-execute.md) | `on-demand` |
| `validate-and-handoff` | `validate`, `handoff`, `complete` | [`steps/03-validate-and-handoff.md`](steps/03-validate-and-handoff.md) | `before-completion` |

## Progressive Disclosure Contract

- Read the manifest's required entry selector (`prepare`, or `clarify`/`route` for guided flow) before any command, durable write, or lifecycle transition.
- Read an `execute` selector only when performing the selected skill work.
- Read a `validate`, `handoff`, or `complete` selector before reporting completion.
- Do not broad-load unselected steps. If selectors return no match or a validation error, stop and report the blocker.
- Resolve selectors with the canonical `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`; never invent a step path.
- In a source checkout use `skills/<skill>/...`; in a consumer install use `.agents/skills/<skill>/...`.
