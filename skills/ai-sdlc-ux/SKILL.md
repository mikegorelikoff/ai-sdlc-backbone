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

This table is generated from `steps/manifest.toon`. The manifest and linked
step documents are canonical; regenerate this projection after graph changes.

| Step | Ready when | Depends on | Operation | Load |
| --- | --- | --- | --- | --- |
| `preflight` | `prepare` | none | `inspect-and-route` | [`steps/01-prepare.md`](steps/01-prepare.md) — `required` |
| `context` | `clarify`, `route` | `preflight` | `compile-context` | [`steps/02-context.md`](steps/02-context.md) — `required` |
| `execute` | `execute` | `context` | `execute-procedure` | [`steps/02-execute.md`](steps/02-execute.md) — `on-demand` |
| `validate` | `validate` | `execute` | `validate-evidence` | [`steps/03-validate-and-handoff.md`](steps/03-validate-and-handoff.md) — `before-completion` |
| `handoff` | `handoff`, `complete` | `validate` | `handoff-result` | [`steps/04-handoff.md`](steps/04-handoff.md) — `before-completion` |

## Progressive Disclosure Contract

- Resolve the phase entrypoint and dependency-ready set with
  `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`; never invent a step path.
- Read only the emitted StepCard and its selected context. Pass completed step
  IDs back to the selector before requesting the next ready node.
- Treat `direct_read` as an explicit context strategy. Block only when mandatory
  evidence or critical anchors are missing.
- Explore is read-only. After Apply, journal every selected owning-skill step,
  including analysis and validation nodes, before advancing the graph.
- In a source checkout use `skills/<skill>/...`; in a project-scoped install
  use `.agents/skills/<skill>/...`.
