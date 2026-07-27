---
name: ai-sdlc-evidence-council
description: Optional AI SDLC evidence-council workflow. Use when an AI assistant needs to review a high-impact topic through several explicit perspectives, orchestrate simulated lenses or truly independent reviewer executions, and synthesize evidence-backed agreements, conflicts, proposals, owners, and unresolved questions without allowing panel members to rewrite authoritative artifacts. Supports `--quick-flow` for labeled simulated review and `--full-flow` for stricter panel and evidence coverage.
---

# ai-sdlc-evidence-council: Authority-Safe Review Orchestration

> Optional review capability, not required by the core module.
> Every rule below is important to follow. None of it can be skipped.
> A council advises accountable owners; it never becomes approval authority.

## 0. Skill Card

- Skill name: `ai-sdlc-evidence-council`
- Primary audience: Delivery, Architecture, QA, Dev, BA
- Supporting audience: PM, UX, Research, Security
- Audience tags: Delivery, Architecture, QA, Dev, BA, PM
- SDLC stage: Cross-lifecycle high-impact review
- Purpose: Combine multiple evidence perspectives while preserving authority.
- Output: `evidence-council.md` and `_ai_sdlc/evidence-council.toon`

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
