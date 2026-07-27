---
name: ai-sdlc-ux
description: Optional AI SDLC user-experience workflow. Use when an AI assistant needs to define actors, goals, user journeys, interaction steps, loading/empty/error/success states, recovery behavior, content intent, accessibility requirements, or UX acceptance evidence and route them into traceable human and machine artifacts. Supports `--quick-flow` for a focused journey slice and `--full-flow` for strict state, accessibility, and acceptance coverage.
---

# ai-sdlc-ux: Traceable Experience Specification

> Optional domain skill, not required by the core module.
> Every rule below is important to follow. None of it can be skipped.
> UX artifacts specify behavior; they do not imply stakeholder approval or visual fidelity.

## 0. Skill Card

- Skill name: `ai-sdlc-ux`
- Primary audience: UX, BA, PM
- Supporting audience: Dev, QA, Accessibility, Delivery
- Audience tags: UX, BA, PM, Dev, QA
- SDLC stage: Discovery, refinement, and design
- Purpose: Preserve testable journeys, states, recovery, and accessibility.
- Output: `ux-spec.md` and `_ai_sdlc/ux-spec.toon`

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
