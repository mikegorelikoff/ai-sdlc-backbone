---
name: ai-sdlc-validation
description: AI SDLC backend validation workflow. Use when an AI assistant needs to validate Go, SQL, API, provider integration, SDD, or documentation changes in this repository and choose focused deterministic checks without running unrelated expensive tests by default. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.
---

# ai-sdlc-validation: Validation Command Selection

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-validation`
- Primary audience: Dev
- Supporting audience: QA, BA
- Audience tags: Dev, QA, BA
- SDLC stage: Implementation validation
- Purpose: Select, run, and report focused deterministic validation checks for AI SDLC code, SQL, API, provider, SDD, documentation, and tool-governance changes.
- Output: Focused validation commands, outcomes, coverage notes, and residual risk

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
