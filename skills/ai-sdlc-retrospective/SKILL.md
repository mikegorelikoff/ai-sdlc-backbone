---
name: ai-sdlc-retrospective
description: AI SDLC evidence-backed retrospective workflow. Use when delivery work is complete or paused and an AI assistant needs to capture observations, connect them to validation or artifact evidence, formulate reviewable process or policy improvement proposals, assign ownership, and preserve the rule that policy changes require an accepted decision. Supports `--quick-flow` for focused learning and `--full-flow` for strict evidence and decision gates.
---

# ai-sdlc-retrospective: Reviewable Delivery Learning

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Retrospectives propose improvements; they never silently change policy.

## 0. Skill Card

- Skill name: `ai-sdlc-retrospective`
- Primary audience: Delivery, Dev, QA, BA
- Supporting audience: PM, platform maintainers
- Audience tags: Delivery, Dev, QA, BA, PM
- SDLC stage: Post-delivery learning
- Purpose: Separate evidence-backed observations from governed improvements.
- Output: `retrospective.md` and `_ai_sdlc/retrospective.toon`

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
