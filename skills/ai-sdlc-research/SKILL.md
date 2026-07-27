---
name: ai-sdlc-research
description: Optional AI SDLC research workflow. Use when an AI assistant needs to investigate a customer, market, domain, technology, regulation, competitor, operational question, or implementation uncertainty and produce a routed source inventory plus synthesized findings with confidence, limitations, open questions, and delivery trace targets. Supports `--quick-flow` for focused evidence and `--full-flow` for multi-source and source-diversity gates.
---

# ai-sdlc-research: Sourced Delivery Evidence

> Optional domain skill, not required by the core module.
> Every rule below is important to follow. None of it can be skipped.
> Research informs decisions; it does not silently become a requirement or approval.

## 0. Skill Card

- Skill name: `ai-sdlc-research`
- Primary audience: Research, PM, BA, Architecture
- Supporting audience: Dev, QA, Security, Delivery
- Audience tags: Research, PM, BA, Architecture, Dev
- SDLC stage: Discovery, refinement, and design evidence
- Purpose: Preserve questions, sources, findings, confidence, and limitations.
- Output: `research.md` and `_ai_sdlc/research.toon`

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
