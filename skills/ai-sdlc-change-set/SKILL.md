---
name: ai-sdlc-change-set
description: AI SDLC controlled change-workspace and specification-delta workflow. Use when an AI assistant needs to create or validate an isolated proposal workspace, author and validate requirement deltas, preview canonical changes, or apply and archive an explicitly approved change with rollback evidence. Supports `--quick-flow` for assumption-driven drafts and `--full-flow` for strict owner, target, evidence, and authority checks.
---

# ai-sdlc-change-set: Isolated Change Workspace

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> A change workspace proposes intent; it never becomes canonical truth by itself.

## 0. Skill Card

- Skill name: `ai-sdlc-change-set`
- Primary audience: Delivery, Dev, BA
- Supporting audience: PM, QA, Architecture, Security
- Audience tags: Delivery, Dev, BA, PM, QA
- SDLC stage: Controlled change intake
- Purpose: Create and validate an isolated, reviewable workspace before any
  authoritative specification mutation.
- Output: `changes/<change-id>/` with proposal, design, tasks, delta and
  evidence indexes, lifecycle records, preview, approval, and recovery evidence

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
