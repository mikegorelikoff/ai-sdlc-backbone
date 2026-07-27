---
name: ai-sdlc-quality-lenses
description: AI SDLC reusable quality-lens workflow. Use when an AI assistant needs to challenge a requirement, design, plan, test strategy, change, or delivery artifact through pre-mortem, adversarial, edge-case, stakeholder-conflict, reversibility, abuse-case, operational-failure, or assumption lenses and finalize evidence-backed findings with ownership and traceability. Supports `--quick-flow` for selected high-value lenses and `--full-flow` for the complete applicable registry.
---

# ai-sdlc-quality-lenses: Traceable Cross-Artifact Review

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Findings are proposals for review, not authority to change source artifacts.

## 0. Skill Card

- Skill name: `ai-sdlc-quality-lenses`
- Primary audience: BA, QA, Dev, Delivery
- Supporting audience: PM, Architecture, Security
- Audience tags: BA, QA, Dev, Delivery, PM
- SDLC stage: Cross-lifecycle quality review
- Purpose: Apply reusable challenge lenses and finalize evidence-backed findings.
- Output: `quality-lens-report.md` and `_ai_sdlc/quality-lens-report.toon`

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
