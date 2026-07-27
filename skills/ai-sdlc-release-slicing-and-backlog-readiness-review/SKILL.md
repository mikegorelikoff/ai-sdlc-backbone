---
name: ai-sdlc-release-slicing-and-backlog-readiness-review
description: Use after backlog decomposition to define prioritization, MVP and release slices, sequencing, readiness, traceability, and JIRA-ready outputs, then score backlog quality for planning and estimation. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.
---

# ai-sdlc-release-slicing-and-backlog-readiness-review: Release Slicing And Backlog Readiness Review

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-release-slicing-and-backlog-readiness-review`
- Primary audience: PM
- Supporting audience: Product Owner, Delivery, BA, QA, Dev Lead
- Audience tags: PM, PO, BA, QA, Dev
- SDLC stage: Release planning / backlog readiness
- Purpose: Run the final planning gate on the backlog package before estimation, roadmap slicing, or execution planning.
- Output: MVP/release slices, sequencing, readiness score, and planning risks

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
