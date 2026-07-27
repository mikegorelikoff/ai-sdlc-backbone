---
name: ai-sdlc-project-context
description: AI SDLC evidence-backed project context and bounded task-pack workflow. Use when an AI assistant needs to onboard to a repository, detect stack and commands, map ownership and test topology, check context drift, conditionally select task sources, exclude secrets, or allocate a freshness-aware context pack within an explicit token budget. Supports `--quick-flow` for focused evidence and `--full-flow` for stricter repository coverage.
---

# ai-sdlc-project-context: Evidence-Backed Repository Memory

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Confirm the repository root and output location before durable writes.
> Do not read, reproduce, or summarize secrets.

## 0. Skill Card

- Skill name: `ai-sdlc-project-context`
- Primary audience: Dev
- Supporting audience: QA, BA, Delivery, AI assistants
- Audience tags: Dev, QA, BA, Delivery
- SDLC stage: Cross-feature repository context
- Purpose: Generate durable repository memory and task-specific, bounded,
  freshness-aware context from explained safe sources.
- Output: `project-context.md`, `_ai_sdlc/project-context.toon`, and optional
  topology and task-pack records below `_ai_sdlc/context/`

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
