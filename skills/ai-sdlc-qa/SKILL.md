---
name: ai-sdlc-qa
description: AI SDLC QA workflow. Use when an AI assistant is asked for QA planning, acceptance validation, regression scope, exploratory checks, smoke tests, release verification, or change-focused manual validation evidence. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.
---

# ai-sdlc-qa: QA Planning And Evidence

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-qa`
- Primary audience: QA
- Supporting audience: BA, Dev, PM
- Audience tags: QA, BA, Dev, PM
- SDLC stage: QA planning and refinement
- Purpose: Produce QA acceptance, regression, manual-check, and signoff evidence for AI SDLC changes and place QA refinement artifacts under `specs-refiniment/<feature-name>/<file.md>` when writing files.
- Output: QA acceptance plan, regression targets, manual checks, validation evidence, and residual risks

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
