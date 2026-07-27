---
name: ai-sdlc-workflow
description: AI SDLC declarative workflow planning. Use when an AI assistant needs to validate a versioned workflow, plan typed dependency steps, evaluate bounded conditions, enforce approval gates, attach deterministic hooks, detect cycles, or create safe dependency waves with sequential fallback when host concurrency or isolation is unavailable. Supports `--quick-flow` and `--full-flow`.
---

# ai-sdlc-workflow: Declarative Workflow Planning

> Internal AI SDLC skill, not client-facing by default.
> Planning never executes actions, hooks, approvals, or shell commands.

## 0. Skill Card

- Skill name: `ai-sdlc-workflow`
- Primary audience: Delivery, Dev
- Supporting audience: QA, Security, Architecture
- Audience tags: Delivery, Dev, QA, Security
- SDLC stage: Controlled execution planning
- Purpose: Compile portable workflow intent into deterministic, gated, host-safe waves.
- Output: `_ai_sdlc/workflows/<workflow-id>/plan.{toon,json,md}`

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
