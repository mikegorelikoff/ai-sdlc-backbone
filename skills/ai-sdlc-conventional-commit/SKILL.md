---
name: ai-sdlc-conventional-commit
description: AI SDLC Conventional Commit workflow. Use when an AI assistant drafts, validates, reviews, or fixes commit messages in this repository, especially when commits must include SDD spec references, validation summaries, or safe conventional commit subjects. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.
---

# ai-sdlc-conventional-commit: Conventional Commit Message

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-conventional-commit`
- Primary audience: Dev
- Supporting audience: PM, BA, QA
- Audience tags: Dev, PM, BA, QA
- SDLC stage: Commit message drafting
- Purpose: Draft, validate, or repair an AI SDLC commit message that uses Conventional Commit syntax and includes SDD, business, implementation, testing, and validation traceability when the change is medium or large.
- Output: Conventional Commit subject/body with traceability and validation summary

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
